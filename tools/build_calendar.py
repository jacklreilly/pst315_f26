"""Generate pst315_schedule.ics - the subscribable course calendar.

Class sessions become timed events on Tuesdays during class time; assignment
deadlines become all-day events on the day they are due. Re-run after changing
the schedule or any due date, then re-render the site.
"""
import os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.abspath(os.path.join(HERE, "..", "pst315_schedule.ics"))

DOMAIN   = "jacklreilly.github.io"
SITE     = f"https://{DOMAIN}/pst315_f26"
TZ       = "America/New_York"
CLASS_START, CLASS_END = "153000", "181500"      # Tuesdays 3:30-6:15 PM
LOCATION = "HB Crouse Hall, Kittredge Auditorium"
# Fixed so regenerating an unchanged schedule produces an identical file.
DTSTAMP  = "20260820T000000Z"

# (week, Tuesday, topic, meets?)
CLASSES = [
    (1,  date(2026, 8, 25), "Course Intro",           True),
    (2,  date(2026, 9,  1), "Working With Clients",   True),
    (3,  date(2026, 9,  8), "No Class (Client Meeting Week)", False),
    (4,  date(2026, 9, 15), "Individual Meetings",    True),
    (5,  date(2026, 9, 22), "Data & Surveys",         True),
    (6,  date(2026, 9, 29), "Excel & Coding",         True),
    (7,  date(2026,10,  6), "Graphing & Methods",     True),
    (8,  date(2026,10, 13), "No Class (Fall Break)",  False),
    (9,  date(2026,10, 20), "Individual Meetings",    True),
    (10, date(2026,10, 27), "Work Time",              True),
    (11, date(2026,11,  3), "Professional Materials", True),
    (12, date(2026,11, 10), "Individual Meetings",    True),
    (13, date(2026,11, 17), "Presenting Your Work",   True),
    (14, date(2026,12,  1), "Student Presentations",  True),
    (15, date(2026,12,  8), "Wrap-Up",                True),
]

# (due date, assignment, page slug)
DUE = [
    (date(2026, 8, 28), "Project Application",           "01-project-application"),
    (date(2026, 9,  4), "Client Email",                  "02-client-email"),
    (date(2026, 9, 11), "First Client Meeting",          "03-first-client-meeting"),
    (date(2026, 9, 18), "Finalized Contract & Timeline", "04-contract-timeline"),
    (date(2026, 9, 18), "Second Client Meeting",         "05-second-client-meeting"),
    (date(2026, 9, 25), "Organizational Assessment",     "06-organizational-assessment"),
    (date(2026, 9, 25), "Weekly Task Plan",              "07-weekly-task-plan"),
    (date(2026,10,  2), "Draft Executive Summary",       "08-draft-executive-summary"),
    (date(2026,10,  2), "Excel Coding Workshop",         "09-excel-coding-workshop"),
    (date(2026,10,  9), "Excel Graphing Workshop",       "10-excel-graphing-workshop"),
    (date(2026,10, 16), "Practice Report",               "11-practice-report"),
    (date(2026,10, 23), "Formatted Report Shell",        "12-formatted-report-shell"),
    (date(2026,11,  6), "Rough Draft",                   "13-rough-draft"),
    (date(2026,11, 20), "Final Report",                  "14-final-report"),
    # emailed to your UCA by Monday night, not the Friday
    (date(2026,11, 30), "Final Presentation",            "15-final-presentation"),
    (date(2026,12, 11), "Professional Materials",        "16-professional-materials"),
    (date(2026,12, 11), "Final Reflection",              "17-final-reflection"),
]

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE"""

def esc(s):
    return s.replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")

def fold(line):
    """iCalendar limits lines to 75 octets; continuations start with a space."""
    out, cur = [], line
    while len(cur.encode("utf8")) > 75:
        cut = 74
        while len(cur[:cut].encode("utf8")) > 75: cut -= 1
        out.append(cur[:cut]); cur = " " + cur[cut:]
    out.append(cur)
    return out

def event(uid, summary, description, *, start=None, end=None, day=None, location=None):
    L = ["BEGIN:VEVENT", f"UID:{uid}@{DOMAIN}", f"DTSTAMP:{DTSTAMP}"]
    if day is not None:
        L.append(f"DTSTART;VALUE=DATE:{day:%Y%m%d}")
        L.append(f"DTEND;VALUE=DATE:{day + timedelta(days=1):%Y%m%d}")
        L.append("X-MICROSOFT-CDO-ALLDAYEVENT:TRUE")
        L.append("TRANSP:TRANSPARENT")          # all-day items should not show as busy
    else:
        L.append(f"DTSTART;TZID={TZ}:{start}")
        L.append(f"DTEND;TZID={TZ}:{end}")
        L.append("TRANSP:OPAQUE")
    L.append(f"SUMMARY:{esc(summary)}")
    if description: L.append(f"DESCRIPTION:{esc(description)}")
    if location:    L.append(f"LOCATION:{esc(location)}")
    L.append("SEQUENCE:0")
    L.append("END:VEVENT")
    return L

lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
         "PRODID:-//Jack Reilly//PST 315 Course Schedule//EN",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         "X-WR-CALNAME:PST 315", "X-WR-TIMEZONE:America/New_York",
         "X-WR-CALDESC:PST 315 Methods of Policy Analysis and Presentation - class sessions and assignment deadlines"]
lines += VTIMEZONE.split("\n")

for wk, d, topic, meets in CLASSES:
    uid = f"pst315-class-{d:%Y%m%d}"
    desc = f"Week {wk}. Course schedule: {SITE}/logistics.html#course-schedule"
    if meets:
        lines += event(uid, f"PST 315: {topic}", desc,
                       start=f"{d:%Y%m%d}T{CLASS_START}", end=f"{d:%Y%m%d}T{CLASS_END}",
                       location=LOCATION)
    else:
        lines += event(uid, f"PST 315: {topic}", desc, day=d)

for d, name, slug in DUE:
    lines += event(f"pst315-due-{d:%Y%m%d}-{slug}",
                   f"PST 315 Due: {name}",
                   f"Assignment details: {SITE}/assignments/{slug}.html",
                   day=d)

lines.append("END:VCALENDAR")

folded = []
for ln in lines: folded += fold(ln)
with open(OUT, "w", newline="") as f:
    f.write("\r\n".join(folded) + "\r\n")

n_class = sum(1 for c in CLASSES if c[3]); n_noclass = len(CLASSES) - n_class
print(f"  wrote {os.path.basename(OUT)}")
print(f"    {n_class} timed class sessions, {n_noclass} all-day 'no class' notices, "
      f"{len(DUE)} all-day deadlines = {len(CLASSES) + len(DUE)} events")
