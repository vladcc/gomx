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

Then run open a terminal and type:

sudo ./gomx_setup.sh

Now you can run any video with gomx <file name> from the terminal, or do this:

1. Right click the video file
2. Select Open With...
3. Click on Custom Command Line
4. In Command line to execute: on the top write "gomx %f" without the quotes
5. In Application name (optional, set it to keep association) write "gomx" without the quotes
6. Click OK

Now gomx is associated with that video format.

gomx supports all keyboard controls for the omxplayer. Type omxplayer -k for the full list.

The following functionality is added to the gui:

Double left click or w			- fuscreen on/off
Right click when full screen	- show/hide player controls
Mouse wheel up					- volume up
Mouse wheel down				- volume down
Esc								      - unfullscreen/quit
q							        	- quit

If you want to run gomx with arguments, run gomx from the terminal like you would
omxplayer. Note, however, that -o both (for audio output to both local and hdmi) 
is automatically added to the list.

Known issues: 
1. Sometimes the video window does not resize properly when exiting fullscreen.
If that happens, go to fullscreen again and then go back. This should fix it.

2. It usually works fine, but somtimes the gui might crash, becoming unresponsive. 
In that case type in the terminal:

sudo killall python
sudo killall omxplayer.bin

to kill the python and omxplayer.bin processes.
