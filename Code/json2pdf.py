import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Pfad des aktuellen Skripts
current_script_path = os.path.abspath(__file__)
# Übergeordnetes Verzeichnis
parentDirectory = os.path.dirname(os.path.dirname(current_script_path))
print("Übergeordnetes Verzeichnis:", parentDirectory)

jsonfl = os.path.join(parentDirectory,'questions_answers.json')
pdffl = os.path.join(parentDirectory,'questions_answers.pdf')


# JSON-Datei laden
with open(jsonfl, 'r', encoding='utf-8') as f:
    data = json.load(f)

# PDF-Datei erstellen
pdf = SimpleDocTemplate(pdffl, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Zusätzlicher Stil für Überschriften
header_style = ParagraphStyle('HeaderStyle', fontSize=14, leading=16, spaceAfter=10, textColor=colors.darkblue)

# JSON-Daten ohne Tabelle in PDF übertragen
for index, item in enumerate(data, start=1):
    # Überschrift
    elements.append(Paragraph(f"Eintrag {index}", header_style))
    
    # Inhalt als Absätze
    elements.append(Paragraph("<b>Context:</b> " + item["context"], styles["BodyText"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Question:</b> " + item["question"], styles["BodyText"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Answer:</b> " + item["answer"], styles["BodyText"]))
    elements.append(Spacer(1, 16))  # Abstand zwischen Einträgen

# PDF erstellen und speichern
pdf.build(elements)

print(f"Die PDF-Datei '{pdffl}' wurde erfolgreich erstellt.")