import csv
import os
from datetime import datetime

class CSVConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_volksbank_csv(self):
        # Liest die Volksbank-CSV und gibt eine Liste von Dictionaries zurück
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Eingabedatei nicht gefunden: {self.input_file}")
        if not os.access(self.input_file, os.R_OK):
            raise PermissionError(f"Keine Leserechte für Datei: {self.input_file}")
        
        try:
            with open(self.input_file, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile, delimiter=';')
                data = list(reader)
                if not data:
                    raise ValueError("Die CSV-Datei ist leer oder enthält keine Daten")
                return data
        except UnicodeDecodeError:
            # Versuche mit anderer Kodierung
            with open(self.input_file, mode='r', encoding='latin-1') as infile:
                reader = csv.DictReader(infile, delimiter=';')
                data = list(reader)
                if not data:
                    raise ValueError("Die CSV-Datei ist leer oder enthält keine Daten")
                return data
        except Exception as e:
            raise Exception(f"Fehler beim Lesen der CSV-Datei: {str(e)}")

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
            
            # Extrahiere Werte mit Fallbacks
            buchungstag = row.get('Buchungstag') or row.get('Buchungsdatum') or ''
            valutadatum = row.get('Valutadatum') or row.get('Wertstellung') or ''
            buchungstext = row.get('Buchungstext') or ''
            name = row.get('Name Zahlungsbeteiligter') or ''
            iban = row.get('IBAN Zahlungsbeteiligter') or ''
            bic = row.get('BIC (SWIFT-Code) Zahlungsbeteiligter') or ''
            verwendungszweck = row.get('Verwendungszweck') or ''
            betrag = row.get('Betrag') or ''
            waehrung = row.get('Waehrung') or 'EUR'
            
            # Wenn Buchungstag leer ist, versuche Wertstellung zu verwenden
            if not buchungstag and valutadatum:
                buchungstag = valutadatum
            # Wenn Wertstellung leer ist, verwende Buchungstag
            if not valutadatum and buchungstag:
                valutadatum = buchungstag
            
            # Datumsformat ggf. anpassen
            def format_date(date_str):
                if not date_str:
                    return ''
                try:
                    # Versuche verschiedene Datumsformate
                    for fmt in ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y.%m.%d']:
                        try:
                            dt = datetime.strptime(date_str.strip(), fmt)
                            return dt.strftime('%d.%m.%Y')
                        except ValueError:
                            continue
                    # Wenn kein Format passt, gib Original zurück
                    return date_str
                except Exception:
                    return date_str
            
            buchungstag = format_date(buchungstag)
            valutadatum = format_date(valutadatum)
            
            # Betrag formatieren (Komma als Dezimaltrennzeichen)
            if betrag:
                # Entferne Leerzeichen und ersetze Punkt durch Komma
                betrag = str(betrag).strip().replace('.', ',')
                # Wenn kein Komma vorhanden ist, könnte es ein Integer sein
                if ',' not in betrag and '.' not in betrag:
                    # Behalte es als ist (kann später als Ganzzahl interpretiert werden)
                    pass
            else:
                betrag = '0,00'
            
            # Erstelle konvertierte Zeile - alle Felder müssen vorhanden sein
            converted_row = {
                'Buchungstag': buchungstag or '',
                'Wertstellung': valutadatum or '',
                'Umsatzart': buchungstext or '',
                'Auftraggeber/Empfänger': name or '',
                'IBAN': iban or '',
                'BIC': bic or '',
                'Verwendungszweck': verwendungszweck or '',
                'Betrag': betrag or '0,00',
                'Währung': waehrung or 'EUR',
            }
            
            # Nur hinzufügen, wenn mindestens Buchungstag oder Betrag vorhanden ist
            if converted_row['Buchungstag'] or converted_row['Betrag']:
                converted.append(converted_row)
        
        return lexoffice_fields, converted

    def write_lexoffice_csv(self, data):
        # Schreibt die konvertierten Daten ins Lexoffice-CSV-Format
        fields, rows = data
        # Stelle sicher, dass der Export-Ordner existiert
        output_dir = os.path.dirname(self.output_file)
        if output_dir:
            try:
                os.makedirs(output_dir, exist_ok=True)
                # Prüfe Schreibrechte
                if not os.access(output_dir, os.W_OK):
                    raise PermissionError(f"Keine Schreibrechte für Verzeichnis: {output_dir}")
            except Exception as e:
                raise Exception(f"Fehler beim Erstellen des Export-Verzeichnisses '{output_dir}': {str(e)}")
        
        try:
            with open(self.output_file, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fields, delimiter=';')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
        except PermissionError as e:
            raise Exception(f"Keine Schreibrechte für Datei '{self.output_file}': {str(e)}")
        except Exception as e:
            raise Exception(f"Fehler beim Schreiben der Datei '{self.output_file}': {str(e)}")

    def run(self):
        try:
            data = self.read_volksbank_csv()
            if not data:
                raise ValueError("Keine Daten zum Konvertieren gefunden")
            converted_data = self.convert_to_lexoffice_format(data)
            if not converted_data[1]:  # Keine konvertierten Zeilen
                raise ValueError("Keine Daten nach der Konvertierung vorhanden")
            self.write_lexoffice_csv(converted_data)
        except Exception as e:
            raise Exception(f"Fehler beim Konvertieren: {str(e)}")