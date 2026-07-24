# Common events

| Client name           | Event name          | Implemented |          Blink           |
| --------------------- | ------------------- | :---------: | :----------------------: |
| `ps`                  | `ps`                |     [x]     |        [🔗](#ps)         |
| `auth`                | `auth`              |     [x]     |       [🔗](#auth)        |
| `update_balance`      | `updateBalance`     |     [x]     |   [🔗](#updatebalance)   |
| `load_history_period` | `loadHistoryPeriod` |     [x]     | [🔗](#loadhistoryperiod) |
| `demo_refill_balance` | `td/refill`         |     [x]     |     [🔗](#td-refill)     |

# Order / deals events

| Client name                   | Event name                    | Implemented |               Blink                |
| ----------------------------- | ----------------------------- | :---------: | :--------------------------------: |
| `open_deal`                   | `openOrder`                   |     [x]     |          [🔗](#openorder)          |
| ``                            | `copyOrder`                   |     [ ]     |          [🔗](#copyorder)          |
| ``                            | `openFreeTrade`               |     [ ]     |        [🔗](#openfreetrade)        |
| `copy_signal`                 | `copySignalOrder`             |     [x]     |       [🔗](#copysignalorder)       |
| ``                            | `deals/double-up`             |     [ ]     |       [🔗](#deals-double-up)       |
| ``                            | `deals/rollover`              |     [ ]     |       [🔗](#deals-rollover)        |
| `deals_ai`                    | `deals/ai`                    |     [x]     |          [🔗](#deals-ai)           |
| `update_opened_deals`         | `updateOpenedDeals`           |     [x]     |      [🔗](#updateopeneddeals)      |
| ``                            | `social/opened-deal-info`     |     [ ]     |   [🔗](#social-opened-deal-info)   |
| ``                            | `social/closed-deal-info`     |     [ ]     |   [🔗](#social-closed-deal-info)   |
| `social_enable_only_watched`  | `social/enable-only-watched`  |     [x]     | [🔗](#social-enable-only-watched)  |
| `social_disable_only_watched` | `social/disable-only-watched` |     [x]     | [🔗](#social-disable-only-watched) |
| `update_closed_expresses`     | `updateClosedExpresses`       |     [x]     |    [🔗](#updateclosedexpresses)    |
| ``                            | `openExpress`                 |     [ ]     |         [🔗](#openexpress)         |
| ``                            | `openPendingOrder`            |     [ ]     |      [🔗](#openpendingorder)       |
| ``                            | `cancelPendingOrder`          |     [ ]     |     [🔗](#cancelpendingorder)      |

# Assets events

| Client name                        | Event name          | Implemented |          Blink           |
| ---------------------------------- | ------------------- | :---------: | :----------------------: |
| `change_asset`                     | `changeSymbol`      |     [x]     |   [🔗](#changesymbol)    |
| `subscribe_to_asset`               | `subscribeSymbol`   |     [x]     |  [🔗](#subscribesymbol)  |
| ``                                 | `unSubscribeSymbol` |     [ ]     | [🔗](#unsubscribesymbol) |
| `subscribe_for_market_sentiment`   | `subfor`            |     [x]     |      [🔗](#subfor)       |
| `unsubscribe_for_market_sentiment` | `unsubfor`          |     [x]     |     [🔗](#unsubfor)      |

# UI events

| Client name        | Event name             | Implemented |            Blink            |
| ------------------ | ---------------------- | :---------: | :-------------------------: |
| ``                 | `order-chart/load`     |     [ ]     |   [🔗](#order-chart-load)   |
| ``                 | `saveCharts`           |     [ ]     |      [🔗](#savecharts)      |
| ``                 | `deleteChart`          |     [ ]     |     [🔗](#deletechart)      |
| ``                 | `drawing/create`       |     [ ]     |    [🔗](#drawing-create)    |
| ``                 | `drawing/update`       |     [ ]     |    [🔗](#drawing-update)    |
| ``                 | `updateDrawingPoints`  |     [ ]     | [🔗](#updatedrawingpoints)  |
| ``                 | `deleteDrawing`        |     [ ]     |    [🔗](#deletedrawing)     |
| ``                 | `deleteDrawingIds`     |     [ ]     |   [🔗](#deletedrawingids)   |
| ``                 | `deleteDrawings`       |     [ ]     |    [🔗](#deletedrawings)    |
| ``                 | `lockDrawings`         |     [ ]     |     [🔗](#lockdrawings)     |
| `favorite_load`    | `favorite/load`        |     [x]     |    [🔗](#favorite-load)     |
| ``                 | `favorite/change`      |     [ ]     |   [🔗](#favorite-change)    |
| `price_alert_load` | `price-alert/load`     |     [x]     |   [🔗](#price-alert-load)   |
| ``                 | `price-alert/add`      |     [ ]     |   [🔗](#price-alert-add)    |
| ``                 | `price-alert/remove`   |     [ ]     |  [🔗](#price-alert-remove)  |
| ``                 | `user/change-platform` |     [ ]     | [🔗](#user-change-platform) |

# AI events

| Client name                   | Event name                    | Implemented |               Blink                |
| ----------------------------- | ----------------------------- | :---------: | :--------------------------------: |
| ``                            | `ai-strategy-multi/start`     |     [ ]     |   [🔗](#ai-strategy-multi-start)   |
| ``                            | `ai-strategy-multi/stop`      |     [ ]     |   [🔗](#ai-strategy-multi-stop)    |
| `ai_strategy_multi_get_state` | `ai-strategy-multi/get-state` |     [x]     | [🔗](#ai-strategy-multi-get-state) |

# Indicator events

| Client name      | Event name             | Implemented |            Blink            |
| ---------------- | ---------------------- | :---------: | :-------------------------: |
| `indicator_load` | `indicator/load`       |     [x]     |    [🔗](#indicator-load)    |
| ``               | `indicator/create`     |     [ ]     |   [🔗](#indicator-create)   |
| ``               | `indicator/update`     |     [ ]     |   [🔗](#indicator-update)   |
| ``               | `indicator/delete`     |     [ ]     |   [🔗](#indicator-delete)   |
| ``               | `indicator/deleteAll`  |     [ ]     | [🔗](#indicator-deleteall)  |
| ``               | `indicator/fav`        |     [ ]     |    [🔗](#indicator-fav)     |
| ``               | `indicator/unfav`      |     [ ]     |   [🔗](#indicator-unfav)    |
| ``               | `indicator/setVisible` |     [ ]     | [🔗](#indicator-setvisible) |

## Signals events

| Client name           | Event name            | Implemented |           Blink            |
| --------------------- | --------------------- | :---------: | :------------------------: |
| ``                    | `signals/stats`       |     [ ]     |    [🔗](#signals-stats)    |
| `signals_subscribe`   | `signals/subscribe`   |     [x]     |  [🔗](#signals-subscribe)  |
| `signals_unsubscribe` | `signals/unsubscribe` |     [x]     | [🔗](#signals-unsubscribe) |
| ``                    | `sto`                 |     [ ]     |         [🔗](#sto)         |
| ``                    | `sts`                 |     [ ]     |         [🔗](#sts)         |
| ``                    | `usto`                |     [ ]     |        [🔗](#usto)         |

<h2 id="auth"><code>auth</code></h2>
Authenticate socket connection.

### Payload

Demo:

```json
{
  "token": "string",
  "balance": "number",
  "isFastHistory": true
}
```

Real account:

```json
{
  "session": "string",
  "isDemo": true,
  "uid": "number",
  "platform": "number",
  "isFastHistory": true,
  "isOptimized": true
}
```

<h2 id="openorder"><code>openOrder</code></h2>
Open trading order.

### Payload

```json
{
  "asset": "number",
  "amount": "number",
  "action": "string",
  "isDemo": "boolean",
  "requestId": "number",
  "optionType": 100
}
```

### Notes

`requestId` is generated if missing:

```js
requestId = serverTime + randint(1, 100);
```

---

<h2 id="copyorder"><code>copyOrder</code></h2>
Copy existing order.

### Payload

```json
{
  "copyTicket": "string"
}
```

---

<h2 id="openfreetrade"><code>openFreeTrade</code></h2>
Open free trade.

### Payload

```json
{
  "requestId": "number",
  "asset": "number",
  "action": "string",
  "freeTradeId": "number",
  "freeTradeAmount": "number"
}
```

---

<h2 id="copysignalorder"><code>copySignalOrder</code></h2>
Copy signal order.

### Payload

```json
{
  "symbol": "string",
  "amount": "number",
  "expiredAt": "number",
  "action": "string",
  "isDemo": "boolean",
  "requestId": "number",
  "createdAt": "number",
  "timeframe": "number",
  "signalId": "number"
}
```

---

<h2 id="deals-double-up"><code>deals/double-up</code></h2>
Double existing deal.

### Payload

```json
{
  "ticket": "string"
}
```

---

<h2 id="deals-rollover"><code>deals/rollover</code></h2>
Rollover deal.

### Payload

```json
{
  "ticket": "string",
  "amount": "number"
}
```

---

<h2 id="deals-ai"><code>deals/ai</code></h2>
AI deal operation.

### Payload

```js
unknown;
```

---

<h2 id="ai-strategy-multi-start"><code>ai-strategy-multi/start</code></h2>
Start AI strategy.

### Payload

```json
{
  "symbol": "string",
  "strategy": "object",
  "startAmount": "number",
  "dealsCount": "number"
}
```

---

<h2 id="ai-strategy-multi-stop"><code>ai-strategy-multi/stop</code></h2>
Stop AI strategy.

### Payload

```json
{
  "sessionId": "string"
}
```

---

<h2 id="ai-strategy-multi-get-state"><code>ai-strategy-multi/get-state</code></h2>
Get AI strategy state.

---

<h2 id="changesymbol"><code>changeSymbol</code></h2>
Change active trading asset.

### Payload

```json
{
  "asset": "number",
  "period": "number"
}
```

### Period mapping

Internal timeframe ID → seconds:

| ID  | Seconds |
| --- | ------: |
| 15  |       1 |
| 0   |       5 |
| 1   |      10 |
| 2   |      15 |
| 3   |      30 |
| 4   |      60 |
| 13  |     120 |
| 14  |     180 |
| 6   |     300 |
| 7   |     600 |
| 8   |     900 |
| 9   |    1800 |
| 10  |    3600 |
| 11  |   14400 |
| 12  |   86400 |

---

<h2 id="subscribesymbol"><code>subscribeSymbol</code></h2>
Subscribe symbol.

### Payload

```js
unknown;
```

---

<h2 id="unsubscribesymbol"><code>unSubscribeSymbol</code></h2>
Unsubscribe symbol.

### Payload

```js
unknown;
```

---

<h2 id="updatebalance"><code>updateBalance</code></h2>
Request balance update.

---

<h2 id="loadhistoryperiod"><code>loadHistoryPeriod</code></h2>
Load candle history.

### Payload

```json
{
  "asset": "number",
  "index": "number",
  "time": "number",
  "offset": "number",
  "period": "number"
}
```

---

<h2 id="order-chart-load"><code>order-chart/load</code></h2>
Load chart data for order.

### Payload

```json
{
  "id": "number",
  "timeFrom": "number",
  "timeTo": "number",
  "digits": "number",
  "price": "number",
  "openTimestamp": "number",
  "symbolId": "number"
}
```

---

<h2 id="savecharts"><code>saveCharts</code></h2>
Save chart settings.

### Payload

```json
{
  "chartId": "string",
  "chartType": "string",
  "chartPeriod": "number",
  "candlesTimer": "number",
  "symbol": "string",
  "demoDealAmount": "number",
  "liveDealAmount": "number",
  "enabledTradeMonitor": "boolean",
  "enabledRatingWidget": "boolean",
  "isVisible": "boolean",
  "fastTimeframe": "number",
  "enabledAutoscroll": "boolean",
  "enabledGridSnap": "boolean",
  "minimizedTradePanel": "boolean",
  "fastCloseAt": "number",
  "enableQuickAutoOffset": "boolean",
  "quickAutoOffsetValue": "number",
  "showArea": "boolean",
  "percentAmount": "number",
  "aiStrategyStrategy": "string",
  "aiStrategyStartAmount": "number",
  "aiStrategyDealsCount": "number"
}
```

---

<h2 id="deletechart"><code>deleteChart</code></h2>
Delete chart.

### Payload

```json
{
  "chartId": "string"
}
```

---

<h2 id="indicator-create"><code>indicator/create</code></h2>
Create indicator.

### Payload

```json
{
  "requestId": "number",
  "chartId": "string",
  "type": "string",
  "settings": "object",
  "visible": 1
}
```

---

<h2 id="indicator-update"><code>indicator/update</code></h2>
Update indicator.

### Payload

```json
{
  "id": "number",
  "settings": "object"
}
```

---

<h2 id="indicator-delete"><code>indicator/delete</code></h2>
Delete indicator.

### Payload

```json
{
  "id": "number"
}
```

---

<h2 id="indicator-deleteall"><code>indicator/deleteAll</code></h2>
Delete all indicators.

### Payload

```json
{
  "chartId": "string"
}
```

---

<h2 id="indicator-fav"><code>indicator/fav</code></h2>
Add indicator to favorites.

### Payload

```json
{
  "type": "string"
}
```

---

<h2 id="indicator-unfav"><code>indicator/unfav</code></h2>
Remove indicator from favorites.

### Payload

```json
{
  "type": "string"
}
```

---

<h2 id="indicator-setvisible"><code>indicator/setVisible</code></h2>
Change indicator visibility.

### Payload

```json
{
  "id": "number",
  "visible": 0
}
```

---

<h2 id="drawing-create"><code>drawing/create</code></h2>
Create drawing.

### Payload

```json
{
  "chartId": "string",
  "settings": "object",
  "type": "string",
  "assetId": "number",
  "requestId": "number"
}
```

---

<h2 id="drawing-update"><code>drawing/update</code></h2>
Update drawing.

### Payload

```json
{
  "id": "number",
  "settings": "object"
}
```

---

<h2 id="updatedrawingpoints"><code>updateDrawingPoints</code></h2>
Update drawing points.

### Payload

```json
[["drawingId", "point", "time", "price", "assetId", "chartId"]]
```

---

<h2 id="deletedrawing"><code>deleteDrawing</code></h2>
Delete drawing.

### Payload

```json
{
  "drawingId": "number",
  "chartId": "string"
}
```

---

<h2 id="deletedrawings"><code>deleteDrawings</code></h2>
Delete drawings.

### Payload

```json
{
  "chartId": "string",
  "assetId": "number"
}
```

---

<h2 id="lockdrawings"><code>lockDrawings</code></h2>
Lock drawings.

### Payload

```json
["chartId", "locked"]
```

---

<h2 id="social-opened-deal-info"><code>social/opened-deal-info</code></h2>
Get opened social deal info.

### Payload

```json
{
  "copyTicket": "string"
}
```

---

<h2 id="social-closed-deal-info"><code>social/closed-deal-info</code></h2>
Get closed social deal info.

### Payload

```json
{
  "copyTicket": "string"
}
```

---

<h2 id="social-enable-only-watched"><code>social/enable-only-watched</code></h2>
Enable watched filter.

---

<h2 id="social-disable-only-watched"><code>social/disable-only-watched</code></h2>
Disable watched filter.

---

<h2 id="favorite-load"><code>favorite/load</code></h2>
Load favorites.

---

<h2 id="favorite-change"><code>favorite/change</code></h2>
Change favorite.

### Payload

```js
unknown;
```

---

<h2 id="price-alert-load"><code>price-alert/load</code></h2>
Load price alerts.

---

<h2 id="price-alert-add"><code>price-alert/add</code></h2>
Add price alert.

### Payload

```json
{
  "price": "number",
  "assetId": "number"
}
```

---

<h2 id="price-alert-remove"><code>price-alert/remove</code></h2>
Remove price alert.

### Payload

```json
{
  "id": "number"
}
```

---

<h2 id="openpendingorder"><code>openPendingOrder</code></h2>
Create pending order.

### Payload

```js
unknown;
```

---

<h2 id="cancelpendingorder"><code>cancelPendingOrder</code></h2>
Cancel pending order.

### Payload

```json
{
  "ticket": "string"
}
```

---

<h2 id="subfor"><code>subfor</code></h2>
Subscribe market forecast.

### Payload

```js
unknown;
```

---

<h2 id="unsubfor"><code>unsubfor</code></h2>
Unsubscribe market forecast.

### Payload

```js
unknown;
```

---

<h2 id="user-change-platform"><code>user/change-platform</code></h2>
Change platform.

### Payload

```json
{
  "platform": "number"
}
```

---

<h2 id="td-refill"><code>td/refill</code></h2>
Refill demo balance.

<h2 id="signals-stats"><code>signals/stats</code></h2>
### Payload

```js
unknown;
```

<h2 id="updateclosedexpresses"><code>updateClosedExpresses</code></h2>
### Payload

```js
unknown;
```

<h2 id="openexpress"><code>openExpress</code></h2>
### Payload

```json
[e, t]
```

<h2 id="signals-subscribe"><code>signals/subscribe</code></h2>
<h2 id="signals-unsubscribe"><code>signals/unsubscribe</code></h2>
<h2 id="sto"><code>sto</code></h2>
subscribeSocialTradingOrders

### Payload

```json
{
  "showOnlyWatched": unknown,
  "symbols": unknown,
}
```

<h2 id="sts"><code>sts</code></h2>
updateSocialTradingSymbols

### Payload

```json
{
  "showOnlyWatched": unknown,
  "symbols": unknown,
}
```

<h2 id="usto"><code>usto</code></h2>
unSubscribeSocialTradingOrders

<h2 id="deletedrawingsids"><code>deleteDrawingsIds</code></h2>
### Payload

```js
unknown;
```

<h2 id="updateopeneddeals"><code>updateOpenedDeals</code></h2>
<h2 id="ps"><code>ps</code></h2>
