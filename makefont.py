#!/usr/bin/python

# ISC license

import re
import os
import fontforge

font = fontforge.font()

print("Generating...")
for name in list(filter(lambda name: re.match(".....\.svg", name) , os.listdir())):
    glyph = font.createChar(int(name[0:5], 16))
    print(name[0:5])
    glyph.importOutlines(name)
print("Saving...")

font.generate('testfont.otf')
