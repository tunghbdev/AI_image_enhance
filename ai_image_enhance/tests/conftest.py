import sys, os, pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app
