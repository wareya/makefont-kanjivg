#!/usr/bin/python

# ISC license

import re
import os
import fontforge
import codecs
font = fontforge.font()

# The KanjiVG data does not contain a whitespace character, so we need to make it manually.
# Setting the width of a glyph makes it be an occupied glyph, so that's all we need to do.
glyph = font.createChar(0x20) # codepoint of ASCII space
glyph.width = 1000 # Default font size in FnFg
glyph = font.createChar(0x3000) # codepoint of ideographic space
glyph.width = 1000 # Default font size in FnFg

# In the future, I plan to have a supplementary set of SVGs covering the full breadth of normal punctuation.
# However, spaces are simply too important to let sit doing nothing.

print("Generating...")
for name in list(filter(lambda name: re.match(".....\.svg", name) , os.listdir())):
    glyph = font.createChar(int(name[0:5], 16))
    glyph.importOutlines(name)
    # We simplify before doing anything in order to avoid "The curve is too short." from "removeOverlap"
    # Simplify can cause unrounded points, which will cause bugs in removeOverlap.
    # We need to round before removeOverlap anyways, but we also need to round after simplify.
    # Therefore, simplify is first.
    glyph.simplify(1,("smoothcurves", "mergelines", "setstarttoextremum", "removesingletonpoints"))
    glyph.round()
    glyph.removeOverlap()
    # removeOverlap can and will cause very short paths to occur, and can cause nearly-same-location points.
    # We need to simplify to remove them.
    # However, we need to round after simplifying. 
    # However, the last shapechanging instruction done to a glyph aught to be "removeOverlap".
    # ... Therefore, we essentially need to duplicate the above code again.
    glyph.simplify(2,("smoothcurves", "mergelines", "setstarttoextremum", "removesingletonpoints"))
    glyph.round()
    glyph.removeOverlap()
    # The glyph is now in the correct shape, but contour direction is almost definitely backwards (FnFg, WHY?!)
    glyph.correctDirection()
print("Saving...")
font.generate('testfont.otf')
