# SMMDeathCounter
Counts number of deaths for display while streaming Super Mario Maker! Reads from a twitch stream!

# Setup
1. Make a python virtual environment.
2. Run pip install -r requirements.txt
3. Edit monitor.py line 16-20 (or at least set from_stream to false).
    3.a. If you don't choose live stream edit game cords to match the part of the screen you want to monitor. Format: (x,y,xy)
    3.b. Edit line 185 to your window widths make the script pause if your mouse leaves the game window area.
4. ??? (Is this even a thing?)
5. Profit (Run monitor.py)

# Setup Tips
1. Uncomment the while loop in lines 15-21 to wait for your mouse to entire the proper area. Leave the "if mouse_pos.x < 1920:" and "break" lines commented out if you just want the script to print out your current mouse position... helpful for determining the game window.

# Known Issues
1. Sometimes it double counts deaths. Yeah yeah I know. YOU HAD ONE JOB.
