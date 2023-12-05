import re

import sys
sys.path.append("./api")

from definitions.Line import Line
from definitions.Account import Account
from definitions.Total import Total

class ImportHandler:

    def __init__(self):
        self.data = {}

    def add_file(self, file):
        with open("./assets/CA20230913_232001.csv", encoding="latin-1") as file:
            lines = []
            for line in file.readlines():
                if line != "\n":
                    lines.append(line.replace("  ", ""))
            str_lines = "".join(lines).replace("\n\"", "\"")
            
            is_str = False
            data = []
            for line in str_lines.split("\n"):
                if is_str:
                    data[-1] = data[-1] + line
                else:
                    data.append(line)
                if line.count("\"") == 1:
                    is_str = not is_str

            head_part = []
            data_part = []
            account_number = ""
            is_head = True
            for line in data:
                if len(line) != 0:
                    if "n°" in line:
                        account_number = line.split("n° ")[1].replace(";", "")
                    if re.match("[0-9]", line[0]) is None:
                        if is_head == False:
                            self.data[account_number] = Account(head_part, data_part)
                            head_part = []
                            data_part = []
                            is_head = True
                        head_part.append(line)
                    else:
                        if is_head == True:
                            is_head = False
                        data_part.append(line)
            self.data[account_number] = Account(head_part, data_part)

            self.total = Total(self.data)
            
    def show(self):
        self.total.plot()
        self.total.plotly()