from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import os
import sys
import csv
import subprocess
from converter import CSVConverter

# Basisverzeichnis im Home-Verzeichnis des Benutzers
HOME_DIR = os.path.expanduser("~")
CSVTOLEX_DIR = os.path.join(HOME_DIR, "csvtolex")
IMPORT_DIR = os.path.join(CSVTOLEX_DIR, "Import")
EXPORT_DIR = os.path.join(CSVTOLEX_DIR, "Export")

# Erstelle Verzeichnisse falls nicht vorhanden
os.makedirs(IMPORT_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

INPUT_PATH = os.path.join(IMPORT_DIR, "Umsaetze_DE36370601931091947001_2025.04.01.csv")
OUTPUT_PATH = os.path.join(EXPORT_DIR, "lexoffice_export.csv")

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
        file_path, _ = QFileDialog.getOpenFileName(self, "Importdatei auswählen", IMPORT_DIR, "CSV-Dateien (*.csv)")
        if file_path:
            self.input_path = file_path
            QMessageBox.information(self, "Datei gewählt", f"Importdatei gesetzt: {file_path}")

    def convert_file(self):
        if not os.path.exists(self.input_path):
            QMessageBox.warning(self, "Fehler", f"Eingabedatei nicht gefunden: {self.input_path}")
            return
        
        # Stelle sicher, dass der Export-Ordner existiert und schreibbar ist
        export_dir = os.path.dirname(self.output_path)
        if export_dir:
            try:
                os.makedirs(export_dir, exist_ok=True)
                # Prüfe Schreibrechte
                if not os.access(export_dir, os.W_OK):
                    QMessageBox.critical(self, "Berechtigungsfehler", 
                                       f"Keine Schreibrechte für Export-Verzeichnis:\n{export_dir}\n\n"
                                       f"Bitte stellen Sie sicher, dass Sie Schreibrechte für dieses Verzeichnis haben.")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Fehler", 
                                   f"Fehler beim Erstellen des Export-Verzeichnisses:\n{export_dir}\n\n"
                                   f"Fehler: {str(e)}")
                return
        
        try:
            converter = CSVConverter(self.input_path, self.output_path)
            converter.run()
            QMessageBox.information(self, "Fertig", 
                                  f"Konvertierung abgeschlossen!\n\n"
                                  f"Datei gespeichert in:\n{self.output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", 
                               f"Fehler bei der Konvertierung:\n\n{str(e)}\n\n"
                               f"Export-Pfad: {self.output_path}")

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
        # Stelle sicher, dass der Ordner existiert
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        try:
            # Versuche verschiedene Methoden je nach Betriebssystem
            import platform
            system = platform.system()
            if system == "Linux":
                subprocess.Popen(["xdg-open", folder])
            elif system == "Windows":
                subprocess.Popen(["explorer", folder])
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", folder])
            else:
                # Fallback: versuche xdg-open
                subprocess.Popen(["xdg-open", folder])
        except FileNotFoundError:
            QMessageBox.warning(self, "Fehler", 
                              f"Dateimanager konnte nicht geöffnet werden.\n\n"
                              f"Export-Ordner:\n{folder}")
        except Exception as e:
            QMessageBox.warning(self, "Fehler", 
                              f"Ordner konnte nicht geöffnet werden:\n{folder}\n\n"
                              f"Fehler: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
