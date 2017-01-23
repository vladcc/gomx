
# gomx
GUI for the Raspberry Pi's omxplayer

Hello and welcome to the gomx readme!

gomx is a light gui for the hardware accelerated omxplayer on the Raspberry Pi.
It is written in Python using Tk.

With gomx you can move, resize, and hide the video (when you minize gomx). You can also use
the slider to move forward and back.  

Note: You will notice that the video window is always on top.
The reason for this is the way the omxplayer works and it's normal.

To use gomx you first have to install the python omx wrapper from the link below.

https://github.com/willprice/python-omxplayer-wrapper

Then open a terminal and type:

chmod +x gomx_setup.sh
sudo ./gomx_setup.sh

Now you can run any video with gomx [file name] from the command line, or do this:

1. Right click the video file
2. Select Open With...
3. Click on Custom Command Line
4. In Command line to execute: write "gomx %f" without the quotes
5. In Application name (optional, set it to keep association) write "gomx" without the quotes
6. Click OK

Now gomx is associated with that video format and a double click will open it.

gomx supports all keyboard controls for omxplayer. Type omxplayer -k for the full list.

The following functionality is added to the gui:

1. Double left click or w			  - fuscreen on/off
2. Right click when full screen	- show/hide player controls
3. Mouse wheel up					      - volume up
4. Mouse wheel down				      - volume down
5. Esc								            - fullscreen off/quit
6. q							        	      - quit

If you want to run gomx with arguments, run gomx from the terminal like you would
omxplayer. Note, however, that -o both (for audio output to both local and hdmi) 
is automatically added to the list.

Known issues: 

1. The video window may not resize properly when exiting fullscreen.
If that happens, go to fullscreen again and then go back. This should fix it.

2. The gui might crash, becoming unresponsive. 
In that case type in the terminal:

sudo killall python
sudo killall omxplayer.bin

to kill the python and omxplayer.bin processes.
