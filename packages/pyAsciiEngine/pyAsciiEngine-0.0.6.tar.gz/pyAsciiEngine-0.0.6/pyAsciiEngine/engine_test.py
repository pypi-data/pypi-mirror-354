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
        w, h = scr.getHW()
        maxX, maxY = scr.getMaxCoords()

        if key == "q":
            running = False

        elif not key is None:
            last_key = key

        # drawing
        scr.setStr(0, 0, "PyConsoleEngine, (c) Kirill Fridrih", h1)
        scr.setStr(0, 1, "Prees Q to quit", txt)
        scr.setStr(maxX // 2, maxY, f"Last preesed key: {last_key}", txt, anchor=Anchors.CENTER_X_ANCHOR)
        scr.setStr(maxX // 2, maxY , f"Height and width: {h}, {w}", txt, anchor=Anchors.CENTER_X_ANCHOR)
        scr.update()

    scr.quit()


if __name__ == '__main__':
    main()
