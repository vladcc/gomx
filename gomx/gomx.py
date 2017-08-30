#!/usr/bin/python

import sys
import os
import subprocess
import signal
import threading
import tkMessageBox
from Tkinter import *
from omxplayer import OMXPlayer
from omxplayer.keys import *
from time import sleep

# CONSTANTS
# the player resize command code
PL_RESIZE = -1

# video window padding in pixels
# the window is moved PL_WIN_PAD pixels to the left and down
# in order to fit exactly in the gui window
#
# Note: 48 appears to not be consistent on all systems.
# You may need to set it to something else.
#
PL_WIN_PAD = 48

# the title of the gui window
VERSION = 1.1
TITLE = "%s%.1f" % ("gomx v", VERSION)

# this script's name and pid
MYNAME = os.path.basename(__file__)
MYPID = os.getpid()
# player image name
OMXPL = "omxplayer.bin"
# /CONSTANTS

# stop previous instances
for proc in subprocess.check_output(["pgrep", MYNAME]).split('\n'):
	if (proc != ""):
		if (int(proc) != MYPID):
			os.system("killall " + OMXPL)
			os.kill(int(proc), signal.SIGTERM)

# GLOBAL VARIABLES
# global player command
gpl_cmd = 0

# global gui window absolute x and y
# used for video window x1, y1
gwin_abs_x = 0
gwin_abs_y = 0

# global gui video_frame height and width
# used for video window x2, y2
gframe_height = 0
gframe_width = 0

# global gui flag
gis_gui_running = False

# global player flag
gis_player_alive = False

# global current video file
gcurr_video = 0
if (len(sys.argv) > 1):
	gcurr_video = str(sys.argv[1])
	del sys.argv[0]

args = ['-o', 'both']
args.extend(sys.argv)

# global progress bar flag
gis_progrs_clicked = False

# global full screen flag
gis_full_scr = False
# /GLOBAL VARIABLES

# PLAYER THREAD FUNCTION
def start_player():
	"Start the player and loop waiting for commands"
	global gpl_cmd, gis_player_alive, gis_progrs_clicked
	global gwin_abs_x, gwin_abs_y, gframe_height, gframe_width

	if (gcurr_video == 0):
		return

	video_path = gcurr_video
	win_gui.title(TITLE + " - " + video_path)
	player = OMXPlayer(video_path, args)

	# VIDEO TIME AND PROGRESS BAR
	# set video duration
	dur = player.duration()
	mins = dur / 60
	secs = dur % 60
	l_duration.config(text='/ %02d:%02d' % (mins, secs))

	# progress bar binding functions
	def s_progrs_clicked(event):
		"Don't update slider when it's clicked"
		global gis_progrs_clicked
		gis_progrs_clicked = True

	def s_progrs_released(event):
		"Update video position on release"
		global gis_progrs_clicked
		player.set_position(s_progrs.get())
		gis_progrs_clicked = False

	def s_progrs_update(event):
		"Update elapsed time label on each increment"
		pos = s_progrs.get()
		mins = pos / 60
		secs = pos % 60
		l_time.config(text='%02d:%02d' % (mins, secs))

	# configure & bind the progress bar
	s_progrs.config(to=dur-1, length=win_gui.winfo_width()/1.5, command=s_progrs_update)
	s_progrs.bind('<ButtonPress-1>', s_progrs_clicked)
	s_progrs.bind('<ButtonRelease-1>', s_progrs_released)
	# /VIDEO TIME AND PROGRESS BAR

	gis_player_alive = True
	pl_resize()
	# MAIN PLAYER LOOP
	while gis_player_alive:
		if (gis_gui_running == True):
			# see if window is moved
			w_abs_x = win_gui.winfo_x()
			w_abs_y = win_gui.winfo_y()

			if (gwin_abs_x != w_abs_x or gwin_abs_y != w_abs_y):
				# update global coordinates and resize
				gwin_abs_x = w_abs_x
				gwin_abs_y = w_abs_y
				pl_resize()

			if (gpl_cmd == PL_RESIZE):
				# calculate new dimensions
				pl_x1 = gwin_abs_x + PL_WIN_PAD
				pl_y1 = gwin_abs_y + PL_WIN_PAD
				pl_x2 = pl_x1 + gframe_width
				pl_y2 = pl_y1 + gframe_height
				# change size
				player.set_video_pos(pl_x1, pl_y1, pl_x2, pl_y2)
				# zero out command
				gpl_cmd = 0

			# get video position
			pos = player.position()
			# update progress bar
			if (gis_progrs_clicked == False):
				s_progrs.set(pos)

			# check if video is done and exit gracefully
			if (int(dur) == int(pos)):
				b_stop_press()

		if (gpl_cmd == EXIT):
			gis_player_alive = False

		if (gpl_cmd != 0):
			# do command
			player.action(gpl_cmd)
			gpl_cmd = 0

		sleep(0.1)
	# /MAIN PLAYER LOOP
# /PLAYER THREAD FUNCTION

# PLAYER THREAD
def run_player_thread():
	t_pl = threading.Thread(target=start_player)
	t_pl.start()
# /PLAYER THREAD

# PLAYER INTERFACE FUNCTIONS
def pl_exit():
	global gpl_cmd
	gpl_cmd = EXIT

def pl_pause():
	global gpl_cmd
	gpl_cmd = PAUSE

def pl_resize():
	global gpl_cmd
	gpl_cmd = PL_RESIZE

def pl_decr_speed():
	global gpl_cmd
	gpl_cmd = DECREASE_SPEED

def pl_incr_speed():
	global gpl_cmd
	gpl_cmd = INCREASE_SPEED

def pl_rewind():
	global gpl_cmd
	gpl_cmd = REWIND

def pl_fast_fwd():
	global gpl_cmd
	gpl_cmd = FAST_FORWARD

def pl_show_info():
	global gpl_cmd
	gpl_cmd = SHOW_INFO

def pl_prev_aud_strm():
	global gpl_cmd
	gpl_cmd = PREVIOUS_AUDIO

def pl_next_aud_strm():
	global gpl_cmd
	gpl_cmd = NEXT_AUDIO

def pl_prev_chptr():
	global gpl_cmd
	gpl_cmd = PREVIOUS_CHAPTER

def pl_next_chptr():
	global gpl_cmd
	gpl_cmd = NEXT_CHAPTER

def pl_prev_sub():
	global gpl_cmd
	gpl_cmd = PREVIOUS_SUBTITLE

def pl_next_sub():
	global gpl_cmd
	gpl_cmd = NEXT_SUBTITLE

def pl_toggle_sub():
	global gpl_cmd
	gpl_cmd = TOGGLE_SUBTITLE

def pl_decr_sub_delay():
	global gpl_cmd
	gpl_cmd = DECREASE_SUBTITLE_DELAY

def pl_incr_sub_delay():
	global gpl_cmd
	gpl_cmd = INCREASE_SUBTITLE_DELAY

def pl_decr_vol():
	global gpl_cmd
	gpl_cmd = DECREASE_VOLUME

def pl_incr_vol():
	global gpl_cmd
	gpl_cmd = INCREASE_VOLUME

def pl_seek_back_small():
	global gpl_cmd
	gpl_cmd = SEEK_BACK_SMALL

def pl_seek_fwd_small():
	global gpl_cmd
	gpl_cmd = SEEK_FORWARD_SMALL

def pl_seek_back_large():
	global gpl_cmd
	gpl_cmd = SEEK_BACK_LARGE

def pl_seek_fwd_large():
	global gpl_cmd
	gpl_cmd = SEEK_FORWARD_LARGE
# /PLAYER INTERFACE FUNCTIONS

# GUI BINDS
def frame_on_resize(event):
	"Update video window size to fit it's gui frame"
	global gpl_cmd
	global gwin_abs_x, gwin_abs_y, gframe_height, gframe_width
	global gis_full_scr

	if (gis_full_scr == True):
		return

	# update global height and width
	gframe_height = event.height
	gframe_width = event.width
	pl_resize()

def full_screen():
	"Toggle full screen"
	global gis_full_scr
	global gpl_cmd
	global gwin_abs_x, gwin_abs_y
	global gframe_width, gframe_height

	if (gis_full_scr == False):
		# set full screen
		# full screen is done like this instead of
		# resizing to fit the fullscreen gui window
		# because omxplayer always fits the full size of the screen
		# while the gui system may not
		win_gui.attributes("-fullscreen", True)
		gwin_abs_x = 0
		gwin_abs_y = 0
		gframe_width = 0
		gframe_height = 0
		pl_resize()
		gis_full_scr = True
	else:
		# return to previous state
		win_gui.attributes("-fullscreen", False)
		gwin_abs_x = win_gui.winfo_x()
		gwin_abs_y = win_gui.winfo_y()
		gframe_width = video_frame.winfo_width()
		gframe_height = video_frame.winfo_height()
		pl_resize()
		gis_full_scr = False

def gui_show_ctrl(event):
	"Show the controls when fullscreened"
	global gwin_abs_x, gwin_abs_y
	global gframe_width, gframe_height

	if (gis_full_scr == True):
		if (gui_show_ctrl.is_shown == False):
			# show the controls by fiting the video
			# in the fullscreened frame
			gwin_abs_x = win_gui.winfo_x()
			gwin_abs_y = win_gui.winfo_y()
			gframe_width = video_frame.winfo_width()
			gframe_height = video_frame.winfo_height()
			pl_resize()
			gui_show_ctrl.is_shown = True
		else:
			# return to fullscreen
			gwin_abs_x = 0
			gwin_abs_y = 0
			gframe_width = 0
			gframe_height = 0
			pl_resize()
			gui_show_ctrl.is_shown = False
# static flag
gui_show_ctrl.is_shown = False

def gui_vhide_on_minimize(event):
	"Hide video on gui minimize event"
	global gpl_cmd
	gpl_cmd = HIDE_VIDEO

def gui_vshow_on_unminimize(event):
	"Show vide when gui window is unminimized"
	global gpl_cmd
	gpl_cmd = UNHIDE_VIDEO

def gui_kbd_fscr(event):
	"Go fullscreen"
	full_screen()

def gui_kbd_play_pause(event):
	"Get play/pause from the keyboard"
	b_play_press()

def gui_kbd_stop(event):
	"Get stop from keyboard"
	b_stop_press()

def gui_kbd_quit(event):
	"Get quit command from the keyboard"
	b_quit_press()

def gui_kbd_esc(event):
	"Toggle fullscreen if it's on or quit"
	if (gis_full_scr == True):
		full_screen()
	else:
		b_quit_press()

def gui_kbd_decr_speed(event):
	"Slower"
	pl_decr_speed()

def gui_kbd_incr_speed(event):
	"Faster"
	pl_incr_speed()

def gui_kbd_rewind(event):
	"Start over"
	pl_rewind()

def gui_kbd_fast_fwd(event):
	"Fast forward"
	pl_fast_fwd()

def gui_kbd_show_info(event):
	"Show info"
	pl_show_info()

def gui_kbd_prev_aud_st(event):
	"Previous audio stream"
	pl_prev_aud_strm()

def gui_kbd_next_audio_st(event):
	"Next audio stream"
	pl_next_aud_strm()

def gui_kbd_prev_chptr(event):
	"Go to next chapter"
	pl_prev_chptr()

def gui_kbd_next_chptr(event):
	"Go to next chapter"
	pl_next_chptr()

def gui_kbd_prev_sub(event):
	"Previous subtitles"
	pl_prev_sub()

def gui_kbd_next_sub(event):
	"Next subtitles"
	pl_next_sub()

def gui_kbd_toggle_sub(event):
	"Toggle subtitles"
	pl_toggle_sub()

def gui_kbd_decr_sub_delay(event):
	"Decrease subtitle delay"
	pl_decr_sub_delay()

def gui_kbd_incr_sub_delay(event):
	"Increase subtitle delay"
	pl_incr_sub_delay()

def gui_kbd_decr_vol(event):
	"Volume down"
	pl_decr_vol()

def gui_kbd_incr_vol(event):
	"Volume up"
	pl_incr_vol()

def gui_kbd_seek_back_small(event):
	"Go back slightly"
	pl_seek_back_small()

def gui_kbd_seek_fwd_small(event):
	"Go forward slightly"
	pl_seek_fwd_small()

def gui_kbd_seek_back_large(event):
	"Go back a lot"
	pl_seek_back_large()

def gui_kbd_seek_fwd_large(event):
	"Go forward a lot"
	pl_seek_fwd_large()

def b_play_press():
	"Toggle play/pause"
	if (gis_player_alive == True):
		pl_pause()
	else:
		run_player_thread()

def b_stop_press():
	"Stop player only"
	pl_exit()
	win_gui.title(TITLE)

def b_quit_press():
	"Quit everything"
	pl_exit()
	win_gui.quit()

def mouse_wheel(event):
	if event.num == 5 or event.delta == -120:
		pl_decr_vol()
	if event.num == 4 or event.delta == 120:
		pl_incr_vol()
# /GUI BINDS

# GUI MAIN THREAD
win_gui = Tk()
win_gui.title(TITLE)
# default size
wg_w = 640
wg_h = 480
wg_x = 200
wg_y = 200
win_gui.geometry('{}x{}+{}+{}'.format(wg_w,wg_h,wg_x,wg_y))
# key binds
win_gui.bind('1', gui_kbd_decr_speed)
win_gui.bind('2', gui_kbd_incr_speed)
win_gui.bind('less', gui_kbd_rewind)
win_gui.bind('>', gui_kbd_fast_fwd)
win_gui.bind('z', gui_kbd_show_info)
win_gui.bind('j', gui_kbd_prev_aud_st)
win_gui.bind('k', gui_kbd_next_audio_st)
win_gui.bind('i', gui_kbd_prev_chptr)
win_gui.bind('o', gui_kbd_next_chptr)
win_gui.bind('n', gui_kbd_prev_sub)
win_gui.bind('m', gui_kbd_next_sub)
win_gui.bind('s', gui_kbd_toggle_sub)
win_gui.bind('d', gui_kbd_decr_sub_delay)
win_gui.bind('f', gui_kbd_incr_sub_delay)
win_gui.bind('w', gui_kbd_fscr)
win_gui.bind('q', gui_kbd_quit)
win_gui.bind('<space>', gui_kbd_play_pause)
win_gui.bind('p', gui_kbd_play_pause)
win_gui.bind('-', gui_kbd_decr_vol)
win_gui.bind('+', gui_kbd_incr_vol)
win_gui.bind('=', gui_kbd_incr_vol)
win_gui.bind('<Left>', gui_kbd_seek_back_small)
win_gui.bind('<Right>', gui_kbd_seek_fwd_small)
win_gui.bind('<Up>', gui_kbd_seek_back_large)
win_gui.bind('<Down>', gui_kbd_seek_fwd_large)
win_gui.bind('t', gui_kbd_stop)
win_gui.bind('<Map>', gui_vshow_on_unminimize)
win_gui.bind('<Unmap>', gui_vhide_on_minimize)
# unfullscreen or quit when escape is pressed
win_gui.bind('<Escape>', gui_kbd_esc)
# show controls on right click
win_gui.bind('<ButtonPress-3>', gui_show_ctrl)
win_gui.bind("<Button-4>", mouse_wheel)
win_gui.bind("<Button-5>", mouse_wheel)

# the frame holding the video window
video_frame = Frame(win_gui)
video_frame.pack(side="top", fill="both", expand=True)
video_frame.bind("<Configure>", frame_on_resize)
video_frame.bind("<Double-Button-1>", gui_kbd_fscr)

# the frame holding the time and progress bar
time_frame = Frame(win_gui)
time_frame.pack(side="top")

# the progress bar is reconfigured and rebinded with every player thread
# see start_player()
s_progrs = Scale(time_frame, from_=0, to=0, orient="horizontal", showvalue=False)
s_progrs.pack(side="left")

l_duration = Label(time_frame, text="")
l_duration.pack(side="right")
l_time = Label(time_frame, text="00:00")
l_time.pack(side="right")

# the frame holding the control buttons
ctrl_frame = Frame(win_gui)
ctrl_frame.pack(side="bottom")

b_vol_down = Button(ctrl_frame, text="Vol. -", command=pl_decr_vol)
b_vol_down.pack(side="left")
b_vol_up = Button(ctrl_frame, text="Vol. +", command=pl_incr_vol)
b_vol_up.pack(side="left")
b_play = Button(ctrl_frame, text="Play / Pause", command=b_play_press)
b_play.pack(side="left")
b_stop = Button(ctrl_frame, text="Stop", command=b_stop_press)

gis_gui_running = True
run_player_thread()
win_gui.mainloop()
gis_gui_running = False
# /GUI MAIN THREAD
# exit the player when gui is closed
pl_exit()
