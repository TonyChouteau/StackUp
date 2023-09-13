import re
from datetime import datetime
import matplotlib.pyplot as plt

class Account:

    FORMAT_VALUE = "[0-9]{0,3} ?[0-9]{1,3},[0-9]{0,3}"

    def __init__(self, head, data):
        self.head = head
        self.data = data

        for line in self.head:
            if "n°" in line:
                self.account_number = line.split("n° ")[1].replace(";", "")
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
        pass

    def show(self):
        print(f"============= Account {self.account_number} ==============")
        for line in self.head:
            print(line)
        print("================================================")
        for line in self.calculated:
            print(line)

    def plot(self):
        x = [d.get('timestamp') for d in self.calculated]
        y = [d.get('current') for d in self.calculated]
        plt.plot(x, y)
        plt.plot(
            [self.calculated[0].get('timestamp'), self.calculated[-1].get('timestamp')],
            [0, 0]
        )
        plt.show()