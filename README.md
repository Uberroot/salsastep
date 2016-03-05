# salsastep
A step sequencer interface for the Novation Launchpad Pro

# Clone it!
git clone --recursive https://github.com/Uberroot/salsastep.git

# Usage
Run this script and use what ever tool you wish to create the following ALSA MIDI connections
* Launchpad output 1 (or 0 if you wish to use the Live screen) -> salsatep input 0
* salsastep output 0 -> Launchpad input 1 (or 0 if you wish to use the Live screen) 
* salsastep output 1 -> Destination for MIDI events

Note that this script does not yet synchronize with MIDI clocks and is currently locked at 133.333 bpm. This will change in the future.

The sequencer will continually play 1/16th notes in a one bar loop (will be configurable in the future!).
Tap the grid to enable or disable a note
Use the arrow keys to scroll the grid
