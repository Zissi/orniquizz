#!/usr/bin/python

from PyQt4.QtGui import QApplication
from src.OrniquizzMainWindow import OrniquizzMainWindow


def main():
    import sys
    QApplication.setGraphicsSystem("raster")
    app = QApplication(sys.argv)
    app.setApplicationName('Orniquizz')
    app.setOrganizationName("Orni Corp.")
    
    wnd = OrniquizzMainWindow()
    wnd.show()
    app.exec_()

if __name__ == '__main__':
    main()
