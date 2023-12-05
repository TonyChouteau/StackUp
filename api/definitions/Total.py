import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np
import datetime

import pandas
import plotly.express as px
import plotly.graph_objects as go


class Total:
    def __init__(self, accounts):
        self.accounts = accounts

        self.final_value = 0
        calculated_concat = []
        for account_number in accounts:
            self.final_value += accounts[account_number].final_value
            calculated_concat += accounts[account_number].calculated

        calculated_sorted = sorted(calculated_concat, key=lambda line: line.get("timestamp"), reverse=True)

        current = self.final_value
        self.calculated = []
        for data in calculated_sorted:
            last = current - data.get("change")

            self.calculated.append({
                **data,
                "current": current,
                "last": last,
                "change%": data.get("change")/last if last != 0 else 100
            })
            current = last

        self.to_plot = list(reversed(self.calculated))

    def plot(self):
        for account_number in self.accounts:
            account = self.accounts[account_number]
            account.plot()

        diff = self.to_plot[-1].get('timestamp') - self.to_plot[0].get('timestamp')
        x = [d.get('timestamp') for d in self.to_plot]
        y = [d.get('current') for d in self.to_plot]

        xn = np.array(x).reshape((-1, 1))
        yn = np.array(y)
        model = LinearRegression().fit(xn, yn)
        y_pred = model.predict(xn)
        x2 = [(x + diff) for x in x]
        x2n = np.array(x2).reshape((-1, 1))
        y_pred2 = model.predict(x2n)

        plt.plot(x, y)
        plt.plot(
            [self.to_plot[0].get('timestamp'), self.to_plot[-1].get('timestamp')],
            [0, 0]
        )
        plt.plot(x, y_pred)
        plt.plot(x2, y_pred2)
        print("Total :")
        print(f"Value for {datetime.datetime.fromtimestamp(x2[-1])} : {y_pred2[-1]}")
        plt.show()

    def plotly(self):
        x = [d.get('date') for d in self.to_plot]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=[0 for _ in self.to_plot],
                                 mode='lines+markers',
                                 name='0'))
        fig.add_trace(go.Scatter(x=x, y=[d.get('current') for d in self.to_plot],
                                 mode='lines+markers',
                                 name='Total'))

        for account_number in self.accounts:
            account = self.accounts[account_number]
            xa = [d.get('date') for d in account.to_plot]
            ya = [d.get('current') for d in account.to_plot]
            fig.add_trace(go.Scatter(x=xa, y=ya,
                                     mode='lines+markers',
                                     name=f'{account.account_name}'))

        fig.write_html("graph.html")