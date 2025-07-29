"""
Create a name plate from revolved text.
"""

from piecad import *

text_set_font("Roboto-Regular.ttf")

sz = 20
txt1 = text(20, "BRIAN")
txt2 = text(20, "STURGILL")

xu1, yu1, xu2, yu2 = txt1.bounding_box()
hu = yu2 - yu1
wu = xu2 - xu1

xl1, yl1, xl2, yl2 = txt2.bounding_box()
hl = yl2 - yl1
wl = xl2 - xl1

uoff = sz / 6
txt1 = txt1.translate([-xu1, hl - yu1 + uoff])
txt2 = txt2.translate([-xl1, -yl1])

if wu > wl:
    txt2 = txt2.translate([(wu - wl) / 2, 0])
else:
    txt1 = txt1.translate([(wl - wu) / 2, 0])


txt = union(txt1, txt2)

txt = txt.rotate(-90)

txt = revolve(txt, segments=100, revolve_degrees=65).rotate([90, 180 + 65, -90])

x1, y1, z1, x2, y2, z2 = txt.bounding_box()

bottom = rounded_rectangle([x2 - x1, y2 - y1]).extrude(2)

obj = union(txt.translate([0, 0, 2]), bottom)

if __name__ == "__main__":
    view(obj)
    save("/tmp/name_plate.obj", obj)
