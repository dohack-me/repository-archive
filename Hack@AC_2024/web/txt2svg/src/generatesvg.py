#!/usr/bin/env python3

import lxml.etree as ET

def render_xml(xml):
    # parses xml, eg entities are filled in
    print(xml)
    raw = ET.fromstring(xml)
    rendered = ET.tostring(raw)
    return rendered

SVG = """<?xml version="1.0"?>
*COMMENT*
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
	 viewBox="0 0 *XDIMENSION* *YDIMENSION*" xml:space="preserve">
<style type="text/css">
	.st0{font-family:'*FONTFAMILY*';}
	.st1{font-size:*FONTSIZE*px;}
	.st2{color:#000000;}
</style>
<text transform="matrix(1 0 0 1 *XTRANSLATE* *YTRANSLATE*)" class="st0 st1 st2">*CONTENT*</text>
</svg>
"""

class image:
    def __init__(self, text, font, size, x, y, comment="<!-- Generator: TXT2SVG, By Reyes Lee/ZakuroSoda  -->"):
        self.text = text
        self.font = font
        self.size = size
        self.x = int(x)
        self.y = int(y)
        self.comment = comment

    def generate_svg(self):
        svg = SVG
        svg = svg.replace("*XDIMENSION*", str(self.x)).replace("*YDIMENSION*", str(self.y))
        svg = svg.replace("*CONTENT*", self.text).replace("*FONTFAMILY*", self.font).replace("*FONTSIZE*", str(self.size))
        svg = svg.replace("*XTRANSLATE*", str(self.x/4)).replace("*YTRANSLATE*", str(self.y/2))
        svg = svg.replace("*COMMENT*", self.comment)

        return render_xml(svg)
