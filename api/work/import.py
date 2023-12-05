import sys
sys.path.append("./api")

from definitions.ImportHandler import ImportHandler

import_handler = ImportHandler()
import_handler.add_file("./assets/CA20231204_230638.csv")
# import_handler.add_file("./assets/CA20230901_164830.csv")
import_handler.show()
