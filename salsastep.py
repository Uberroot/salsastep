#!/usr/bin/python2

import sys
import thread
import time

sys.path.append("launchsalsa")

import launchsalsa

class Sequencer:
    def __init__(self, did):
        self.view = launchsalsa.ScreenView(128, 16)
        self.grid = []
        self.pos = -1
        self.__did = did
        for i in range(0, 128):
            g = []
            for i in range(0, 16):
                g.append(False)
            self.grid.append(g)
    
    def toggle(self, row, col):
        row = row + self.view._offset[0]
        col = col + self.view._offset[1]
        self.grid[row - 1][col - 1] = not self.grid[row - 1][col - 1]
        self.view.update(launchsalsa.GRID, 1 if self.grid[row - 1][col - 1] else 0, row, col)
        self.view.draw()
    
    def step(self):
        if self.pos != -1:
            for r in range(0, 128):
                on = False
                if self.grid[r][self.pos]:
                    on = True
                    launchsalsa._midiOut(2 + self.__did, launchsalsa._MIDI_OFF, (0, 127 - r, 0, 0, 0))
                self.view.update(launchsalsa.GRID, 1 if on else 0, r + 1, self.pos + 1)
        self.pos += 1
        if self.pos > 15:
            self.pos = 0
        for r in range(0, 128):
            on = False
            if self.grid[r][self.pos]:
                on = True
                launchsalsa._midiOut(2 + self.__did, launchsalsa._MIDI_ON, (0, 127 - r, 96, 0, 0))
            self.view.update(launchsalsa.GRID, 9 if on else 17, r + 1, self.pos + 1)

class StepController(launchsalsa.ScreenController):
    def __init__(self, count):
        self.sequencers = []
        self.current = 0
        self.seqCount = count
        self.__dev_colors = []
        for i in range(0, self.seqCount):
            self.sequencers.append(Sequencer(i))
            self.__dev_colors.append(i * 8 + 4)
    
    def onButtonDown(self, but, vel, row, col):
        if but == launchsalsa.DEVICE:
            self.current = 0 if self.current == self.seqCount - 1 else self.current + 1
            self.sequencers[self.current].view.draw(True)
            launchsalsa._midiOut(1, launchsalsa._MIDI_ON, (0, launchsalsa.DEVICE, self.__dev_colors[self.current], 0, 0))
        if but == launchsalsa.GRID:
            self.sequencers[self.current].toggle(row, col)
        if but == launchsalsa.UP:
            self.sequencers[self.current].view.scroll(-1, 0)
        if but == launchsalsa.DOWN:
            self.sequencers[self.current].view.scroll(1, 0)
        if but == launchsalsa.LEFT:
            self.sequencers[self.current].view.scroll(0, -1)
        if but == launchsalsa.RIGHT:
            self.sequencers[self.current].view.scroll(0, 1)
    
    def onPolyAftertouch(self, row, col, pressure):
        return

    def step(self):
        for i in range(0, self.seqCount):
            self.sequencers[i].step()
        self.sequencers[self.current].view.draw()

count = 3

sc = StepController(count)
def spawn():
    launchsalsa.run("salsastep", 1, 1 + count, sc)
thread.start_new_thread(spawn, ())

time.sleep(1) #Prevent ALSA library from crashing... not really sure why that happens
def milliTime():
    return time.time() * 1000
for i in range(0, count):
    sc.sequencers[i].view.scroll(60, 0)
nextTime = milliTime()
while True:
    while milliTime() < nextTime:
        continue
    sc.step()
    nextTime += 112.5 #133.333333.... bpm
