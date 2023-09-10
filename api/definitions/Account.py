import re

class Account:

    def __init__(self, head, data):
        self.head = head
        self.data = data

        for line in self.head:
            if "n°" in line:
                self.account_number = line.split("n° ")[1].replace(";", "")
            if "Solde" in line:
                final_value = re.findall(" [0-9]{0,3} ?[0-9]{1,3},[0-9]{0,3}", line.replace("\xa0", " "))
                if len(final_value) >= 1:
                    self.final_value = float(final_value[0].replace(" ", "").replace(",", "."))
                else:
                    self.final_value = 0
                    
        # print(self.head)
        print(self.account_number, self.final_value)

    def show(self):
        print(f"============= Account {self.account_number} ==============")
        for line in self.head:
            print(line)
        print("================================================")
        for line in self.data:
            print(line)
