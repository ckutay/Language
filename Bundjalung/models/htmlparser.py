from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class langHTMLParser(HTMLParser): 
    words=""
    import StringIO
    def __init__(self):
        HTMLParser.__init__(self)
 	#words=StringIO.StringIO()
    
    def handle_starttag(self, tag, attrs):
        self.words+=' <'+tag
        for attr in attrs:
	    if attr[1]!="":
                self.words+=' '+attr[0]+' = "'+attr[1]+'"'
            else:
                self.words+=' '+attr[0]+' '   
        self.words+=' > '
    def handle_endtag(self, tag):
        self.words+=" </"+tag+">"

    def handle_startendtag(self,tag, attrs):
	self.words+=" <"+tag
        for attr in attrs:
	    if attr[1]!="":
            	self.words+=' '+attr[0]+' = "'+attr[1]+'"'
	    else:
		self.words+=' '+attr[0]+' '	
	self.words+=" /> " 
    def handle_data(self, data):
        self.words+=self.handle_parse(data)
    def handle_comment(self, data):
        self.words+=" <!-- "+ data+" -->"
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.words+= c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.words+= c
    def handle_decl(self, data):
        self.words+=data
    def handle_pi(self, data):
        self.words+=" <?"+data+"> "
    def read_string(self):
#	contents = output.getvalue()
 #       output.close()
	return self.words

    def handle_parse(self,data):
        words=data.split()
	wordsfinal=""
	for word in words:
          	condition = dblanguage.Bundjalung.Search_English.startswith(word+',')

          	wordlist=dblanguage(condition).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.Search_English)
          	if not wordlist:
           		condition = dblanguage.Bundjalung.Search_English.startswith(word+' ')
           		wordlist=dblanguage(condition).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.Search_English)
           		if not wordlist:
                		condition = dblanguage.Bundjalung.Language_Word==word
                		wordlist=dblanguage(condition).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.Search_English)
	  	if wordlist:

            		sample=wordlist[0]
            		if (sample.SoundFile==None or sample.SoundFile==""):
                       		sample.SoundFile=sample.Language_Word+'.mp3'

            		sample.info='<b><i>'+sample.Language_Word+'</i></b><br>'+sample.Search_English
            		if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+str(sample.SoundFile))):
                		sample.Sound = URL(r=request, c='default',f='sounds', args=str(sample.SoundFile))
                		sample.info="DHTMLSound('"+str(sample.Sound)+"','"+str(sample.info)+"');"
                		substitute1='<a href="/Bundjalung/language/view_word/'+str(sample.id)+'" target="_blank" onMouseOver="'+str(sample.info)+'" > '+word+' </a> '
                		word= substitute1
            		else:
				sample.info="DHTMLText('"+str(sample.info)+"');"
                		substitute1='<a href="/Bundjalung/language/view_word/'+str(sample.id)+'" target="_blank" onMouseOver="'+str(sample.info)+'" > '+word+' </a> '

                	word=substitute1
          	else:
			word=word #no change
	  	wordsfinal+=word+' '
	return wordsfinal

parser = langHTMLParser()

