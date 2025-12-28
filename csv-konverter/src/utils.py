def parse_csv(file_path):
    import pandas as pd
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

def validate_data(data):
    required_columns = ['Datum', 'Betrag', 'Verwendungszweck']  # Beispielspalten
    for column in required_columns:
        if column not in data.columns:
            print(f"Missing required column: {column}")
            return False
    return True

def format_output(data):
    formatted_data = data.rename(columns={
        'Datum': 'date',
        'Betrag': 'amount',
        'Verwendungszweck': 'description'
    })
    return formatted_data[['date', 'amount', 'description']]