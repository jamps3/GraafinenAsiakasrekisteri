from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from main_window import MainWindow
from models import get_user


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kirjautuminen")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tervetuloa Asiakastilaus-tietojärjestelmään."))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tunnus")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Salasana")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Näytä salasana")
        self.show_password_checkbox.stateChanged.connect(
            self.toggle_password_visibility
        )
        layout.addWidget(self.show_password_checkbox)

        self.login_button = QPushButton("Kirjaudu")
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:  # Tarkistetaan, onko Enteriä painettu
            self.login_button.click()  # Aktivoi kirjautumispainike
        super().keyPressEvent(event)

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if get_user(username, password):
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Virhe", "Väärä tunnus tai salasana.")
