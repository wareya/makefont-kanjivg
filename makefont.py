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
    glyph.round()
    glyph.removeOverlap()
    # The only purpose of rounding up above is to avoid bugs in "removeOverlap".
    glyph.simplify(2,("smoothcurves", "mergelines", "setstarttoextremum","removesingletonpoints"))
    # Simplifying might take care of any extra, minor errors (such as overlapping points).
    glyph.removeOverlap()
    # We removeoverlap again just to be safe.
print("Saving...")
font.generate('testfont.otf')
