import csv
import json
import os

# Pfad des aktuellen Skripts
current_script_path = os.path.abspath(__file__)
# Übergeordnetes Verzeichnis
parentDirectory = os.path.dirname(os.path.dirname(current_script_path))
print("Übergeordnetes Verzeichnis:", parentDirectory)


# JSON-Datei lesen
csvfl = os.path.join(parentDirectory,'questions_answers.csv')
jsonfl = os.path.join(parentDirectory,'questions_answers.json')

with open(jsonfl, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# CSV-Datei erstellen
with open(csvfl, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Header hinzufügen
    csv_writer.writerow(['context', 'question', 'answer'])
    
    # Daten schreiben
    for entry in data:
        csv_writer.writerow([entry['context'], entry['question'], entry['answer']])

print(f"JSON Datei '{jsonfl}' wurde umgewandelt in '{csvfl}")