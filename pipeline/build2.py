import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import ROOT, UPLOADS
import importlib.util, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

sys.path.insert(0, ROOT)
spec = importlib.util.spec_from_file_location("old", UPLOADS + "/build.py")
# reuse band definitions from the first version without re-running its build
src = open(UPLOADS + "/build.py").read().split("REGIONS = {")[0]
ns = {}; exec(src, ns)
ERAS, EXPLORE, CONFLICTS, TECH = ns["ERAS"], ns["EXPLORE"], ns["CONFLICTS"], ns["TECH"]

import data_us, data_eu, data_eu2, data_asia, data_africa, data_africa2, data_latam
REGIONS = [
    ("United States / North America", "1F4E79", "E3ECF6", data_us.E),
    ("Europe", "8B2E2A", "F6E2E0", [e for e in data_eu.E if e[0] < 1845] + data_eu2.E),
    ("Asia & Middle East", "9A6200", "FBEFD6", data_asia.E),
    ("Africa", "2E6B3F", "E1EFE4", [e for e in data_africa.E if e[0] < 1882] + data_africa2.E),
    ("Latin America & Caribbean", "6B3A7D", "EFE4F3", data_latam.E),
]

DECADES = list(range(1440, 2030, 10))
FIRST = 2
col = {d: i + FIRST for i, d in enumerate(DECADES)}
LAST = col[2020]
F = "Arial"
INK = "1E1E1E"

wb = Workbook()
ws = wb.active
ws.title = "Timeline"
ws.sheet_view.showGridLines = False
ws.sheet_view.zoomScale = 90

hair = Side(style="thin", color="D9D9D9")
century = Side(style="medium", color="7F7F7F")
def bord(c, left=None):
    return Border(left=left or hair, right=hair, top=hair, bottom=hair)

ws.column_dimensions["A"].width = 20
for d, c in col.items():
    ws.column_dimensions[get_column_letter(c)].width = 34

# Title banner
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=12)
t = ws.cell(1, 1, "WORLD HISTORY TIMELINE  ·  1444 → PRESENT")
t.font = Font(name="Georgia", size=22, bold=True, color=INK)
t.alignment = Alignment(vertical="center", indent=1)
ws.row_dimensions[1].height = 42
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=12)
s = ws.cell(2, 1, "Read down a column to see what was happening everywhere at once.  Hover over any event cell for Who · What · Where · When · Why · Historical significance.  Full detail on the 'Event Details' tab.")
s.font = Font(name=F, size=10, italic=True, color="595959")
s.alignment = Alignment(vertical="center", indent=1)
ws.row_dimensions[2].height = 22

HDR = 3
def label(r, text, color, size=10):
    c = ws.cell(r, 1, text)
    c.font = Font(name=F, bold=True, color="FFFFFF", size=size)
    c.fill = PatternFill("solid", fgColor=color)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = bord(c)

label(HDR, "DECADE", INK, 11)
for d, c in col.items():
    cell = ws.cell(HDR, c, f"{d}s")
    is_cent = d % 100 == 0
    cell.font = Font(name="Georgia", bold=True, color="FFFFFF", size=15 if is_cent else 12)
    cell.fill = PatternFill("solid", fgColor="000000" if is_cent else "3A3A3A")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = bord(cell, century if is_cent else None)
ws.row_dimensions[HDR].height = 30

def band(r, spans, default_fill, font_color, bold, size, height):
    for sp in spans:
        a, b, text = sp[0], sp[1], sp[2]
        fill = sp[3] if len(sp) > 3 else default_fill
        c1, c2 = col[a], col[b]
        for c in range(c1, c2 + 1):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=fill)
            ws.cell(r, c).border = Border(top=Side(style="thin", color="FFFFFF"), bottom=Side(style="thin", color="FFFFFF"),
                                          left=Side(style="medium", color="FFFFFF") if c == c1 else None,
                                          right=Side(style="medium", color="FFFFFF") if c == c2 else None)
        if c2 > c1:
            ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
        cell = ws.cell(r, c1, text)
        cell.font = Font(name=F, bold=bold, color=font_color, size=size)
        cell.alignment = Alignment(wrap_text=True, horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[r].height = height

label(4, "ERA", "404040"); band(4, ERAS, None, "FFFFFF", True, 13, 34)
label(5, "GLOBAL ORDER", "595959"); band(5, EXPLORE, None, INK, True, 10, 34)
label(6, "DEFINING\nCONFLICTS", "595959"); band(6, CONFLICTS, "ECECEC", INK, False, 10, 40)
label(7, "TECH & IDEAS", "595959"); band(7, TECH, "FFF4D6", "5A4300", False, 10, 34)

# spacer row
ws.row_dimensions[8].height = 8

details = []
r = 9
for name, dark, light, events in REGIONS:
    label(r, name.upper(), dark, 11)
    by_dec = {}
    for e in sorted(events, key=lambda x: x[0]):
        by_dec.setdefault(e[0] // 10 * 10, []).append(e)
    maxlines = 2
    for d, c in col.items():
        cell = ws.cell(r, c)
        evs = by_dec.get(d, [])
        cell.border = bord(cell, century if d % 100 == 0 else None)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if not evs:
            continue
        rt = CellRichText()
        lines = 0
        note = []
        for i, (yr, head, who, where, what, why, sig) in enumerate(evs):
            if i:
                rt.append(TextBlock(InlineFont(rFont=F, sz=10), "\n"))
            rt.append(TextBlock(InlineFont(rFont=F, sz=10, b=True, color=dark), f"{yr}  "))
            rt.append(TextBlock(InlineFont(rFont=F, sz=10, color=INK), head))
            lines += 1 + (len(head) + 6) // 36
            note.append(f"■ {yr} — {head.upper()}\nWHO: {who}\nWHAT: {what}\nWHERE: {where}\nWHEN: {yr}\nWHY: {why}\nSIGNIFICANCE: {sig}")
            details.append((yr, f"{d}s", name, head, who, what, where, why, sig))
        cell.value = rt
        cell.fill = PatternFill("solid", fgColor=light)
        cm = Comment("\n\n".join(note), "Timeline")
        cm.width = 420
        cm.height = min(130 * len(evs) + 40, 900)
        cell.comment = cm
        maxlines = max(maxlines, lines)
    ws.row_dimensions[r].height = min(14 * maxlines + 10, 409)
    r += 1

ws.freeze_panes = "B4"

# ---------- Event Details ----------
wd = wb.create_sheet("Event Details")
wd.sheet_view.showGridLines = False
cols = [("When", 8), ("Decade", 9), ("Region", 18), ("Event", 30), ("Who", 30), ("What happened", 42), ("Where", 22), ("Why it happened", 42), ("Historical significance", 50)]
for i, (h, w) in enumerate(cols, 1):
    c = wd.cell(1, i, h)
    c.font = Font(name=F, bold=True, color="FFFFFF", size=11)
    c.fill = PatternFill("solid", fgColor=INK)
    c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
    wd.column_dimensions[get_column_letter(i)].width = w
wd.row_dimensions[1].height = 28
regcolor = {n: (dk, lt) for n, dk, lt, _ in REGIONS}
order = {n: i for i, (n, *_ ) in enumerate(REGIONS)}
details.sort(key=lambda x: (x[0], order[x[2]]))
for i, row in enumerate(details, 2):
    dk, lt = regcolor[row[2]]
    for j, v in enumerate(row, 1):
        c = wd.cell(i, j, v)
        c.font = Font(name=F, size=10, color=INK, bold=(j in (1, 4)))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=hair)
        if j == 3:
            c.fill = PatternFill("solid", fgColor=dk)
            c.font = Font(name=F, size=9, bold=True, color="FFFFFF")
        elif j == 9:
            c.fill = PatternFill("solid", fgColor="FFF8E1")
        elif i % 2 == 0:
            c.fill = PatternFill("solid", fgColor="F7F7F7")
    longest = max(len(str(row[k])) / cols[k][1] for k in range(3, 9))
    wd.row_dimensions[i].height = max(28, 13 * (int(longest) + 1) + 4)
wd.freeze_panes = "E2"
wd.auto_filter.ref = f"A1:I{len(details)+1}"

out = ROOT + "/World_History_Timeline_1444-Present.xlsx"
wb.save(out)
print(len(details), "events")
