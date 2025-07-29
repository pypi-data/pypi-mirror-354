# pyConsoleEngine
Ascii engine for drawing in console. Based on curses library

by [@Arizel79](https://t.me/Arizel79)

## Install
```
pip install pyAsciiEngine
```
## Example:
```python
from pyAsciiEngine import AsciiScreen, Colors
scr = AsciiScreen()

scr.setStr(5, 5, "Hello, world! Prees Q to exit", Colors.RED)
while True:
    key = scr.wait_key()
    if key == "q":
        break
        

```


