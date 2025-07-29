from engine import AsciiScreen, Colors, Styles, TextStyle, Anchors, Symbol



def main():
    sc = AsciiScreen()
    st = TextStyle(Colors.CYAN, Colors.BLACK, Styles.BOLD)

    while True:
        x, y = sc.getSizes()
        sc.setStr(20,0,"hello")
        sc.setStr(x // 2, y-1, f"Sizes: {x} {y}", anchor=Anchors.CENTER_X_ANCHOR, style=st)
        sc.drawRectangle(1, 1, 3,20, Symbol("@", "red"), isFill=False)

        key = sc.get_key()
        sc.update()
        if key == "q":
            break

if __name__ == '__main__':
    main()