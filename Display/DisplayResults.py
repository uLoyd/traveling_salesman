from __future__ import annotations


class DisplayResults:
    def __init__(self, pg):
        self.font = pg.font.SysFont('Arial', 30)
        self.pg = pg
        self.colour = None
        self.text = None
        self.x = 0
        self.y = 0

    def setFont(self, font: str, size: int) -> DisplayResults:
        self.font = self.pg.font.SysFont(font, size)
        return self

    def setText(self, text: str) -> DisplayResults:
        self.text = text
        return self

    def setColour(self, colour) -> DisplayResults:
        self.colour = colour
        return self

    def setPosition(self, x: int, y: int) -> DisplayResults:
        self.x = x
        self.y = y
        return self

    def create(self, window) -> DisplayResults:
        displayTest = self.font.render(self.text, True, self.colour)
        window.blit(displayTest, (self.x, self.y))
        return self


