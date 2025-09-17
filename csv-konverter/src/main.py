from converter import CSVConverter

if __name__ == "__main__":
    input_path = "Import/Umsaetze_DE36370601931091947001_2025.04.01.csv"
    output_path = "Export/lexoffice_export.csv"
    converter = CSVConverter(input_path, output_path)
    converter.run()
    print("Konvertierung abgeschlossen. Die Datei liegt in Export/lexoffice_export.csv")
