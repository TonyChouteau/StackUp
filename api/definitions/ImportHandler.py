import re

import sys
sys.path.append("./api")

from definitions.Line import Line
from definitions.Account import Account

class ImportHandler:

    def __init__(self):
        self.data = {}

    def add_file(self, file):
        with open("./assets/export_ca.csv", encoding="latin-1") as file:
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
            is_head = False
            for line in data:
                if len(line) != 0:
                    if "n°" in line:
                        account_number = line.split("n° ")[1].replace(";", "")
                    if re.match("[0-9]", line[0]) is None:
                        if is_head == False:
                            head_part = []
                            data_part = []
                            is_head = True
                        head_part.append(line)
                    else:
                        if is_head == True:
                            self.data[account_number] = Account(head_part, data_part)
                            is_head = False
                        data_part.append(line)
            
    def show(self):
        for account_number in self.data:
            self.data[account_number].show()