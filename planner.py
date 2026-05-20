from datetime import date, datetime

def _days_until(exam_date_str):
    exam = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
    return (exam - date.today()).days


def compute_status(modules, logs):
    current_week = date.today().isocalendar()[1]
    result = []

    for module in modules:
        days_left = _days_until(module["exam_date"])
        start_week = module.get("start_week", current_week)
        weeks_tracked = max(current_week - start_week + 1, 1)

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

        sessions_per_week = len(module.get("sessions", []))
        deficit = max(sessions_per_week * weeks_tracked - attended, 0)

        # Wie viele Wochen bis zur Prüfung?
        weeks_left = max(days_left / 7, 0.5)
        # Wie groß ist der Rückstand relativ zu den verbleibenden Wochen?
        catchup_pressure = deficit / weeks_left

        score = (
            module["ects"]       * 1.0
            + module["difficulty"] * 1.5
            + catchup_pressure     * 10.0
            + (3.0 if review_needed else 0.0)
        )

        if days_left < 28 or (days_left < 56 and deficit > 3):
            priority = "DRINGEND"
        elif catchup_pressure > 1.0 or deficit > 3:
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
