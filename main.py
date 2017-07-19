# Import requirements
from moviepy.editor import *
from ConfigParser import SafeConfigParser

#Read configuration file
parser = SafeConfigParser()
parser.read('video-data.ini')

text_parser = SafeConfigParser()
text_parser.read('fonts.ini')

#GLOBAL VARIABLES 
#Lists to hold text and video sub-clips
txt_clip_list = [i for i in range(len(parser.sections()))]
med_clip_list = [i for i in range(len(parser.sections()))]


#Assigns user-specified font to a variable
user_font = "Comic Sans" #currently hard coded; this is where we read in user input 

#Defines text size based on video aspect ratio
def textSize():
	tScale = "size"
	aspect_ratio = parser.get('video0', 'aspect_ratio')

	if aspect_ratio == "1.3:1":
		tScale = "medium"
	if aspect_ratio == "16:9":
		tScale = "large"
	if aspect_ratio == "1:1":
		tScale = "small"
	return tScale

def scaleFonts():
	tSize = 0
	if tScale == "small":
		pass
	if tScale == "medium":
		pass
	if tScale == "large":
		pass
	return tSize

#Finds length of all inputted media to determine global audio track duration

def audioLength():
	audioBegin = 0
	audioEnd = 0
	audio_duration = 0
	for m in parser.sections():
		audioBegin += parser.getint(m, 'start_time')
		audioEnd += parser.getint(m, 'end_time')
	audio_duration = (audioEnd - audioBegin)
	return audio_duration

def sizeVideo():
	aspect_ratio = parser.get('video0', 'aspect_ratio')
	sizeX = 0
	sizeY = 0

	#if aspect_ratio == "1.3:1":
		#sizeX = 
		#sizeY = 
	#if aspect_ratio == "16:9":
		#sizeX = 1080
		#sizeY = 720
	#if aspect_ratio == "1:1":
		#sizeX = 1280
		#sizeY = 1280
	#if aspect_ratio == "4:5":
	#	sizeX = 864
	#	sizeY = 1080
	#return (sizeX, sizeY)


#Makes individual text, media, and audio clips and then stitches them into one video
def compileVideo():
	#Global list indexers for inside the for loop
	i = 0
	j = 0

	#CONSTANT VARIABLES - values that apply to the entire video
	#Text
	tColor = parser.get('video0', 'text_color')
	tHighlight = parser.get('video0', 'text_highlight_color')
	tSize = parser.getint('video0', 'text_size')
	tBackground = parser.get('video0', 'text_background')


	tFont = text_parser.get(user_font, 'text_font')

	#Audio
	global_audio = parser.get('video0', 'video_audio')
	audio_bool = parser.getboolean('video0', 'audio_setting')
	audio_length = audioLength()
	#File
	vid_fps = parser.getint('video0', 'frames_per_second')
	vid_codec = parser.get('video0', 'video_codec')
	file_name = parser.get('video0', 'save_as')

	for m in parser.sections():
		#For each video, set all variables via configuration file
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		tAlign = parser.get(m, 'text_align')
		tPlace = parser.get(m, 'text_place')
		clip_start = parser.getint(m, 'start_time')
		clip_end = parser.getint(m, 'end_time')
		text_duration = clip_end - clip_start

		#Make the text asset for clip m in the config file
		txt_clip = TextClip(text, font=tFont, fontsize=tSize, color=tColor)
		txt_clip = txt_clip.set_duration(text_duration).fadein(.35).fadeout(.35).set_position(("center","top"))		

		#Make the video asset for slide m in the config file
		med_clip = VideoFileClip(media).subclip(clip_start, clip_end).fadein(.35).fadeout(.35)

		#compose text and video to create clip m
		video_clip = CompositeVideoClip([med_clip, txt_clip])
		#add completed clip to list of clips
		med_clip_list[i] = video_clip
		#index for clip list
		i += 1

	#concatenate all completed clips
	video = concatenate_videoclips(med_clip_list)

	#Set audio for entire video
	audioclip = AudioFileClip(global_audio)#.set_duration(audio_length, change_end=True)
	video2 = video.set_audio(audioclip)
	#write out final video 
	video2.write_videofile("knight_lab.mp4", fps=vid_fps, codec=vid_codec, audio=audio_bool)


compileVideo()
