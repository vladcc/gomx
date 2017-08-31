#!/usr/bin/python

import os
import subprocess
import signal
import math
import tkMessageBox
from Tkinter import *
from omxplayer import OMXPlayer
from omxplayer.keys import *

# handle keyboard interrupts
def signal_handler(signal, frame):
	print "Bye"
	b_quit_press()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

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

# wait time in ms for tk.after()
CALLBACKT = 100
# /CONSTANTS

# stop previous instances
for proc in subprocess.check_output(["pgrep", MYNAME]).split('\n'):
	if (proc != ""):
		if (int(proc) != MYPID):
			os.system("killall " + OMXPL)
			os.kill(int(proc), signal.SIGTERM)

# GLOBAL VARIABLES
# current video file
gcurr_video = 0

# progress bar flag
gis_progrs_clicked = False

# gui flag
gis_gui_running = False

# full screen flag
gis_full_scr = False

# player flag
gis_player_alive = False

# player instance
gplayer = 0

# gui window absolute x and y
# used for video window x1, y1
gwin_abs_x = 0
gwin_abs_y = 0

# gui video_frame height and width
# used for video window x2, y2
gframe_height = 0
gframe_width = 0

# video timing
gdur = 0
gmins = 0
gsecs = 0
# /GLOBAL VARIABLES

# do arguments
if (len(sys.argv) > 1):
	gcurr_video = str(sys.argv[1])
	del sys.argv[0]

args = ['-o', 'both']
args.extend(sys.argv)

# PLAYER ROUTINES
def start_player():
	"Launch the player, get video duration, set progress bar to 0"
	global gplayer, gcurr_video, gis_player_alive
	global gdur, gmins, gsecs

	if (gcurr_video == 0):
		return False

	video_path = gcurr_video
	win_gui.title(TITLE + " - " + video_path)
	gplayer = OMXPlayer(video_path, args)
	gis_player_alive = True
	gplayer.set_aspect_mode("letterbox")
	gdur = gplayer.duration()
	gmins = gdur / 60
	gsecs = gdur % 60
	l_duration.config(text='/ %02d:%02d' % (gmins, gsecs))
	s_progrs.set(0)
	s_progrs.config(state="normal")
	return gis_player_alive

def update_player():
	"Callback for tk.after(), called every CALLBACKT ms"
	global gplayer, gcurr_video, gis_player_alive
	global gwin_abs_x, gwin_abs_y
	global gdur, gmins, gsecs

	if (gis_player_alive):
		# progress bar binding functions
		def s_progrs_clicked(event):
			"Don't update the slider when it's clicked"
			global gis_progrs_clicked
			gis_progrs_clicked = True

		def s_progrs_released(event):
			"Update video position on release"
			global gis_progrs_clicked
			pos = s_progrs.get()
			if (int(pos) < int(gdur)):
				gplayer.set_position(pos)
			gis_progrs_clicked = False

		def s_progrs_update(event):
			"Update elapsed time label on each increment"
			pos = s_progrs.get()
			gmins = pos / 60
			gsecs = pos % 60
			l_time.config(text='%02d:%02d' % (gmins, gsecs))

		# configure & bind the progress bar
		s_progrs.config(to=gdur-1, length=win_gui.winfo_width()/1.5, command=s_progrs_update)
		s_progrs.bind('<ButtonPress-1>', s_progrs_clicked)
		s_progrs.bind('<ButtonRelease-1>', s_progrs_released)

		if (gis_gui_running):
			# see if window is moved
			w_abs_x = win_gui.winfo_x()
			w_abs_y = win_gui.winfo_y()

			if (gwin_abs_x != w_abs_x or gwin_abs_y != w_abs_y):
				# update global coordinates and resize
				gwin_abs_x = w_abs_x
				gwin_abs_y = w_abs_y
				pl_resize()

			pos = s_progrs.get()
			# get video position
			if (int(pos) < int(gdur)):
				try:
					pos = gplayer.position()
				except:
					gis_player_alive = False

			# update progress bar
			if (gis_progrs_clicked == False):
				s_progrs.set(pos)

			# exit if video is done
			if (int(gdur) <= int(pos)):
				b_stop_press()

		win_gui.after(CALLBACKT, update_player)
	return
# /PLAYER ROUTINES

# PLAYER INTERFACE
def player_do(act):
	if (gis_player_alive):
		gplayer.action(act)

def pl_exit():
	global gis_player_alive, gis_full_scr
	s_progrs.set(0)
	player_do(EXIT)
	gis_player_alive = False
	if (gis_full_scr):
		full_screen()
	s_progrs.config(state="disabled")

def pl_pause():
	player_do(PAUSE)

def pl_resize():
	global gwin_abs_x, gwin_abs_y, gframe_height, gframe_width
	# calculate new dimensions
	pl_x1 = gwin_abs_x + PL_WIN_PAD
	pl_y1 = gwin_abs_y + PL_WIN_PAD
	pl_x2 = pl_x1 + gframe_width
	pl_y2 = pl_y1 + gframe_height
	# change size
	if (gis_player_alive):
		gplayer.set_video_pos(pl_x1, pl_y1, pl_x2, pl_y2)
		player_do(PL_RESIZE)

def pl_decr_speed():
	player_do(DECREASE_SPEED)

def pl_incr_speed():
	player_do(INCREASE_SPEED)

def pl_rewind():
	player_do(REWIND)

def pl_fast_fwd():
	player_do(FAST_FORWARD)

def pl_show_info():
	player_do(SHOW_INFO)

def pl_prev_aud_strm():
	player_do(PREVIOUS_AUDIO)

def pl_next_aud_strm():
	player_do(NEXT_AUDIO)

def pl_prev_chptr():
	player_do(PREVIOUS_CHAPTER)

def pl_next_chptr():
	player_do(NEXT_CHAPTER)

def pl_prev_sub():
	player_do(PREVIOUS_SUBTITLE)

def pl_next_sub():
	player_do(NEXT_SUBTITLE)

def pl_toggle_sub():
	player_do(TOGGLE_SUBTITLE)

def pl_decr_sub_delay():
	player_do(DECREASE_SUBTITLE_DELAY)

def pl_incr_sub_delay():
	player_do(INCREASE_SUBTITLE_DELAY)

def pl_decr_vol():
	player_do(DECREASE_VOLUME)

def pl_incr_vol():
	player_do(INCREASE_VOLUME)

def pl_seek_back_small():
	player_do(SEEK_BACK_SMALL)

def pl_seek_fwd_small():
	player_do(SEEK_FORWARD_SMALL)

def pl_seek_back_large():
	player_do(SEEK_BACK_LARGE)

def pl_seek_fwd_large():
	player_do(SEEK_FORWARD_LARGE)
# /PLAYER INTERFACE

# SCREEN HANDLERS
def frame_on_resize(event):
	"Update video window size to fit the gui frame"
	global gwin_abs_x, gwin_abs_y, gframe_height, gframe_width
	global gis_full_scr

	# update global height and width
	gframe_height = event.height
	gframe_width = event.width
	pl_resize()
	return

def show_ctrls(bool_show):
	"Hide/show control frames"
	if (bool_show):
		video_frame.pack_forget()
		video_frame.pack(side="top", fill="both", expand=True)
		time_frame.pack(side="top")
		ctrl_frame.pack(side="bottom")
	else:
		video_frame.pack_forget()
		video_frame.pack(side="top", fill="both", expand=True)
		ctrl_frame.pack_forget()
		time_frame.pack_forget()
	return

def full_screen():
	"Toggle full screen"
	global gis_full_scr
	global gwin_abs_x, gwin_abs_y
	global gframe_width, gframe_height

	if (gis_full_scr == False):
		# set full screen
		# full screen is done like this instead of
		# resizing to fit the fullscreen gui window
		# because omxplayer always fits the full size of the screen
		# while the gui system may not
		win_gui.attributes("-fullscreen", True)
		show_ctrls(False)
		gwin_abs_x = 0
		gwin_abs_y = 0
		gframe_width = 0
		gframe_height = 0
		pl_resize()
		gis_full_scr = True
	else:
		# return to previous state
		win_gui.attributes("-fullscreen", False)
		show_ctrls(False)
		show_ctrls(True)
		gwin_abs_x = win_gui.winfo_x()
		gwin_abs_y = win_gui.winfo_y()
		gframe_width = video_frame.winfo_width()
		gframe_height = video_frame.winfo_height()
		pl_resize()
		gis_full_scr = False
	return
# /SCREEN HANDLERS

# GUI BINDS
def gui_show_ctrl(event):
	"Show the controls when fullscreened"
	global gwin_abs_x, gwin_abs_y
	global gframe_width, gframe_height

	if (gis_full_scr):
		if (gui_show_ctrl.is_shown == False):
			# show the controls by fitting the video
			# in the fullscreened frame
			show_ctrls(True)
			gwin_abs_x = win_gui.winfo_x()
			gwin_abs_y = win_gui.winfo_y()
			gframe_width = video_frame.winfo_width()
			gframe_height = video_frame.winfo_height()
			pl_resize()
			gui_show_ctrl.is_shown = True
		else:
			# return to fullscreen
			show_ctrls(False)
			gwin_abs_x = 0
			gwin_abs_y = 0
			gframe_width = 0
			gframe_height = 0
			pl_resize()
			gui_show_ctrl.is_shown = False
	return
# static flag
gui_show_ctrl.is_shown = False

def gui_vhide_on_minimize(event):
	"Hide video on gui minimize event"
	player_do(HIDE_VIDEO)

def gui_vshow_on_unminimize(event):
	"Show vide when gui window is unminimized"
	player_do(UNHIDE_VIDEO)

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
		if (start_player()):
			pl_resize()
			win_gui.after(CALLBACKT, update_player)

def b_stop_press():
	"Stop player only"
	pl_exit()

def b_quit_press():
	"Quit everything"
	pl_exit()
	win_gui.quit()

def mouse_wheel(event):
	"+/- volume with the wheel"
	if event.num == 5 or event.delta == -120:
		pl_decr_vol()
	if event.num == 4 or event.delta == 120:
		pl_incr_vol()
# /GUI BINDS

# GUI
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
video_frame = Frame(win_gui, bg="black")
video_frame.pack(side="top", fill="both", expand=True)
video_frame.bind("<Configure>", frame_on_resize)
video_frame.bind("<Double-Button-1>", gui_kbd_fscr)

# the frame holding the time and progress bar
time_frame = Frame(win_gui)
time_frame.pack(side="top")

# the progress bar
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
b_stop.pack(side="left")

# register what to do when 'x' is clicked
win_gui.protocol("WM_DELETE_WINDOW", b_quit_press)

gis_gui_running = True
if (start_player()):
	win_gui.after(CALLBACKT, update_player)
win_gui.mainloop()
gis_gui_running = False
# /GUI
