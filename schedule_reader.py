import openpyxl
from datetime import date

DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


def _split_module_name(raw_name):
    """'Statistik / OR' → ['Statistik', 'OR']"""
    for sep in ["/", "&", "+"]:
        if sep in raw_name:
            return [p.strip() for p in raw_name.split(sep) if p.strip()]
    return [raw_name.strip()]


def read_schedule(path="Stundenplan.xlsx"):
    wb  = openpyxl.load_workbook(path)
    ws  = wb["Stundenplan"]

    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    col_modul = headers.index("Modul")
    col_ects  = headers.index("ECTS")
    col_exam  = next(i for i, h in enumerate(headers) if "Pruefung" in h)
    col_diff  = next(i for i, h in enumerate(headers) if "Schwierigkeit" in h)
    day_cols  = {day: headers.index(day) for day in DAYS if day in headers}

    today      = date.today()
    start_week = today.isocalendar()[1]

    # Aufgaben einlesen (optionales Sheet)
    tasks_by_module = _read_tasks(wb)

    module_map = {}  # name → module dict

    for row in ws.iter_rows(min_row=2, values_only=True):
        raw_name = row[col_modul]
        if not raw_name:
            continue

        names = _split_module_name(str(raw_name))

        # Sessions aus den Tag-Spalten
        sessions = []
        for day, col in day_cols.items():
            cell_val = str(row[col]).strip() if row[col] else ""
            if cell_val and cell_val != "None":
                for stype in [v.strip() for v in cell_val.split(",") if v.strip()]:
                    sessions.append({"type": stype, "day": day})

        for name in names:
            if name not in module_map:
                module_map[name] = {
                    "name":       name,
                    "ects":       int(row[col_ects] or 0),
                    "exam_date":  str(row[col_exam]).strip() if row[col_exam] else "",
                    "difficulty": int(row[col_diff] or 3),
                    "start_week": start_week,
                    "sessions":   [],
                    "tasks":      tasks_by_module.get(name, []),
                    "linked_to":  [n for n in names if n != name],
                }
            # Sessions hinzufügen (bei geteilten Modulen bekommen beide denselben Slot)
            module_map[name]["sessions"].extend(sessions)

    return list(module_map.values())


def _read_tasks(wb):
    if "Aufgaben" not in wb.sheetnames:
        return {}

    ws = wb["Aufgaben"]
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    try:
        col_modul    = headers.index("Modul")
        col_desc     = headers.index("Beschreibung")
        col_days     = next(i for i, h in enumerate(headers) if "Tage" in h)
        col_time     = headers.index("Uhrzeit")
        col_deadline = next(i for i, h in enumerate(headers) if "Deadline" in h)
        col_weekly   = next(i for i, h in enumerate(headers) if "oechentlich" in h)
    except (ValueError, StopIteration):
        return {}

    result = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[col_modul]:
            continue
        name = str(row[col_modul]).strip()
        task = {
            "description": str(row[col_desc]).strip()     if row[col_desc]     else "",
            "days":        [d.strip() for d in str(row[col_days]).split(",") if d.strip()] if row[col_days] else [],
            "time":        str(row[col_time]).strip()      if row[col_time]     else "",
            "deadline":    str(row[col_deadline]).strip()  if row[col_deadline] else "",
            "weekly":      str(row[col_weekly]).strip().lower() in ("ja", "yes", "1"),
        }
        result.setdefault(name, []).append(task)

    return result
