#!/usr/bin/python2

import sys
import thread
import time

sys.path.append("launchsalsa")

import launchsalsa

class StepController(launchsalsa.ScreenController):
    def __init__(self):
        self.view = launchsalsa.ScreenView(128, 16)
        self.grid = []
        self.pos = -1
        for i in range(0, 128):
            g = []
            for i in range(0, 16):
                g.append(False)
            self.grid.append(g)

    def onButtonDown(self, but, vel, row, col):
        if but == launchsalsa.GRID:
            row = row + self.view._offset[0]
            col = col + self.view._offset[1]
            self.grid[row - 1][col - 1] = not self.grid[row - 1][col - 1]
            self.view.update(launchsalsa.GRID, 1 if self.grid[row - 1][col - 1] else 0, row, col)
            self.view.draw()
        if but == launchsalsa.UP:
            self.view.scroll(-1, 0)
        if but == launchsalsa.DOWN:
            self.view.scroll(1, 0)
        if but == launchsalsa.LEFT:
            self.view.scroll(0, -1)
        if but == launchsalsa.RIGHT:
            self.view.scroll(0, 1)
        print("%s - %s, %s @ %s down" % (but, row, col, vel))
    
    def onPolyAftertouch(self, row, col, pressure):
        if self.grid[row - 1][col - 1]:
            self.view.update(launchsalsa.GRID, pressure, row, col)
            self.view.draw()
        print("%d, %d: %s aftertouch" % (col, row, pressure))

    def step(self):
        if self.pos != -1:
            for r in range(0, 128):
                on = False
                if self.grid[r][self.pos]:
                    on = True
                    launchsalsa._midiOut(2, launchsalsa._MIDI_OFF, (0, 127 - r, 0, 0, 0))
                self.view.update(launchsalsa.GRID, 1 if on else 0, r + 1, self.pos + 1)
        self.pos += 1
        if self.pos > 15:
            self.pos = 0
        for r in range(0, 128):
            on = False
            if self.grid[r][self.pos]:
                on = True
                launchsalsa._midiOut(2, launchsalsa._MIDI_ON, (0, 127 - r, 96, 0, 0))
            self.view.update(launchsalsa.GRID, 9 if on else 17, r + 1, self.pos + 1)
        self.view.draw()

sc = StepController()
def spawn():
    launchsalsa.run("salsastep", 1, 2, sc)
thread.start_new_thread(spawn, ())

time.sleep(1) #Prevent ALSA library from crashing... not really sure why that happens
def milliTime():
    return time.time() * 1000

nextTime = milliTime()
while True:
    while milliTime() < nextTime:
        continue
    sc.step()
    nextTime += 112.5 #133.333333.... bpm
