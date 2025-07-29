import engine
from engine import Colors, Anchors, Styles


def main():
    scr = engine.AsciiScreen()

    h1 = engine.TextStyle(Colors.RED, Colors.BLACK, Styles.BOLD)
    txt = engine.TextStyle(Colors.WHITE, Colors.BLACK, )
    last_key = None

    running = True
    while running:
        key = scr.get_key(.1)
        x, y = scr.getSizes()
        maxX, maxY = scr.getMaxCoords()

        if key == "q":
            running = False

        elif not key is None:
            last_key = repr(key)
        else:
            key = " "

        # drawing
        scr.clear()
        scr.setStr(0, 0, "PyConsoleEngine, (c) Kirill Fridrih", h1)
        scr.setStr(0, 1, "Prees Q to quit", txt)
        scr.setStr(maxX // 2, maxY - 1, f"Last preesed key: {last_key}", txt, anchor=Anchors.CENTER_X_ANCHOR)
        scr.setStr(maxX // 2, maxY , f"Sizes: {x}, {y}", txt, anchor=Anchors.CENTER_X_ANCHOR)
        scr.update()

    scr.quit()


if __name__ == '__main__':
    main()
