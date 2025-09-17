# CSV-Konverter

Dieses Projekt ist ein CSV-Konverter, der speziell entwickelt wurde, um Volksbank-Exportdateien in das Lexoffice-Format zu konvertieren. 

## Inhaltsverzeichnis

- [Installation](#installation)
- [Benutzung](#benutzung)
- [Beispiele](#beispiele)
- [Abhängigkeiten](#abhängigkeiten)
- [Lizenz](#lizenz)

## Installation

Um das Projekt zu installieren, klonen Sie das Repository und installieren Sie die Abhängigkeiten mit pip:

```bash
git clone <repository-url>
cd csv-konverter
pip install -r requirements.txt
```

## Benutzung

Um den CSV-Konverter zu verwenden, importieren Sie die `CSVConverter`-Klasse aus `converter.py` und verwenden Sie die bereitgestellten Methoden, um die Volksbank-Exportdatei einzulesen und die konvertierten Daten zu speichern.

```python
from src.converter import CSVConverter

converter = CSVConverter()
converter.convert('input_volksbank.csv', 'output_lexoffice.csv')
```

## Beispiele

Hier sind einige Beispiele für die Verwendung des Konverters:

1. **Einfaches Beispiel**: Konvertieren einer Volksbank-Exportdatei in das Lexoffice-Format.
2. **Erweiterte Nutzung**: Anpassen der Konvertierungsparameter.

## Abhängigkeiten

Dieses Projekt verwendet die folgenden Abhängigkeiten:

- pandas

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.