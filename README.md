# SMMDeathCounter
Counts number of deaths for display while streaming Super Mario Maker!

# Setup
1. Make a python virtual environment.
2. Run pip install -r requirements.txt
3. Edit monitor.py line 10 to match the part of the screen you want to monitor. Format: (x,y,xy)
3.a. Edit line 185 to your window widths make the script pause if your mouse leaves the game window area.
4. ??? (Is this even a thing?)
5. Profit (Run monitor.py)

## Tips
1. Uncomment the while loop in lines 15-21 to wait for your mouse to entire the proper area. Leave the "if mouse_pos.x < 1920:" and "break" lines commented out if you just want the script to print out your current mouse position... helpful for determining the game window.
