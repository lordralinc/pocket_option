from __future__ import annotations

import abc
import os
import pathlib
import typing
import warnings

import pydantic

from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, UpdateAssetItem

if typing.TYPE_CHECKING:
    from pocket_option.generated_client import PocketOptionClient
    from pocket_option.models import Asset
    from pocket_option.utils import Q

__all__ = ("AssetsStorage",)


class AssetsStorage(abc.ABC):
    def __init__(self, client: PocketOptionClient) -> None:
        self.client = client

        self.client.on.assets_update(self._on_update_assets)

        self.client.assets = self

    async def _on_update_assets(self, items: list[UpdateAssetItem]) -> None:
        await self.add_assets_bulk(items)

    @abc.abstractmethod
    async def get_assets(self) -> list[UpdateAssetItem]: ...

    @typing.overload
    async def get_asset(self, *, assset: Asset) -> UpdateAssetItem | None: ...
    @typing.overload
    async def get_asset(self, *, asset_id: int) -> UpdateAssetItem | None: ...
    @abc.abstractmethod
    async def get_asset(
        self,
        *,
        assset: Asset | None = None,
        asset_id: int | None = None,
    ) -> UpdateAssetItem | None: ...

    @abc.abstractmethod
    async def search_assets(self, *, query: typing.Any | None = None) -> list[UpdateAssetItem]: ...

    @abc.abstractmethod
    async def add_asset(self, item: UpdateAssetItem) -> None: ...
    @abc.abstractmethod
    async def add_assets_bulk(self, items: list[UpdateAssetItem]) -> None: ...


class MemoryAssetsStorage(AssetsStorage):
    def __init__(self, client: PocketOptionClient):
        super().__init__(client)
        self._storage: dict[int, UpdateAssetItem] = {}

    async def get_assets(self) -> list[UpdateAssetItem]:
        return list(self._storage.values())

    @typing.overload
    async def get_asset(self, *, assset: Asset) -> UpdateAssetItem | None: ...
    @typing.overload
    async def get_asset(self, *, asset_id: int) -> UpdateAssetItem | None: ...
    async def get_asset(self, *, assset: Asset | None = None, asset_id: int | None = None) -> UpdateAssetItem | None:
        if asset_id is not None:
            return self._storage.get(asset_id)
        if assset is not None:
            for item in self._storage.values():
                if item.asset == assset:
                    return item
        return None

    async def search_assets(self, *, query: Q | None = None) -> list[UpdateAssetItem]:
        assets = list(self._storage.values())
        if query is not None:
            assets = [it for it in assets if query(it)]
        return assets

    async def add_asset(self, item: UpdateAssetItem) -> None:
        self._storage[item.id] = item

    async def add_assets_bulk(self, items: list[UpdateAssetItem]) -> None:
        for it in items:
            await self.add_asset(it)


class JSONAssetsStorage(MemoryAssetsStorage):
    TYPE_ADAPTER = pydantic.TypeAdapter(dict[int, UpdateAssetItem])

    def __init__(self, client: PocketOptionClient):
        super().__init__(client)
        self.path = pathlib.Path("reverse", "assets.json")
        if os.environ.get("PO_DEBUG") != "1":
            warnings.warn(
                "JSONAssetsStorage is intended for development/testing only. Do not use it in production.",
                RuntimeWarning,
                stacklevel=2,
            )

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes(self.TYPE_ADAPTER.dump_json(self._storage, indent=2))

    async def add_asset(self, item: UpdateAssetItem):
        await super().add_asset(item)
        self.save()
