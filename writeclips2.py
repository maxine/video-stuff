# Import requirements
from moviepy.editor import *
from configparser import SafeConfigParser

#Read configuration file
parser = SafeConfigParser()
parser.read('video-data.ini')

#Global variables to hold text and video sub-clips
textList = [i for i in range(len(parser.sections()))]
videoList = [i for i in range(len(parser.sections()))]

#Cleaned-up version of original writeClips() function
def writeClips2():
	#Global list indexers
	i = 0
	j = 0

	for m in parser.sections():
		#Set all variables via configuration file
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		fSize = parser.getint(m, 'font_size')
		fColor = parser.get(m, 'font_color')
		textSpot = parser.get(m, 'text_location')
		clipStart = parser.getint(m, 'start_time')
		clipEnd = parser.getint(m, 'end_time')
		textDuration = clipEnd - clipStart

		#Make the text asset for each video in the config file
		txt_clip = TextClip(text,fontsize=fSize,color=fColor, size=(1280, 720))
		txt_clip = txt_clip.set_pos(textSpot).set_duration(textDuration)
		textList[i] = txt_clip
		i += 1

		#Make the video asset for each video in the config file
		vid_clip = VideoFileClip(media).subclip(clipStart, clipEnd)
		videoList[j] = vid_clip
		j += 1

	#Put together individual text/video clips into one successive text or video clip
	textVid = concatenate_videoclips(textList)
	videoVid = concatenate_videoclips(videoList)
	#videoVid = concatenate_videoclips([videoList[0], videoList[1]])

	#Overlay concatenated text clip onto concatenated video clip and output the file
	video = CompositeVideoClip([videoVid, textVid])
	video.write_videofile("textonly.mp4", fps=12, codec='libx264')

writeClips2()


#args

#python syntax for passing in general args
	#fxn(arg1, arg2, keyword_arguments) (args are ordered and expected in a 

#kwargs are kyword arguments that don't necessarily have to be passed in bc they have
#a default argument

#whereas a1 and a2 are generic args, kword_arguments are named and when passed in
#are redefined
#*args and **qwargs --> any leftover parameters given by the inputter can be passed into these



#*clips would take an arbitrary list of clips --> doesn't take a list anymore, just takes clips
#so if you wanna pass in a list you have to put a star in front of it




#in hypothetical pass in -- > list comprehension (ex: map)
#fxn of x for x in list is another example of this --> equivalent of doing
#a for x in list and then calling 
#


#other things: dictionary comprhensio for iterating over entire ditionary
#dictionaries and lists are THE data strructs in Python

#map
