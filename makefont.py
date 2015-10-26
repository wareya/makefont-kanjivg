#!/usr/bin/python

# ISC license

import re
import os
import fontforge
import codecs
font = fontforge.font()
font.encoding = "unicode"

print("Generating...")
for name in list(filter(lambda name: re.match("0....\.svg", name) , os.listdir())):
    glyph = font.createMappedChar("u"+name[1:5])
    glyph.importOutlines(name)
    glyph.correctDirection()
    glyph.removeOverlap()
print("Saving...")
font.generate('testfont.otf')
