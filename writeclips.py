from moviepy.editor import *
from configparser import SafeConfigParser

parser = SafeConfigParser()
test = parser.read('video-data.ini')

concatClip = [i for i in range(len(parser.sections()))]

def writeClips():
	for m in parser.sections():
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		fSize = parser.get(m, 'font_size')
		fColor = parser.get(m, 'font_color')
		textSpot = parser.get(m, 'text_location')
		clipStart = parser.get(m, 'start_time')
		clipEnd = parser.get(m, 'end_time')
		duration = clipStart - clipEnd

		clip = VideoFileClip(media).subclip(clipStart, clipEnd)
		txt_clip = TextClip(text,fontsize=fSize,color=fColor)
		txt_clip = txt_clip.set_pos(textSpot).set_duration(10)
		videoClip = CompositeVideoClip([clip, txt_clip])
		concatClip[i] = videoClip

print(concatClip)
#video = concatenate_videoclips(concatClip)
#video.write_videofile("yeahtest.mp4")

#NEXT TIME: GET VIDEO TO RENDER
#error won't render video because "Traceback (most recent call last):
 # File "writeclips.py", line 27, in <module>
  #  video = concatenate_videoclips(concatClip)
 # File "/Users/mwhitely/.virtualenvs/ffmpeg2/lib/python3.6/site-packages/moviepy/video/compositing/concatenate.py", line 71, in concatenate_videoclips
  #  tt = np.cumsum([0] + [c.duration for c in clips])
 # File "/Users/mwhitely/.virtualenvs/ffmpeg2/lib/python3.6/site-packages/moviepy/video/compositing/concatenate.py", line 71, in <listcomp>
  #  tt = np.cumsum([0] + [c.duration for c in clips])
#AttributeError: 'int' object has no attribute 'duration'"