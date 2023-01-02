import json
import csv
import os
import datetime
import textwrap

def convert_pixels_json_to_moodistory_csv(json_file_path, time):
    # Open the input JSON file and read the data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(f'Error: Unable to open or parse file {json_file_path}')
        return

    # Create a new list of rows for the output CSV file
    rows = [['date', 'time', 'mood', 'notesAndThoughts']]

    # Convert each day's data to a row in the CSV file
    for day in data:
        date = day['date']
        mood = None
        notes_and_thoughts = ''

        for entry in day['entries']:
            if entry['type'] == 'Mood':
                mood = entry['value']
            if 'notes' in entry:
                notes_and_thoughts = textwrap.dedent(entry['notes']).strip()

        # Add a row to the output CSV file if a mood was recorded for this day
        if mood is not None:
            rows.append([date, time, mood, notes_and_thoughts])

    # Determine the delimiter based on the file extension of the input file
    delimiter = ',' if json_file_path.endswith('.json') else ';'

    # Create the output CSV file and write the data to it
    csv_file_path = os.path.splitext(json_file_path)[0] + '.csv'
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(rows)
    except OSError:
        print(f'Error: Unable to create file {csv_file_path}')
        return

    # Print a success message
    print(f'Successfully converted {json_file_path} to {csv_file_path}')

# Prompt the user to enter the file path to the JSON file and the default time for the entries
json_file_path = input('Enter the file path to the JSON file: ')
time = input('Enter the default time for the entries in the format HH:MM:SS: ')

# Validate the time format
try:
    datetime.datetime.strptime(time, '%H:%M:%S')
except ValueError:
    print('Error: Invalid time format')
    exit()

# Convert the JSON file to a CSV file
convert_pixels_json_to_moodistory_csv(json_file_path, time)
