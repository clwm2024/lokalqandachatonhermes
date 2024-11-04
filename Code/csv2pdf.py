import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Pfad des aktuellen Skripts
current_script_path = os.path.abspath(__file__)
# Übergeordnetes Verzeichnis
parentDirectory = os.path.dirname(os.path.dirname(current_script_path))
print("Übergeordnetes Verzeichnis:", parentDirectory)


# PDF-Datei erstellen
#pdffl = "questions_answers.pdf"
pdffl = os.path.join(parentDirectory,'questions_answers.pdf')
csvfl = os.path.join(parentDirectory,'questions_answers.csv')

pdf = canvas.Canvas(pdffl, pagesize=A4)
width, height = A4
pdf.setFont("Helvetica", 10)

# CSV-Datei lesen und in PDF schreiben
y_position = height - 40
with open(csvfl, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        text = ' | '.join(row)
        pdf.drawString(40, y_position, text)
        y_position -= 15  # Abstand zwischen den Zeilen
        # Neue Seite bei Bedarf
        if y_position < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = height - 40

pdf.save()

print(f"CSV Datei '{csvfl}' wurde umgewandelt in '{pdffl}")
