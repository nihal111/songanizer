import os
import eyed3
import subprocess
import subprocess
import mechanize

br = mechanize.Browser()
filename="a.mp3"
apikey="v6m4z1dh"

p = subprocess.Popen(['fpcalc',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
#print out

a = out.find("DURATION", 0,40) +9
b = out.find("FINGERPRINT", 0 ,40)-1

duration = out[a:b]
fingerprint = out[b+13:-1]

url = 'http://api.acoustid.org/v2/lookup?client='+apikey+'&meta=recordings+releasegroups+compress&duration='+duration+'&fingerprint='+fingerprint
url = 'http://www.azlyrics.com/lyrics/metallica/theunforgivenii.html'
info= br.open(url).read()
print info


'''
artistindex1= info.find("name")
artistindex2= info.find("\"",artistindex1+8)
albumindex1= info.find("Album")
albumindex1= info.find("title",albumindex1)+9
albumindex2= info.find("\"",albumindex1)
titleindex1 = albumindex2 + 15
titleindex2 = info.find("\"",titleindex1)
artist = info[(artistindex1+8):artistindex2]
album = info[albumindex1:albumindex2]
title =info[titleindex1:titleindex2]



print artist
print album
print title

mp3 = eyed3.load('/home/nihal/Desktop/a.mp3')
mp3.tag.artist = unicode('badass', "UTF-8")
mp3.tag.album = unicode('#3', "UTF-8")
mp3.tag.recording_date=2012
mp3.tag.title = u"Hall of fame"
mp3.tag.genre= u"Rock"
mp3.tag.save()
'''