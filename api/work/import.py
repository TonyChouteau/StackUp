import sys
sys.path.append("./api")

from definitions.ImportHandler import ImportHandler

import_handler = ImportHandler()
import_handler.add_file("./assets/export_ca.csv")
import_handler.show()
