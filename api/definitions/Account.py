import re
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np

class Account:

    FORMAT_VALUE = "[0-9]{0,3} ?[0-9]{1,3},[0-9]{0,3}"

    def __init__(self, head, data):
        self.head = head
        self.data = data

        for line in self.head:
            if "n°" in line:
                self.account_number = line.split("n° ")[1].replace(";", "")
                if " carte n°" in line:
                    self.account_name = line.split(" carte n°")[0]
                else:
                    self.account_name = line.split(" n°")[0]
            if "Solde" in line:
                final_value = re.findall(f" {self.FORMAT_VALUE}", line.replace("\xa0", " "))
                if len(final_value) >= 1:
                    self.final_value = float(final_value[0].replace(" ", "").replace(",", "."))
                else:
                    self.final_value = 0

        if self.final_value == 0:
            print("ERRRRORRRRR")

        current = self.final_value
        self.calculated = []
        for data in self.data:
            format_list = data.replace("\xa0", " ").replace("\"", "").split(";")

            dt = datetime.strptime(format_list[0], "%d/%m/%Y")
            change_loss = re.findall(self.FORMAT_VALUE, format_list[2])
            change_gain = re.findall(self.FORMAT_VALUE, format_list[3])
            if len(change_gain) >= 1:
                change_gain = float(change_gain[0].replace(" ", "").replace(",", "."))
            else:
                change_gain = 0
            if len(change_loss) >= 1:
                change_loss = float(change_loss[0].replace(" ", "").replace(",", "."))
            else:
                change_loss = 0

            if change_loss == 0 and change_gain == 0:
                print("ERRRRORRRRR")

            change = -change_loss + change_gain
            last = current - change

            self.calculated.append({
                'date_str': format_list[0],
                'date': dt,
                'timestamp': dt.timestamp(),
                'description': format_list[1],
                'descr': format_list[1][:40] + "..." if len(format_list[1]) > 43 else format_list[1],
                'change': change,
                'change%': change/last*100 if last != 0 else 100,
                'current': current,
                'before_change': last
            })
            current = last

        self.to_plot = list(reversed(self.calculated))
        pass

    def show(self):
        print(f"============= Account {self.account_number} ==============")
        for line in self.head:
            print(line)
        print("================================================")
        for line in self.calculated:
            print(line)

    def plot(self):
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
        print(f"{self.account_name} ({self.account_number})")
        print(f"Value for {datetime.fromtimestamp(x2[-1])} : {y_pred2[-1]}")
        plt.show()