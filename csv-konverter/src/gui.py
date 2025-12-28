from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import os
import sys
import csv
import subprocess
from converter import CSVConverter

# Basisverzeichnis immer relativ zur ausführbaren Datei
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT_PATH = os.path.join(BASE_DIR, "Import/Umsaetze.csv fehlgeschlagen")
OUTPUT_PATH = os.path.join(BASE_DIR, "Export/lexoffice_export.csv")
EXPORT_DIR = os.path.join(BASE_DIR, "Export")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV zu Lexoffice Konverter")
        self.setGeometry(200, 200, 1000, 600)
        main_layout = QVBoxLayout()

        # Button-Leiste oben
        button_layout = QHBoxLayout()

        self.import_btn = QPushButton("Datei importieren")
        self.import_btn.clicked.connect(self.import_file)
        button_layout.addWidget(self.import_btn, alignment=Qt.AlignLeft)

        self.convert_btn = QPushButton("Konvertieren")
        self.convert_btn.clicked.connect(self.convert_file)
        button_layout.addWidget(self.convert_btn, alignment=Qt.AlignLeft)

        self.show_btn = QPushButton("Datei anzeigen")
        self.show_btn.clicked.connect(self.show_file)
        button_layout.addWidget(self.show_btn, alignment=Qt.AlignRight)

        self.save_btn = QPushButton("Speichern")
        self.save_btn.clicked.connect(self.save_table)
        button_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)

        self.export_folder_btn = QPushButton("Export-Ordner öffnen")
        self.export_folder_btn.clicked.connect(self.open_export_folder)
        button_layout.addWidget(self.export_folder_btn, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.input_path = INPUT_PATH
        self.output_path = OUTPUT_PATH
        self.header = []

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Importdatei auswählen", "Import", "CSV-Dateien (*.csv)")
        if file_path:
            self.input_path = file_path
            QMessageBox.information(self, "Datei gewählt", f"Importdatei gesetzt: {file_path}")

    def convert_file(self):
        if not os.path.exists(self.input_path):
            QMessageBox.warning(self, "Fehler", f"Eingabedatei nicht gefunden: {self.input_path}")
            return
        converter = CSVConverter(self.input_path, self.output_path)
        converter.run()
        QMessageBox.information(self, "Fertig", "Konvertierung abgeschlossen!")

    def show_file(self):
        if not os.path.exists(self.output_path):
            QMessageBox.warning(self, "Fehler", f"Exportdatei nicht gefunden: {self.output_path}")
            return
        with open(self.output_path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            rows = list(reader)
        if not rows:
            self.table.clear()
            return
        self.header = rows[0]
        self.table.setRowCount(len(rows)-1)
        self.table.setColumnCount(len(rows[0]))
        self.table.setHorizontalHeaderLabels(rows[0])
        white = QColor(Qt.white)
        black = QColor(Qt.black)
        for i, row in enumerate(rows[1:]):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                item.setBackground(white)
                item.setForeground(black)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def save_table(self):
        if not self.header or self.table.rowCount() == 0:
            QMessageBox.warning(self, "Fehler", "Keine Daten zum Speichern vorhanden.")
            return
        with open(self.output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(self.header)
            for row in range(self.table.rowCount()):
                rowdata = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    rowdata.append(item.text() if item else "")
                writer.writerow(rowdata)
        QMessageBox.information(self, "Gespeichert", f"Tabelle wurde gespeichert: {self.output_path}")

    def open_export_folder(self):
        folder = EXPORT_DIR
        try:
            if sys.platform.startswith("win"):
                os.startfile(folder)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Ordner konnte nicht geöffnet werden: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
