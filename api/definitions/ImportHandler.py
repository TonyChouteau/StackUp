import sys
sys.path.append("./api")

from definitions.Line import Line

class ImportHandler:

    def __init__(self):
        pass

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

            self.data = data
            
    def head(self):
        for data in self.data[:20]:
            print(data)

    def show(self):
        for data in self.data:
            print(data)