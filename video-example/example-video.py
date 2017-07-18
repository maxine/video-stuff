# Import requirements
from moviepy.editor import *
from ConfigParser import SafeConfigParser
#from moviepy.video.fx.scroll import fadein
#from moviepy.video.fx.scroll import fadeout

#Read configuration file
parser = SafeConfigParser()
parser.read('example-data.ini')

#Global variables to hold text and video sub-clips
txt_clip_list = [i for i in range(len(parser.sections()))]
med_clip_list = [i for i in range(len(parser.sections()))]


audio_duration = 0
def audioLength():
	audioBegin = 0
	audioEnd = 0	
	for m in parser.sections():
		audioBegin += parser.getint(m, 'start_time')
		audioEnd += parser.getint(m, 'end_time')
		global audio_duration
		audio_duration = audioEnd - audioBegin
	return audio_duration



#Cleaned-up version of original writeClips() function
def writeClips():
	#Global list indexers for inside the for loop
	i = 0
	j = 0

	#Set constant variables - values that are true for all clips
	audio = parser.get('video0', 'video_audio')
	audio_bool = parser.getboolean('video0', 'audio_setting')
	audio_length = audioLength()
	vid_fps = parser.getint('video0', 'frames_per_second')
	vid_codec = parser.get('video0', 'video_codec')
	file_name = parser.get('video0', 'save_as')

	for m in parser.sections():
		#For each video, set all variables via configuration file
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		tSize = parser.getint(m, 'font_size')
		tColor = parser.get(m, 'font_color')
		textSpot = parser.get(m, 'text_location')
		clipStart = parser.getint(m, 'start_time')
		clipEnd = parser.getint(m, 'end_time')
		text_duration = clipEnd - clipStart

		#Make the text asset for each video in the config file
		txt_clip = TextClip(text, fontsize=tSize,color=tColor, size=(1280, 720))
		txt_clip = txt_clip.set_pos(textSpot).set_duration(text_duration).fadein(.35).fadeout(.35)
		txt_clip_list[i] = txt_clip
		i += 1

		#Make the video asset for each video in the config file
		med_clip = VideoFileClip(media).subclip(clipStart, clipEnd).fadein(.35).fadeout(.35)
		med_clip_list[j] = med_clip
		j += 1

	#Put together individual text/video clips into one successive text or video clip
	text_vid = concatenate_videoclips(txt_clip_list)
	media_vid = concatenate_videoclips(med_clip_list)
	audioclip = AudioFileClip(audio).set_duration(audio_length, change_end=True)

	#Overlay concatenated text clip onto concatenated video clip and output the final video
	video = CompositeVideoClip([media_vid, text_vid])
	video = video.set_audio(audioclip)
	video.write_videofile("knight_lab.mp4", fps=vid_fps, codec=vid_codec, audio=audio_bool)

writeClips()
