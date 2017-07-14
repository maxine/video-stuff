from moviepy.editor import *
from configparser import SafeConfigParser

parser = SafeConfigParser()
test = parser.read('video-data.ini')

#concatClip = [i for i in range(len(parser.sections()))]

holdVideo = None
finalVideo = None
def writeClips():
	for m in parser.sections():
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		fSize = parser.getint(m, 'font_size')
		fColor = parser.get(m, 'font_color')
		textSpot = parser.get(m, 'text_location')
		clipStart = parser.getint(m, 'start_time')
		clipEnd = parser.getint(m, 'end_time')
		duration = clipStart - clipEnd

		global holdVideo
		global finalVideo

		clip = VideoFileClip(media).subclip(clipStart, clipEnd)
		txt_clip = TextClip(text,fontsize=fSize,color=fColor)
		txt_clip = txt_clip.set_pos(textSpot).set_duration(10)
		videoClip = CompositeVideoClip([clip, txt_clip])

		if holdVideo == None:
			holdVideo = videoClip
			finalVideo = videoClip
			videoClip = None
			#holdVideo.write_videofile("yeahtest.mp4")
		else:
			holdVideo = finalVideo
			finalVideo = concatenate_videoclips(holdVideo, videoClip)
			finalVideo.write_videofile("yeahtest1.mp4")
			videoClip = None
		
	#holdVideo.write_videofile("yeahtest.mp4")
		
writeClips()



#holdVideo.write_videofile("yeahtest.mp4")

#print(concatClip)
#video = concatenate_videoclips(concatClip)

#took out duration in txt_clip = txt_clip.set_pos(textSpot)
#used to be: txt_clip = txt_clip.set_pos(textSpot).duration(duration)