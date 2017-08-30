
# gomx
GUI for the Raspberry Pi's omxplayer

gomx is a light GUI for the hardware accelerated omxplayer.
It's done in Python using Tk. It allows you to move, resize, and hide(when you minimize) the video window.
With the slider you can move forward and back.

Note: The video window is always on top.
The reason for this is the way omxplayer works, it's normal.

To use gomx you first have to install the Python omx wrapper from the link below.

https://github.com/willprice/python-omxplayer-wrapper

Then open a terminal and type:

1. chmod +x gomx_setup.sh
2. sudo ./gomx_setup.sh

You can now play any video with "gomx [file name]" from the command line, or do this:

1. Right click the video file
2. Select "Open With..."
3. Click on "Custom Command Line"
4. In "Command line to execute:" write "gomx %f" without the quotes
5. In "Application name (optional, set it to keep association)" write "gomx" without the quotes
6. Click OK

Now gomx is associated with that video format and double clicking on files of that type will use it by default.

The GUI provides the following functionality:

1. Double left click or w - fullscreen on/off
2. Right click when full screen - show/hide player controls
3. Mouse wheel up - volume up
4. Mouse wheel down - volume down
5. Esc - fullscreen off/quit
6. q - quit

gomx supports all keyboard controls for omxplayer. Type omxplayer -k for the full list.

If you want to run gomx with arguments run gomx from the terminal like you would
omxplayer. Note, however, that "-o both" (for audio output to both local and hdmi)
is automatically added.

Known issues:

1. The video window may not resize properly when exiting fullscreen.
Fix: Go to fullscreen and back again.

2. The gui might crash becoming unresponsive.
Fix: Open the video file again. If that doesn't work kill gomx and omxplayer like so:

sudo killall omxplayer.bin
sudo killall gomx

If "killall gomx" doesn't do the trick try:
sudo pkill gomx --signal SIGKILL

3. The video window may not be properly aligned inside the GUI.
Fix: Change the value of PL_WIN_PAD inside the gomx script.
For me 48 works best. Another user reported he had to set it to 1.
