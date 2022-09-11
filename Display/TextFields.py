from Display.DisplayResults import DisplayResults
import pygame as pg


pg.init()

BestCurrentDisplayTitle = DisplayResults(pg) \
    .setText("Current best fitness:") \
    .setColour((0, 255, 0)) \
    .setPosition(720, 10)

BestCurrentDisplay = DisplayResults(pg) \
    .setText("NaN") \
    .setColour((0, 125, 255)) \
    .setPosition(720, 50)

BestCurrentTimeTitle = DisplayResults(pg) \
    .setText("Current best travel time:") \
    .setColour((0, 255, 255)) \
    .setPosition(720, 90)

BestCurrentTime = DisplayResults(pg) \
    .setText("NaN") \
    .setColour((255, 125, 50)) \
    .setPosition(720, 130)

BestCurrentLengthTitle = DisplayResults(pg) \
    .setText("Current best travel length:") \
    .setColour((0, 255, 255)) \
    .setPosition(720, 170)

BestCurrentLength = DisplayResults(pg) \
    .setText("NaN") \
    .setColour((255, 125, 50)) \
    .setPosition(720, 210)

BestLastDisplayTitle = DisplayResults(pg) \
    .setText("Result from iteration:") \
    .setColour((255, 255, 0)) \
    .setPosition(720, 250)

BestLastDisplay = DisplayResults(pg) \
    .setText("0") \
    .setColour((255, 255, 125)) \
    .setPosition(720, 290)

AverageTimeTitle = DisplayResults(pg) \
    .setText("Average time of calculation: ") \
    .setColour((255, 60, 170)) \
    .setPosition(720, 330)

AverageTime = DisplayResults(pg) \
    .setText("0") \
    .setColour((255, 60, 170)) \
    .setPosition(720, 370)