import os
import eyed3
from eyed3 import id3
import subprocess
import subprocess
import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#Robot error
apikey="v6m4z1dh"




filename="a.mp3"

flag=1
try:
	mp3 = eyed3.load(filename)
except:
	flag=0
if (flag==1):
	p = subprocess.Popen(['fpcalc',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	#print out

	a = out.find("DURATION", 0,40) +9
	b = out.find("FINGERPRINT", 0 ,40)-1

	duration = out[a:b]
	fingerprint = out[b+13:-1]
	url = 'http://api.acoustid.org/v2/lookup?client='+apikey+'&meta=recordings+releasegroups+compress&duration='+duration+'&fingerprint='+fingerprint
	#print url
	info= br.open(url).read()
	if(info.find("error")==-1):
		artistindex0=info.find("artist")
		artistindex1= info.find("name")+8
		artistindex2= info.find("\"",artistindex1)
		albumindex1= info.find("Album")
		albumindex1= info.find("title",albumindex1)+9
		albumindex2= info.find("\"",albumindex1)
		titleindex1 = albumindex2 + 15
		titleindex2 = info.find("\"",titleindex1)
		artist = info[(artistindex1):artistindex2]
		album = info[albumindex1:albumindex2]
		title =info[titleindex1:titleindex2]

		while ((artist=="Various Artists") and ((artistindex1+400)<len(info))):
			artistindex0=info.find("artist",artistindex2)
			artistindex1= info.find("name",artistindex0)+8
			artistindex2= info.find("\"",artistindex1)
			artist = info[(artistindex1):artistindex2]

		url = 'http://search.azlyrics.com/search.php?q='+artist+'+'+title
		url =url.replace(' ','+')

		br.open(url)

		links = []
		for link in br.links(url_regex="http://www.azlyrics.com/lyrics/"):
			links.append(link.url)
		if (len(links)):
			#print links[0]
			info= br.open(links[0]).read()
			albumindex1 = info.find("glyphicon-cd")
			if (albumindex1!=-1):		
				albumindex1 = info.find("collapse",albumindex1)+11
				albumindex2 = info.find("\"",albumindex1)
				yearindex1 = info.find("(",albumindex2)+1
				yearindex2 = info.find(")",albumindex2)
				album = info[albumindex1:albumindex2]
				year = (info[yearindex1:yearindex2])
				print album
				print year
				mp3.tag.album = unicode(album, "UTF-8")
				try:
					mp3.tag.recording_date=year
				except:
					print "date haga"

		print artist
		print title
		mp3.tag.artist = unicode(artist, "UTF-8")
		mp3.tag.title = unicode(title, "UTF-8")
		mp3.tag.save()
