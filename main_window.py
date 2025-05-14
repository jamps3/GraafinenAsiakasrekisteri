from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu
from PyQt6.QtGui import QAction
from asiakasrekisteri import AsiakasrekisteriWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graafinen Asiakasrekisteri")
        self.setGeometry(100, 100, 1024, 768)

        # Keskitetään ikkuna näytölle
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

        menubar = self.menuBar()
        rekisterit_menu = menubar.addMenu("Rekisterit")

        asiakasrekisteri_action = QAction("Asiakasrekisteri", self)
        asiakasrekisteri_action.triggered.connect(self.open_asiakasrekisteri)

        rekisterit_menu.addAction(asiakasrekisteri_action)

        self.init_ui()

    def init_ui(self):
        # Asiakasrekisterin näyttäminen suoraan
        self.asiakasrekisteri_widget = AsiakasrekisteriWidget()

        # Asetetaan asiakasrekisteri pääikkunaksi
        self.setCentralWidget(self.asiakasrekisteri_widget)

        # Voit lisätä muita elementtejä tänne myöhemmin

    def open_asiakasrekisteri(self):
        self.asiakasrekisteri_widget = AsiakasrekisteriWidget()
        self.setCentralWidget(self.asiakasrekisteri_widget)
