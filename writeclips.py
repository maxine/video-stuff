from moviepy.editor import *
from configparser import SafeConfigParser

parser = SafeConfigParser()
test = parser.read('video-data.ini')

#concatClip = [i for i in range(len(parser.sections()))]

holdVideo = None
finalVideo = None

holdText = None
finalText = None

textList = [i for i in range(len(parser.sections()))]
def writeClips():
	global holdVideo
	global finalVideo
	global holdText
	global finalText

	i = 0
	for m in parser.sections():
		text = parser.get(m, 'clip_text')
		#print(type(text))
		media = parser.get(m, 'media_link')
		#print(type(media))
		fSize = parser.getint(m, 'font_size')
		#print(type(fSize))
		fColor = parser.get(m, 'font_color')
		#print(type(fColor))
		textSpot = parser.get(m, 'text_location')
		#print(type(textSpot))
		clipStart = parser.getint(m, 'start_time')
		#print(type(clipStart))
		clipEnd = parser.getint(m, 'end_time')
		#print(type(clipEnd))
		duration = clipEnd - clipStart
		#print(type(duration))


		txt_clip = TextClip(text,fontsize=fSize,color=fColor, size=(1280, 720))
		txt_clip = txt_clip.set_pos(textSpot).set_duration(10)
		textList[i] = txt_clip
		i += 1
	textList[0].write_videofile("textonly.mp4", fps=12, codec='libx264')


		#if holdText == None:
		#	holdText = txt_clip
		#	finalText = txt_clip
		#	txt_clip = None
		#else:
		#	holdText = finalText
		#	finalText = concatenate_videoclips(holdText, txt_clip)
		#print(finalText)

		#videoClip = VideoFileClip(media).subclip(clipStart, clipEnd)
		#if holdVideo == None:
			#holdVideo = videoClip
			#finalVideo = videoClip
			#videoClip = None
			##holdVideo.write_videofile("yeahtest.mp4")
		#else:
			#holdVideo = finalVideo
			#finalVideo = concatenate_videoclips(holdVideo, videoClip)
		
	#video = CompositeVideoClip([finalVideo, finalText])
	#video.write_videofile("yeahtest.mp4")
		
writeClips()



#holdVideo.write_videofile("yeahtest.mp4")

#print(concatClip)
#video = concatenate_videoclips(concatClip)

#took out duration in txt_clip = txt_clip.set_pos(textSpot)
#used to be: txt_clip = txt_clip.set_pos(textSpot).duration(duration)