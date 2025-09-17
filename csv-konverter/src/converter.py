import csv
from datetime import datetime

class CSVConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_volksbank_csv(self):
        # Liest die Volksbank-CSV und gibt eine Liste von Dictionaries zurück
        with open(self.input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            return list(reader)

    def convert_to_lexoffice_format(self, data):
        # Erwartete Lexoffice-Spalten
        lexoffice_fields = [
            'Buchungstag', 'Wertstellung', 'Umsatzart', 'Auftraggeber/Empfänger',
            'IBAN', 'BIC', 'Verwendungszweck', 'Betrag', 'Währung'
        ]
        converted = []
        for row in data:
            # Zeilen mit "Abschluss" im Buchungstext überspringen
            if 'Abschluss' in (row.get('Buchungstext') or ''):
                continue
            converted_row = {
                'Buchungstag': row.get('Buchungstag') or row.get('Buchungstag') or row.get('Buchungsdatum') or row.get('Buchungstag'),
                'Wertstellung': row.get('Valutadatum') or row.get('Wertstellung'),
                'Umsatzart': row.get('Buchungstext'),
                'Auftraggeber/Empfänger': row.get('Name Zahlungsbeteiligter'),
                'IBAN': row.get('IBAN Zahlungsbeteiligter'),
                'BIC': row.get('BIC (SWIFT-Code) Zahlungsbeteiligter'),
                'Verwendungszweck': row.get('Verwendungszweck'),
                'Betrag': row.get('Betrag'),
                'Währung': row.get('Waehrung') or 'EUR',
            }
            # Datumsformat ggf. anpassen
            for key in ['Buchungstag', 'Wertstellung']:
                if converted_row[key]:
                    try:
                        dt = datetime.strptime(converted_row[key], '%d.%m.%Y')
                        converted_row[key] = dt.strftime('%d.%m.%Y')
                    except Exception:
                        pass
            # Betrag ggf. ins richtige Format bringen (Komma als Dezimaltrennzeichen)
            if converted_row['Betrag']:
                converted_row['Betrag'] = str(converted_row['Betrag']).replace('.', ',')
            converted.append(converted_row)
        return lexoffice_fields, converted

    def write_lexoffice_csv(self, data):
        # Schreibt die konvertierten Daten ins Lexoffice-CSV-Format
        fields, rows = data
        with open(self.output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fields, delimiter=';')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def run(self):
        data = self.read_volksbank_csv()
        converted_data = self.convert_to_lexoffice_format(data)
        self.write_lexoffice_csv(converted_data)