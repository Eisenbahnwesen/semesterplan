"""Erstellt Stundenplan.xlsx mit Stundenplan- und Aufgaben-Sheet."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

thin   = Side(style="thin", color="AAAAAA")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def header_cell(ws, row, col, value, bg="2E4057"):
    cell = ws.cell(row=row, column=col, value=value)
    cell.font      = Font(color="FFFFFF", bold=True)
    cell.fill      = PatternFill("solid", fgColor=bg)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border    = border
    return cell

def data_cell(ws, row, col, value=""):
    cell = ws.cell(row=row, column=col, value=value)
    cell.fill      = PatternFill("solid", fgColor="F0F4F8")
    cell.alignment = Alignment(horizontal="center")
    cell.border    = border
    return cell

wb = openpyxl.Workbook()

# ── Sheet 1: Stundenplan ─────────────────────────────────────────────────────
ws1 = wb.active
ws1.title = "Stundenplan"

headers1 = ["Modul", "ECTS", "Pruefung (YYYY-MM-DD)", "Schwierigkeit (1-5)"] + DAYS
for col, h in enumerate(headers1, 1):
    bg = "048A81" if h in DAYS else "2E4057"
    header_cell(ws1, 1, col, h, bg)

examples1 = [
    ["Statistik",            5, "2026-07-23", 4, "VL",      "",   "GUe",     "",    ""   ],
    ["Operations Research",  5, "2026-07-23", 3, "VL",      "",   "",        "GUe", ""   ],
    ["Statistik / OR",       5, "2026-07-23", 4, "VL",      "",   "",        "",    ""   ],
    ["Fertigungstechnik",    4, "2026-08-03", 3, "",        "VL", "",        "",    "GUe"],
]
for r, row in enumerate(examples1, 2):
    for c, val in enumerate(row, 1):
        data_cell(ws1, r, c, val)

ws1.column_dimensions["A"].width = 26
ws1.column_dimensions["B"].width = 6
ws1.column_dimensions["C"].width = 20
ws1.column_dimensions["D"].width = 18
for col in ["E","F","G","H","I"]:
    ws1.column_dimensions[col].width = 13
ws1.row_dimensions[1].height = 30

# Hinweis-Zelle
note = ws1.cell(row=len(examples1)+3, column=1,
    value="Tipp: '/' im Modulnamen = zwei Module teilen den Slot (z.B. 'Statistik / OR')")
note.font = Font(italic=True, color="888888")

# ── Sheet 2: Aufgaben ────────────────────────────────────────────────────────
ws2 = wb.create_sheet("Aufgaben")

headers2 = ["Modul", "Beschreibung", "Tage (kommagetrennt)", "Uhrzeit", "Deadline-Tag", "Woechentlich (ja/nein)"]
for col, h in enumerate(headers2, 1):
    header_cell(ws2, 1, col, h)

examples2 = [
    ["Statistik",           "Online-Uebungsaufgaben",    "",                  "",      "Freitag",  "ja"],
    ["Statistik",           "Mini-Test",                 "Montag,Mittwoch",   "11:30", "",         "ja"],
    ["Operations Research", "Hausaufgaben abgeben",      "",                  "",      "Donnerstag","ja"],
]
for r, row in enumerate(examples2, 2):
    for c, val in enumerate(row, 1):
        data_cell(ws2, r, c, val)

col_widths2 = [22, 28, 24, 10, 14, 22]
for i, w in enumerate(col_widths2, 1):
    ws2.column_dimensions[chr(64+i)].width = w
ws2.row_dimensions[1].height = 30

wb.save("Stundenplan.xlsx")
print("Stundenplan.xlsx erstellt (2 Sheets: Stundenplan + Aufgaben).")
