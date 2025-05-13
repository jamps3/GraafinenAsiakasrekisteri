from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QCheckBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
import bcrypt
import pymysql


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asiakastilaus - Kirjautuminen")
        self.setGeometry(200, 200, 400, 200)
        self.init_ui()

    def init_ui(self):
        self.label_title = QLabel("Tervetuloa Asiakastilaus-tietojärjestelmään.")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_user = QLabel("Tunnus:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Salasana:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_pass = QCheckBox("Näytä salasana")
        self.show_pass.stateChanged.connect(self.toggle_password)

        self.login_button = QPushButton("Kirjaudu")
        self.login_button.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.show_pass)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def toggle_password(self):
        if self.show_pass.isChecked():
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

    def check_login(self):
        user = self.input_user.text()
        password = self.input_pass.text()

        try:
            connection = pymysql.connect(
                host="your-db-hostname",
                user="your-db-user",
                password="your-db-password",
                database="Asiakastilaus",
            )
            cursor = connection.cursor()
            cursor.execute(
                "SELECT SALASANA_HASH FROM KAYTTAJA WHERE TUNNUS = %s", (user,)
            )
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode(), result[0].encode()):
                QMessageBox.information(self, "Onnistui", "Kirjautuminen onnistui.")
                # TODO: Avaa pääkäyttöliittymä (main_window.py)
            else:
                QMessageBox.warning(self, "Virhe", "Väärä tunnus tai salasana.")

            cursor.close()
            connection.close()
        except Exception as e:
            QMessageBox.critical(self, "Virhe", f"Yhteysvirhe: {e}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
