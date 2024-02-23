from src.Lib import gui

testGUI = False


def test_gui():
    # Test with positive numbers
    if testGUI:
        g = gui.GUI()
        g.run()