| Client name                | Event name                           | Implemented |                   Blink                   |
| -------------------------- | ------------------------------------ | :---------: | :---------------------------------------: |
| `disconnect`               | `disconnect`                         |     [x]     |             [🔗](#disconnect)             |
| `connect`                  | `connect`                            |     [x]     |              [🔗](#connect)               |
| `success_auth`             | `successauth`                        |     [x]     |            [🔗](#successauth)             |
| ``                         | `NotAuthorized`                      |     [ ]     |           [🔗](#notauthorized)            |
| `update_balance`           | `successupdateBalance`               |     [x]     |        [🔗](#successupdatebalance)        |
| `update_assets`            | `updateAssets`                       |     [x]     |            [🔗](#updateassets)            |
| `update_close_value`       | `updateStream`                       |     [x]     |            [🔗](#updatestream)            |
| ``                         | `updateHistoryNew`                   |     [ ]     |          [🔗](#updatehistorynew)          |
| `update_history_new_fast`  | `updateHistoryNewFast`               |     [x]     |        [🔗](#updatehistorynewfast)        |
| ``                         | `updateTime`                         |     [ ]     |             [🔗](#updatetime)             |
| `update_opened_deals`      | `updateOpenedDeals`                  |     [x]     |         [🔗](#updateopeneddeals)          |
| ``                         | `updateClosedDeals`                  |     [ ]     |         [🔗](#updatecloseddeals)          |
| `success_open_deal`        | `successopenOrder`                   |     [x]     |          [🔗](#successopenorder)          |
| ``                         | `failopenOrder`                      |     [ ]     |           [🔗](#failopenorder)            |
| ``                         | `successcloseOrder`                  |     [ ]     |         [🔗](#successcloseorder)          |
| ``                         | `successcopyOrder`                   |     [ ]     |          [🔗](#successcopyorder)          |
| ``                         | `failcopyOrder`                      |     [ ]     |           [🔗](#failcopyorder)            |
| ``                         | `successopenExpress`                 |     [ ]     |         [🔗](#successopenexpress)         |
| ``                         | `failopenExpress`                    |     [ ]     |          [🔗](#failopenexpress)           |
| ``                         | `successcloseExpress`                |     [ ]     |        [🔗](#successcloseexpress)         |
| ``                         | `successupdateOpenedExpresses`       |     [ ]     |    [🔗](#successupdateopenedexpresses)    |
| ``                         | `successupdateClosedExpresses`       |     [ ]     |    [🔗](#successupdateclosedexpresses)    |
| ``                         | `successupdateExpress`               |     [ ]     |        [🔗](#successupdateexpress)        |
| ``                         | `successindicator/create`            |     [ ]     |      [🔗](#successindicator-create)       |
| ``                         | `failindicator/create`               |     [ ]     |        [🔗](#failindicator-create)        |
| ``                         | `successindicator/load`              |     [ ]     |       [🔗](#successindicator-load)        |
| ``                         | `successindicator/delete`            |     [ ]     |      [🔗](#successindicator-delete)       |
| ``                         | `successindicator/deleteAll`         |     [ ]     |     [🔗](#successindicator-deleteall)     |
| ``                         | `successdrawing/create`              |     [ ]     |       [🔗](#successdrawing-create)        |
| ``                         | `faildrawing/create`                 |     [ ]     |         [🔗](#faildrawing-create)         |
| ``                         | `successdrawing/load`                |     [ ]     |        [🔗](#successdrawing-load)         |
| ``                         | `successdeleteDrawing`               |     [ ]     |        [🔗](#successdeletedrawing)        |
| ``                         | `updateOpenedSocialDeals`            |     [ ]     |      [🔗](#updateopenedsocialdeals)       |
| ``                         | `updateClosedSocialDeals`            |     [ ]     |      [🔗](#updateclosedsocialdeals)       |
| ``                         | `openSocialDeal`                     |     [ ]     |           [🔗](#opensocialdeal)           |
| ``                         | `signals/load`                       |     [ ]     |            [🔗](#signals-load)            |
| ``                         | `signals/update`                     |     [ ]     |           [🔗](#signals-update)           |
| ``                         | `successsignals/stats`               |     [ ]     |        [🔗](#successsignals-stats)        |
| ``                         | `successai-strategy-multi/start`     |     [ ]     |   [🔗](#successai-strategy-multi-start)   |
| ``                         | `failai-strategy-multi/start`        |     [ ]     |    [🔗](#failai-strategy-multi-start)     |
| ``                         | `successai-strategy-multi/stop`      |     [ ]     |   [🔗](#successai-strategy-multi-stop)    |
| ``                         | `failai-strategy-multi/stop`         |     [ ]     |     [🔗](#failai-strategy-multi-stop)     |
| ``                         | `successai-strategy-multi/get-state` |     [ ]     | [🔗](#successai-strategy-multi-get-state) |
| ``                         | `failai-strategy-multi/get-state`    |     [ ]     |  [🔗](#failai-strategy-multi-get-state)   |
| ``                         | `ai-strategy-multi/update`           |     [ ]     |      [🔗](#ai-strategy-multi-update)      |
| `change_market_sentiment`  | `chafor`                             |     [x]     |               [🔗](#chafor)               |
| ``                         | `failopenOrder`                      |     [ ]     |           [🔗](#failopenorder)            |
| ``                         | `updateClosedSocialDeals`            |     [ ]     |      [🔗](#updateclosedsocialdeals)       |
| ``                         | `updateOpenedSocialDeals`            |     [ ]     |      [🔗](#updateopenedsocialdeals)       |
| ``                         | `updateAchievements`                 |     [ ]     |         [🔗](#updateachievements)         |
| `update_closed_deals`      | `updateClosedDeals`                  |     [x]     |         [🔗](#updatecloseddeals)          |
| ``                         | `successopenOrder`                   |     [ ]     |          [🔗](#successopenorder)          |
| ``                         | `successopenFreeTrade`               |     [ ]     |        [🔗](#successopenfreetrade)        |
| ``                         | `failopenFreeTrade`                  |     [ ]     |         [🔗](#failopenfreetrade)          |
| ``                         | `successpending/created`             |     [ ]     |       [🔗](#successpending-created)       |
| ``                         | `failpending/created`                |     [ ]     |        [🔗](#failpending-created)         |
| ``                         | `10NUMBER_DEALS_WITH_PROFIT`         |     [ ]     |     [🔗](#10number_deals_with_profit)     |
| ``                         | `successcopyOrder`                   |     [ ]     |          [🔗](#successcopyorder)          |
| ``                         | `failcopyOrder`                      |     [ ]     |           [🔗](#failcopyorder)            |
| ``                         | `failcancelOrder`                    |     [ ]     |          [🔗](#failcancelorder)           |
| ``                         | `successcancelOrder`                 |     [ ]     |         [🔗](#successcancelorder)         |
| ``                         | `loadHistoryPeriod`                  |     [ ]     |         [🔗](#loadhistoryperiod)          |
| `load_history_period_fast` | `loadHistoryPeriodFast`              |     [x]     |       [🔗](#loadhistoryperiodfast)        |
| ``                         | `updateCharts`                       |     [ ]     |            [🔗](#updatecharts)            |
| ``                         | `successopenExpress`                 |     [ ]     |         [🔗](#successopenexpress)         |
| ``                         | `failopenExpress`                    |     [ ]     |          [🔗](#failopenexpress)           |
| ``                         | `successcloseExpress`                |     [ ]     |        [🔗](#successcloseexpress)         |
| ``                         | `successcloseExpressDeals`           |     [ ]     |      [🔗](#successcloseexpressdeals)      |
| ``                         | `successupdateOpenedExpresses`       |     [ ]     |    [🔗](#successupdateopenedexpresses)    |
| ``                         | `successupdateClosedExpresses`       |     [ ]     |    [🔗](#successupdateclosedexpresses)    |
| ``                         | `successupdateExpress`               |     [ ]     |        [🔗](#successupdateexpress)        |
| ``                         | `successdeleteDrawing`               |     [ ]     |        [🔗](#successdeletedrawing)        |
| ``                         | `successdrawing/create`              |     [ ]     |       [🔗](#successdrawing-create)        |
| ``                         | `faildrawing/create`                 |     [ ]     |         [🔗](#faildrawing-create)         |
| ``                         | `successdrawing/load`                |     [ ]     |        [🔗](#successdrawing-load)         |
| `success_close_deal`       | `successcloseOrder`                  |     [x]     |         [🔗](#successcloseorder)          |
| ``                         | `successindicator/create`            |     [ ]     |      [🔗](#successindicator-create)       |
| ``                         | `failindicator/create`               |     [ ]     |        [🔗](#failindicator-create)        |
| ``                         | `successindicator/load`              |     [ ]     |       [🔗](#successindicator-load)        |
| ``                         | `successindicator/deleteAll`         |     [ ]     |     [🔗](#successindicator-deleteall)     |
| ``                         | `successindicator/delete`            |     [ ]     |      [🔗](#successindicator-delete)       |
| ``                         | `successopenPendingOrder`            |     [ ]     |      [🔗](#successopenpendingorder)       |
| ``                         | `failopenPendingOrder`               |     [ ]     |        [🔗](#failopenpendingorder)        |
| ``                         | `successupdatePending`               |     [ ]     |        [🔗](#successupdatepending)        |
| ``                         | `successcancelPendingOrder`          |     [ ]     |     [🔗](#successcancelpendingorder)      |
| ``                         | `failcancelPendingOrder`             |     [ ]     |       [🔗](#failcancelpendingorder)       |
| ``                         | `successorder-chart/load`            |     [ ]     |      [🔗](#successorder-chart-load)       |
| ``                         | `successsocial/opened-deal-info`     |     [ ]     |   [🔗](#successsocial-opened-deal-info)   |
| ``                         | `successsocial/closed-deal-info`     |     [ ]     |   [🔗](#successsocial-closed-deal-info)   |
| ``                         | `signals/load`                       |     [ ]     |            [🔗](#signals-load)            |
| ``                         | `signals/update`                     |     [ ]     |           [🔗](#signals-update)           |
| ``                         | `successsignals/stats`               |     [ ]     |        [🔗](#successsignals-stats)        |
| ``                         | `successcopySignalOrder`             |     [ ]     |       [🔗](#successcopysignalorder)       |
| ``                         | `successdeals/rollover`              |     [ ]     |       [🔗](#successdeals-rollover)        |
| ``                         | `faildeals/rollover`                 |     [ ]     |         [🔗](#faildeals-rollover)         |
| ``                         | `successfavorite/load`               |     [ ]     |        [🔗](#successfavorite-load)        |
| ``                         | `successfavorite/change`             |     [ ]     |       [🔗](#successfavorite-change)       |
| ``                         | `successprice-alert/load`            |     [ ]     |      [🔗](#successprice-alert-load)       |
| ``                         | `successprice-alert/add`             |     [ ]     |       [🔗](#successprice-alert-add)       |
| ``                         | `failprice-alert/add`                |     [ ]     |        [🔗](#failprice-alert-add)         |
| ``                         | `successprice-alert/remove`          |     [ ]     |     [🔗](#successprice-alert-remove)      |
| ``                         | `tradingReward`                      |     [ ]     |           [🔗](#tradingreward)            |
| ``                         | `successai-strategy-multi/start`     |     [ ]     |   [🔗](#successai-strategy-multi-start)   |
| ``                         | `failai-strategy-multi/start`        |     [ ]     |    [🔗](#failai-strategy-multi-start)     |
| ``                         | `successai-strategy-multi/stop`      |     [ ]     |   [🔗](#successai-strategy-multi-stop)    |
| ``                         | `failai-strategy-multi/stop`         |     [ ]     |     [🔗](#failai-strategy-multi-stop)     |
| ``                         | `successai-strategy-multi/get-state` |     [ ]     | [🔗](#successai-strategy-multi-get-state) |
| ``                         | `failai-strategy-multi/get-state`    |     [ ]     |  [🔗](#failai-strategy-multi-get-state)   |
| ``                         | `ai-strategy-multi/update"`          |     [ ]     |     [🔗](#ai-strategy-multi-update")      |

# Connection

<h2 id="disconnect"><code>disconnect</code></h2>
Socket disconnected.

### Payload

```json
{}
```

---

<h2 id="successauth"><code>successauth</code></h2>
Authentication successful.

### Payload

```json
{}
```

---

<h2 id="notauthorized"><code>NotAuthorized</code></h2>
Authorization failed.

### Payload

```json
{}
```

---

# Market Data

<h2 id="updateassets"><code>updateAssets</code></h2>
Updates available trading assets.

### Payload

```json
{}
```

---

<h2 id="updatestream"><code>updateStream</code></h2>
Real-time price stream update.

### Payload

```json
[["assetId", "timestamp", "price"]]
```

### Processing

Server sends compressed arrays:

```js
[asset, time, price];
```

Client converts them to:

```js
{
  (asset, time, price);
}
```

Equivalent:

```js
function updateStream(data) {
  const stream = data.map(([asset, time, price]) => ({
    asset,
    time,
    price,
  }));

  updateStream(stream);
}
```

---

<h2 id="updatehistorynew"><code>updateHistoryNew</code></h2>
New history data received.

### Payload

```json
{}
```

### Processing

The latest candle price updates server time:

```js
function (payload) {
    const data = parse(payload);

    const history = data.history.sort(
        (a, b) => a[0] - b[0]
    );

    if (history.length > 0) {
        const [time, price] =
            history[history.length - 1];

        updateStream(
            [{
                asset: data.asset,
                time,
                price
            }],
            true
        );
    }
}
```

---

<h2 id="updatehistorynewfast"><code>updateHistoryNewFast</code></h2>
Fast history update.

Same behavior as:

```
updateHistoryNew
```

### Processing

```js
updateStream(
  [
    {
      asset,
      time,
      price,
    },
  ],
  true,
);
```

---

<h2 id="updatetime"><code>updateTime</code></h2>
Update server timestamp.

### Payload

```json
1234567890
```

### Processing

```js
function(time) {
    const timestamp = Math.floor(time);

    if (serverTime < timestamp) {
        serverTime = timestamp;
    }
}
```

---

# Deals

<h2 id="updateopeneddeals"><code>updateOpenedDeals</code></h2>
Opened deals update.

### Payload

```json
{}
```

---

<h2 id="updatecloseddeals"><code>updateClosedDeals</code></h2>
Closed deals update.

### Payload

```json
{}
```

---

<h2 id="successopenorder"><code>successopenOrder</code></h2>
Order opened successfully.

### Payload

```json
{}
```

---

<h2 id="failopenorder"><code>failopenOrder</code></h2>
Order opening failed.

### Payload

```json
{}
```

---

<h2 id="successcloseorder"><code>successcloseOrder</code></h2>
Order closed successfully.

### Payload

```json
{}
```

---

<h2 id="successcopyorder"><code>successcopyOrder</code></h2>
Copy order successful.

### Payload

```json
{}
```

---

<h2 id="failcopyorder"><code>failcopyOrder</code></h2>
Copy order failed.

### Payload

```json
{}
```

---

# Express Deals

<h2 id="successopenexpress"><code>successopenExpress</code></h2>
Express deal opened.

### Payload

```json
{}
```

---

<h2 id="failopenexpress"><code>failopenExpress</code></h2>
Express deal failed.

### Payload

```json
{}
```

---

<h2 id="successcloseexpress"><code>successcloseExpress</code></h2>
Express deal closed.

### Payload

```json
{}
```

---

<h2 id="successupdateopenedexpresses"><code>successupdateOpenedExpresses</code></h2>
Opened express deals updated.

### Payload

```json
{}
```

---

<h2 id="successupdateclosedexpresses"><code>successupdateClosedExpresses</code></h2>
Closed express deals updated.

### Payload

```json
{}
```

---

<h2 id="successupdateexpress"><code>successupdateExpress</code></h2>
Express deal update.

### Payload

```json
{}
```

---

# Indicators

<h2 id="successindicator-create"><code>successindicator/create</code></h2>
Indicator created.

### Payload

```json
{}
```

---

<h2 id="failindicator-create"><code>failindicator/create</code></h2>
Indicator creation failed.

### Payload

```json
{}
```

---

<h2 id="successindicator-load"><code>successindicator/load</code></h2>
Indicators loaded.

### Payload

```json
{}
```

---

<h2 id="successindicator-delete"><code>successindicator/delete</code></h2>
Indicator deleted.

### Payload

```json
{}
```

---

<h2 id="successindicator-deleteall"><code>successindicator/deleteAll</code></h2>
All indicators deleted.

### Payload

```json
{}
```

---

# Drawings

<h2 id="successdrawing-create"><code>successdrawing/create</code></h2>
Drawing created.

### Payload

```json
{}
```

---

<h2 id="faildrawing-create"><code>faildrawing/create</code></h2>
Drawing creation failed.

### Payload

```json
{}
```

---

<h2 id="successdrawing-load"><code>successdrawing/load</code></h2>
Drawings loaded.

### Payload

```json
{}
```

---

<h2 id="successdeletedrawing"><code>successdeleteDrawing</code></h2>
Drawing deleted.

### Payload

```json
{}
```

---

# Social Trading

<h2 id="updateopenedsocialdeals"><code>updateOpenedSocialDeals</code></h2>
Opened social deals update.

### Payload

```json
{}
```

---

<h2 id="updateclosedsocialdeals"><code>updateClosedSocialDeals</code></h2>
Closed social deals update.

### Payload

```json
{}
```

---

<h2 id="opensocialdeal"><code>openSocialDeal</code></h2>
Open social deal.

### Payload

```json
{}
```

---

# Signals

<h2 id="signals-load"><code>signals/load</code></h2>
Load signals.

### Payload

```json
{}
```

---

<h2 id="signals-update"><code>signals/update</code></h2>
Signal update.

### Payload

```json
{}
```

---

<h2 id="successsignals-stats"><code>successsignals/stats</code></h2>
Signal statistics.

### Payload

```json
{}
```

---

# AI Strategy

<h2 id="successai-strategy-multi-start"><code>successai-strategy-multi/start</code></h2>
AI strategy started.

### Payload

```json
{}
```

---

<h2 id="failai-strategy-multi-start"><code>failai-strategy-multi/start</code></h2>
AI strategy start failed.

### Payload

```json
{}
```

---

<h2 id="successai-strategy-multi-stop"><code>successai-strategy-multi/stop</code></h2>
AI strategy stopped.

### Payload

```json
{}
```

---

<h2 id="failai-strategy-multi-stop"><code>failai-strategy-multi/stop</code></h2>
AI strategy stop failed.

### Payload

```json
{}
```

---

<h2 id="successai-strategy-multi-get-state"><code>successai-strategy-multi/get-state</code></h2>
AI strategy state.

### Payload

```json
{}
```

---

<h2 id="failai-strategy-multi-get-state"><code>failai-strategy-multi/get-state</code></h2>
AI strategy state error.

### Payload

```json
{}
```

---

<h2 id="ai-strategy-multi-update"><code>ai-strategy-multi/update</code></h2>
AI strategy update.

### Payload

```json
{}
```
