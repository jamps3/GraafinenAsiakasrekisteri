from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from utils import get_connection  # <-- Käytetään utils.py:n tietokantayhteyttä


class AsiakasrekisteriWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asiakasrekisteri")
        self.init_ui()
        self.load_data()

    def init_ui(self):
        # Syöttökentät
        self.input_id = QLineEdit()
        self.input_etunimi = QLineEdit()
        self.input_sukunimi = QLineEdit()
        self.input_yritys = QLineEdit()

        self.input_id.setPlaceholderText("Asiakasnumero")
        self.input_etunimi.setPlaceholderText("Etunimi")
        self.input_sukunimi.setPlaceholderText("Sukunimi")
        self.input_yritys.setPlaceholderText("Yritys")

        # Napit
        self.btn_add = QPushButton("Uusi")
        self.btn_update = QPushButton("Päivitä")
        self.btn_delete = QPushButton("Poista")

        self.btn_add.clicked.connect(self.add_customer)
        self.btn_update.clicked.connect(self.update_customer)
        self.btn_delete.clicked.connect(self.delete_customer)

        # Taulukko
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Asiakasnumero", "Etunimi", "Sukunimi", "Yritys"]
        )
        self.table.cellClicked.connect(self.fill_form)

        # SQL-komennon näyttäminen
        self.sql_command_label = QLabel("Viimeisin SQL-komento: ")

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.input_id)
        form_layout.addWidget(self.input_etunimi)
        form_layout.addWidget(self.input_sukunimi)
        form_layout.addWidget(self.input_yritys)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_delete)
        form_layout.addLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.sql_command_label)

        self.setLayout(main_layout)

    def get_connection(self):
        return get_connection()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ASIAKAS")
            for row_num, row_data in enumerate(cursor.fetchall()):
                self.table.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
            cursor.close()
            conn.close()
            # Muutetaan sarakkeet automaattisesti sopiviksi sisällön mukaan
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Virhe", f"Tietojen lataus epäonnistui:\n{e}")

    def fill_form(self, row, _):
        self.input_id.setText(self.table.item(row, 0).text())
        self.input_etunimi.setText(self.table.item(row, 1).text())
        self.input_sukunimi.setText(self.table.item(row, 2).text())
        self.input_yritys.setText(self.table.item(row, 3).text())

    def update_customer(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql_query = """
                UPDATE ASIAKAS SET ETUNIMI=%s, SUKUNIMI=%s, YRITYS=%s WHERE ASIAKASNUMERO=%s
            """
            cursor.execute(
                sql_query,
                (
                    self.input_etunimi.text(),
                    self.input_sukunimi.text(),
                    self.input_yritys.text(),
                    self.input_id.text(),
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.sql_command_label.setText(
                f"Viimeisin SQL-komento: {sql_query}"
            )  # Päivitetään SQL-komento
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Virhe", f"Asiakkaan päivitys epäonnistui:\n{e}")

    def add_customer(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql_query = """
                INSERT INTO ASIAKAS (ETUNIMI, SUKUNIMI, YRITYS) VALUES (%s, %s, %s)
            """
            cursor.execute(
                sql_query,
                (
                    self.input_etunimi.text(),
                    self.input_sukunimi.text(),
                    self.input_yritys.text(),
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.sql_command_label.setText(
                f"Viimeisin SQL-komento: {sql_query}"
            )  # Päivitetään SQL-komento
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Virhe", f"Asiakkaan lisäys epäonnistui:\n{e}")

    def delete_customer(self):
        # Kysy vahvistusta poiston suorittamiseen
        reply = QMessageBox.question(
            self,
            "Vahvista poisto",
            "Oletko varma, että haluat poistaa tämän asiakkaan?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        # Jos käyttäjä valitsee "Yes"
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                sql_query = "DELETE FROM ASIAKAS WHERE ASIAKASNUMERO=%s"
                cursor.execute(sql_query, (self.input_id.text(),))
                conn.commit()
                cursor.close()
                conn.close()
                self.sql_command_label.setText(
                    f"Viimeisin SQL-komento: {sql_query}"
                )  # Päivitetään SQL-komento
                self.load_data()
            except Exception as e:
                QMessageBox.critical(
                    self, "Virhe", f"Asiakkaan poisto epäonnistui:\n{e}"
                )
