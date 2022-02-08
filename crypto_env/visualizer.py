import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm


class Visualizer:
    """
    问题：
    1、计算速度实在太慢
    2、画图缺少general的适配性，重复代码太多
    下个版本修复这两个问题
    """

    def __init__(self, env, time_feature_name):
        self._env = env
        self._time = time_feature_name

    def draw_signal(self):
        transaction_record = self._env.recorder.get_transaction_record()
        buy_signal_index = transaction_record[transaction_record['signal'] == 0].index
        sell_signal_index = transaction_record[transaction_record['signal'] == 1].index

        fig = make_subplots()
        fig.add_trace(
            go.Scatter(
                dict(mode='lines',
                     name='Price in USD',
                     x=self._env.dataloader.get_feature(self._time),
                     y=self._env.dataloader.get_feature('PriceUSD'),
                     line_color='black',
                     line_width=1)
            )
        )
        fig.add_trace(
            go.Scatter(
                dict(name='buy',
                     mode='markers',
                     x=self._env.dataloader.get_feature(self._time).iloc[buy_signal_index],
                     y=self._env.dataloader.get_feature('PriceUSD').iloc[buy_signal_index],
                     marker_symbol=119,
                     marker_line_color='green',
                     marker_line_width=2,
                     marker_size=15)
            )
        )
        fig.add_trace(
            go.Scatter(
                dict(name='sell',
                     mode='markers',
                     x=self._env.dataloader.get_feature(self._time).iloc[sell_signal_index],
                     y=self._env.dataloader.get_feature('PriceUSD').iloc[sell_signal_index],
                     marker_symbol=120,
                     marker_line_color='red',
                     marker_line_width=2,
                     marker_size=15)
            )
        )
        fig.update_yaxes(title_text="Price in USD")
        fig.update_xaxes(title_text="Time")
        fig.update_layout(template="plotly_white")
        fig.update_layout(title_text='Buy and Sell Signals')
        return fig

    def draw_portfolio(self):
        duration = self._env.dataloader.get_duration()
        fiat_balance_history = []
        crypto_holding_usd_history = []
        total_history = []

        for i in tqdm(range(duration)):
            fiat_balance = self._env.recorder.get_fiat_balance(i)
            fiat_balance_history.append(fiat_balance)

        for i in tqdm(range(duration)):
            crypto_holding_usd = self._env.recorder.get_crypto_value(i)
            crypto_holding_usd_history.append(crypto_holding_usd)

        for i in tqdm(range(duration)):
            payload = fiat_balance_history[i] + crypto_holding_usd_history[i]
            total_history.append(payload)

        fig = make_subplots()
        fig.add_trace(
            go.Scatter(
                dict(mode='lines',
                     name='Fiat Balance',
                     x=self._env.dataloader.get_feature(self._time),
                     y=fiat_balance_history,
                     line_color='red',
                     line_width=1)
            )
        )
        fig.add_trace(
            go.Scatter(
                dict(mode='lines',
                     name='Crypto Holding Value (USD)',
                     x=self._env.dataloader.get_feature(self._time),
                     y=crypto_holding_usd_history,
                     line_color='green',
                     line_width=1)
            )
        )
        fig.add_trace(
            go.Scatter(
                dict(mode='lines',
                     name='Total (USD)',
                     x=self._env.dataloader.get_feature(self._time),
                     y=total_history,
                     line_color='blue',
                     line_width=1)
            )
        )
        fig.update_yaxes(title_text="USD")
        fig.update_xaxes(title_text='Date')
        fig.update_layout(title_text='Portfolio Time Series')
        fig.update_layout(template="plotly_white")
        return fig

    def draw_return(self):
        duration = self._env.dataloader.get_duration()
        roi_history = []

        for i in tqdm(range(duration)):
            roi = self._env.recorder.get_roi(i)
            roi_history.append(roi)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                dict(
                    mode='lines',
                    name='Gross ROI',
                    x=self._env.dataloader.get_feature(self._time),
                    y=roi_history,
                    line_color='blue',
                    line_width=1
                )
            )
        )

        fig.update_yaxes(title_text="Percent", secondary_y=False)
        fig.update_yaxes(title_text="Ratio", secondary_y=True)
        fig.update_xaxes(title_text="Date")
        fig.update_layout(title_text="Gross ROI and Annualized Sharpe Ratio")
        fig.update_layout(template="plotly_white")
        return fig