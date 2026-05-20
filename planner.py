from datetime import date, datetime

SEMESTER_START_WEEK = 15  # KW 15 = Semesterstart


def _days_until(exam_date_str):
    exam = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
    return (exam - date.today()).days


def _weeks_elapsed():
    current_week = date.today().isocalendar()[1]
    return max(current_week - SEMESTER_START_WEEK + 1, 1)


def compute_status(modules, logs):
    weeks = _weeks_elapsed()
    result = []

    for module in modules:
        days_left = _days_until(module["exam_date"])

        attended = sum(
            len(log["attended"])
            for log in logs
            if log["module"] == module["name"]
        )
        review_needed = any(
            log["review_needed"]
            for log in logs
            if log["module"] == module["name"]
        )

        sessions_per_week = sum(st["per_week"] for st in module["session_types"])
        deficit = max(sessions_per_week * weeks - attended, 0)

        urgency = 100 / days_left if days_left > 0 else 10.0
        score = (
            module["ects"]       * 1.5
            + module["difficulty"] * 2.0
            + deficit              * 3.0
            + urgency              * 10.0
            + (5.0 if review_needed else 0.0)
        )

        if days_left < 14 or score > 40:
            priority = "DRINGEND"
        elif deficit > 2 or score > 20:
            priority = "ZURUECKGEFALLEN"
        else:
            priority = "IM PLAN"

        if priority == "DRINGEND":
            recommendation = "Sofort aufholen – Pruefung naht!"
        elif review_needed:
            recommendation = "Wiederholung einplanen"
        elif deficit > 0:
            recommendation = f"{deficit} verpasste Session(s) nachholen"
        else:
            recommendation = "Weiter so"

        result.append({
            "name":           module["name"],
            "priority":       priority,
            "days_until_exam": days_left,
            "score":          score,
            "recommendation": recommendation,
        })

    return sorted(result, key=lambda x: x["score"], reverse=True)


def show_status(status):
    print("\n========== STATUS UPDATE ==========")
    for s in status:
        print(f"[{s['priority']}] {s['name']}  (Pruefung in {s['days_until_exam']} Tagen)")
        print(f"  -> {s['recommendation']}\n")
    print("===================================")
