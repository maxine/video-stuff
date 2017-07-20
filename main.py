# Import requirements
from moviepy.editor import *
from ConfigParser import SafeConfigParser
import struct
import imghdr
import re

#Read configuration files
parser = SafeConfigParser()
parser.read('video-data.ini')
text_parser = SafeConfigParser()
text_parser.read('fonts.ini')

#GLOBAL VARIABLES 
#Lists to hold text and video sub-clips
#txt_clip_list = [i for i in range(len(parser.sections()))]
med_clip_list = [i for i in range(len(parser.sections()))]


#NOT YET IMPLEMENTED. Will return desired text scale based on video aspect ratio
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


#NOT YET IMPLEMENTED. Will scale text size depending on aspect ratio
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


#MAY BE DEPRECATED if we opt to use size in ComposeVideoClip.
#Makes a still image with specified size and color to be stacked at the bottom of a composited
#media clip as the "canvas" of the larger video composition. Ensures even sizing. 
def videoSize():
	aspect_ratio = parser.get('video0', 'aspect_ratio')
	bkgd_color = parser.get('video0', 'background_color')

	if aspect_ratio == "16:9":
		bkgd = ColorClip((1080, 720), color=[30,43,23])
	if aspect_ratio == "1:1":
		bkgd = ColorClip((1280, 1280), color=[30,43,23])
	if aspect_ratio == "4:5":
		bkgd = ColorClip((864, 1080), color=[30,43,23])
	return bkgd


#Returns a tuple of (width, height) of an image/gif. Doesn't work for videos.
def get_image_size(fname):
	'''Determine the image type of fhandle and return its size. from draco'''
	with open(fname, 'rb') as fhandle:
		head = fhandle.read(24)
		if len(head) != 24:
			return
		if imghdr.what(fname) == 'png':
			check = struct.unpack('>i', head[4:8])[0]
			if check != 0x0d0a1a0a:
				return
			width, height = struct.unpack('>ii', head[16:24])
		elif imghdr.what(fname) == 'gif':
			width, height = struct.unpack('<HH', head[6:10])
		elif imghdr.what(fname) == 'jpeg':
			try:
				fhandle.seek(0) # Read 0xff next
				size = 2
				ftype = 0
				while not 0xc0 <= ftype <= 0xcf:
					fhandle.seek(size, 1)
					byte = fhandle.read(1)
					while ord(byte) == 0xff:
						byte = fhandle.read(1)
					ftype = ord(byte)
					size = struct.unpack('>H', fhandle.read(2))[0] - 2
				# We are at a SOFn block
				fhandle.seek(1, 1)  # Skip `precision' byte.
				height, width = struct.unpack('>HH', fhandle.read(4))
			except Exception: #IGNORE:W0703
				return
		else:
			return
		return width, height


#Defines which axis to scale a picture/gif by.
def scaleImage(a):
	image_size = get_image_size(a)
	x = image_size[0]
	y = image_size[1]

	if x > y:
		return "horizontal"
	if (y > x) or (y == x):
		return "vertical"


#makes a gif clip
def makeGif(med, length):
	med_clip = VideoFileClip(med, audio=False).loop(duration = length)
	return med_clip


#makes an image clip
def makeImage(med, length):
	if scaleImage(med) == "horizontal":
		med = ImageClip(med, duration = length)
		med_clip = med.resize(width=1080)
		return med_clip
	if scaleImage(med) == "vertical":
		med = ImageClip(med, duration = length)
		med_clip = med.resize(height=720)
		return med_clip


#makes a video clip
def makeVideo(med, start, length):
	med_clip = VideoFileClip(med, audio=False).subclip(start, length).fadein(.35).fadeout(.35)
	return med_clip

#print(makeVideo('video-example/example-media/kl_welcome.mp4', 0, 10))
#Reads inputted media type and calls proper "make" function for type
def makeMedia(med, start, length):
	imgPattern = ['.png', '.tiff', '.jpeg']
	vidExt = ['.ogv', '.mp4', '.mpeg', '.avi', '.mov']

	if '.gif' in  med:
		med_clip = makeGif(med, length)
	if any(ext in med for ext in imgExt):
		med_clip = makeImage(med, length)
	if any(ext in med for ext in vidExt):
		med_clip = makeVideo(med, start, length)
	else:
		return
	return med_clip


#Makes individual text, media, and audio clips and then stitches them into one video
def compileVideo():
	#Global list indexers for inside the for loop
	i = 0
	#j = 0

	#CONSTANT VARIABLES - values that apply to the entire video
	#Text
	tColor = parser.get('video0', 'text_color')
	tHighlight = parser.get('video0', 'text_highlight_color')
	tSize = parser.getint('video0', 'text_size')
	tBackground = parser.get('video0', 'text_background')
	tFont = parser.get('video0', 'text_font')
	#Audio
	global_audio = parser.get('video0', 'video_audio')
	audio_length = audioLength()
	#File
	vid_fps = parser.getint('video0', 'frames_per_second')
	vid_codec = parser.get('video0', 'video_codec')
	file_name = parser.get('video0', 'save_as')

	for m in parser.sections():
		#For each video, set all variables via configuration file
		text = parser.get(m, 'clip_text')
		tAlign = parser.get(m, 'text_align')
		tPlace = parser.get(m, 'text_place')
		media = parser.get(m, 'media_link')
		clip_start = parser.getint(m, 'start_time')
		clip_end = parser.getint(m, 'end_time')
		text_duration = clip_end - clip_start

		#Make the text asset for clip m in the config file
		txt_clip = TextClip(text, font=tFont, fontsize=tSize, color=tColor)
		txt_clip = txt_clip.set_duration(text_duration).fadein(.35).fadeout(.35).set_position((tAlign,tPlace))		

		#Make the video/background asset for slide m in the config file
		med_clip = makeMedia(media, clip_start, text_duration).set_position("center", "center")
		#bkgd = videoSize().set_duration(text_duration)

		#compose text and video to create clip and put in list of completed clips
		video_clip = CompositeVideoClip([med_clip, txt_clip], size=(1080, 720))
		med_clip_list[i] = video_clip
		i += 1

	#concatenate all completed clips
	audio = AudioFileClip(global_audio).set_duration(audio_length)
	video = concatenate_videoclips(med_clip_list)

	#Set audio for entire video
	final_video = video.set_audio(audio)
	#write out final video 
	final_video.write_videofile(filename=file_name, fps=vid_fps, codec=vid_codec)

compileVideo()