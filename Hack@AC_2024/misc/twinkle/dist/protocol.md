## Protocol Outline
The protocol employs an 8-LED NeoPixel strip to encode hexadecimal data. The LEDs are numbered 0 through 7. Each LED can take Red, Green, and Blue values, with each value ranging from 0 to 255. The actual displayed color of the LED is determined by the combination of these three values.

1. **Packet Start**:
   - A new packet begins with LED 0 displaying solid White (255,255,255) for 2 seconds. LEDs 1-7 are off at this time.

Here's an ASCII representation of the NeoPixel strip at the start of a packet:

```
LED: 0 1 2 3 4 5 6 7
     ↓
     Solid White (Packet Start)
```

2. **Channel Indication and Data Encoding**:
   - After the 2-second delay, LED 0 is set to pure Red, Green, or Blue (255 intensity on the chosen color and 0 on the other two). This indicates the data channel for the current packet.
   - Simultaneously, hex data is encoded into the color intensities on LEDs 1-7. The chosen channel carries the actual data, and the other two channels are set to random intensities.
   - Each LED from 1-7 represents one byte of hex data, encoding a total of 7 bytes per packet on the chosen channel.

After the delay, LED 0 is set to pure Red, Green, or Blue to indicate the chosen channel, and data is simultaneously encoded into the color intensities on LEDs 1-7. In this example, we choose the Green channel, so LED 0 will be pure green (0,255,0) and the Green value will carry the actual data on LEDs 1-7:

```
LED: 0           1           2           3           4           5           6           7
R    (0)         RND         RND         RND         RND         RND         RND         RND
G    (255)       DATA        DATA        DATA        DATA        DATA        DATA        DATA
B    (0)         RND         RND         RND         RND         RND         RND         RND
```

Remember, the color displayed by each LED is the combination of the Red, Green, and Blue values. Therefore, LEDs won't show pure colors (except for LED 0 at the channel indication step).

3. **Additional Notes**:
   - Each packet will be broadcast for 3 seconds
   - After each broadcast, LEDs will be cleared (turned off) until the next packet is broadcasted.
   - After all packets have been broadcasted, LEDs will turn off. 