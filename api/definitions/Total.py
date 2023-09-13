import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np

class Total:
    def __init__(self, accounts):
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
        pass

    def plot(self):
        calculated_reverse = list(reversed(self.calculated))
        diff = calculated_reverse[-1].get('timestamp') - calculated_reverse[0].get('timestamp')
        x = [d.get('timestamp') for d in calculated_reverse]
        y = [d.get('current') for d in calculated_reverse]

        xn = np.array(x).reshape((-1, 1))
        yn = np.array(y)
        model = LinearRegression().fit(xn, yn)
        y_pred = model.predict(xn)
        x2 = [(x + diff) for x in x]
        x2n = np.array(x2).reshape((-1, 1))
        y_pred2 = model.predict(x2n)

        plt.plot(x, y)
        plt.plot(
            [calculated_reverse[0].get('timestamp'), calculated_reverse[-1].get('timestamp')],
            [0, 0]
        )
        plt.plot(x, y_pred)
        plt.plot(x2, y_pred2)
        plt.show()