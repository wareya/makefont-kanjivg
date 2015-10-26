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
    # We simplify before doing anything in order to avoid "The curve is too short." from "removeOverlap"
    # Simplify can cause unrounded points, which will cause bugs in removeOverlap.
    # We need to round before removeOverlap anyways, but we also need to round after simplify.
    # Therefore, simplify is first.
    glyph.simplify(1,("smoothcurves", "mergelines", "setstarttoextremum","removesingletonpoints"))
    glyph.round()
    glyph.removeOverlap()
    # removeOverlap can and will cause very short paths to occur, and can cause nearly-same-location points.
    # We need to simplify to remove them.
    # However, we need to round after simplifying. 
    # However, the last instruction done to a glyph aught to be "removeOverlap".
    # ... Therefore, we essentially need to duplicate the above code again.
    glyph.simplify(2,("smoothcurves", "mergelines", "setstarttoextremum","removesingletonpoints"))
    glyph.round()
    glyph.removeOverlap()
print("Saving...")
font.generate('testfont.otf')
