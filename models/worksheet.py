def wsread_question(page_body, page):
	return page

def wordlist(topic_id):
    wordlist=None
    try:
        wordlist=db(db.topics.page_id==topic_id).select()
    except:
        pass
    return dict(words=wordlist)

def wsread_page(page ):
    import re,os
    page_body=page.body
    worksheet= db(db.plugin_wiki_tag.name=="WorkSheet").select().first()
    if(worksheet!=None):
      if(page.tags=="|"+str(worksheet.id)+"|"):
	#replace Answer with textbox
	return page.body
<<<<<<< HEAD
#find sound and upload
    examples=os.listdir('applications/'+language+'/uploads/media/sounds')
    examples.sort(lambda x,y: -cmp(len(x), len(y)))
    r = re.compile(r'(<a.*?<\/a>)')
    for example in examples:
	if len(example.split(' '))>1:
	    text=os.path.splitext(example)[0]
	    if text in page_body:
		parags=r.split(page_body)
		paragraphs=""
	 	for parag in parags:	
			if parag.startswith('<a'):
				paragraphs+=parag
			else:
				Sound = URL(r=request, c='default',f='sounds', args=str(example))
	    			Info="DHTMLSound('"+str(Sound)+"','"+str(text)+"');"
				paragraphs+=parag.replace(text, '<a href="#" onMouseOver="'+str(Info)+'" > '+text+' </a> ')	
		page_body=paragraphs
    #parags=re.split(r'(<a.*?<\/a>)',page_body)
    #parser = langHTMLParser()

    #parser.feed(page_body)
    #words=parser.read_string()
# bypass    words=page_body	
    #page_body=words
=======
#find images and upload
    images=re.split(r"(<img.*?>)",page_body)

    if (len(images)>1):
        page_body=""
        for image in images:
            image_name=re.split(r'(src=".*?")',image)
            #image_name=image.split('src="')    
            if image_name!=image:
                image=""
                for image_n in image_name:
                        image_file=image_n.split('src="')
                        if(len(image_file)>1):

                                image_file=image_file[1].split('"')[0]
                                record=dblanguage(dblanguage.images.name==image_file).select().first()

                                if(record!=None):
                                        image_name=record.filename

                                        image_n='src="http://bundjalung.dalang.com.au/langdownload/'+image_name+'"'
                        image+=image_n
                page_body+=image
    parags=re.split(r"(<a.*?</a>)",page_body)
    page_body=""

    for words in parags:
     wordpara=words.split()
     for word in wordpara:
	condition = dblanguage.Bundjalung.English==word
	wordlist=dblanguage(condition).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.English)

	if not wordlist:
	        condition = dblanguage.Bundjalung.Language_Word==word
        	wordlist=dblanguage(condition).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.English)
	if wordlist:

	    sample=wordlist[0]
	    i=0
	    if (sample.SoundFile==None or sample.SoundFile==""):
                       sample.SoundFile=sample.Language_Word+'.mp3'

	    sample.info='<b><i>'+sample.Language_Word+'</i></b><br>'+sample.English
	    if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+str(sample.SoundFile))):
		sample.Sound = URL(r=request, c='default',f='filedownload/media/sounds', args=str(sample.SoundFile))
	        sample.info="DHTMLSound('"+str(sample.Sound)+"','"+str(sample.info)+"');"
	    	substitute1='<a href="/Bundjalung/language/view_word/'+str(sample.id)+'" target="_blank" onMouseOver="'+str(sample.info)+'" > '+word+' </a> '
		word= substitute1
	    else:
		sample.info="DHTMLSound('"+str(' ')+"','"+str(sample.info)+"');"

                substitute1='<a href="/Bundjalung/language/view_word/'+str(sample.id)+'" target="_blank" onMouseOver="'+str(sample.info)+'" > '+word+' </a> '

		word=substitute1
		i+=2

        page_body+=word+' '
>>>>>>> 5e27a4d7423724f1c023932db88ae5cfb1224b78

#  else do wiki pages  last
    query = (db.plugin_wiki_page)
    pages=db(query).select(orderby="title DESC")
 
    for pagetitle in pages:

        		if(pagetitle.title!=page.title):
        	    	   page_title=re.sub('_',' ',pagetitle.title)
        	    	   pCap  = re.compile('\\b'+page_title+'\\b')
        	    	   pSmall = re.compile('\\b'+page_title.lower()+'\\b')
        	     	   words=re.split(r"(<a.*?</a>)",page_body)
        	    	   i=0
        	    	   page_body=""
        	    	   while i<len(words):
        	        	substitute = '<a href="/Bundjalung/plugin_wiki/page/'+pagetitle.title+'">'+page_title+'</a>'
        	        	words[i]= pCap.sub(substitute,words[i])
        	        	if(pCap!=pSmall):
        	                   substitute = '<a href="/Bundjalung/plugin_wiki/page/'+pagetitle.title+'">'+page_title.lower()+'</a>'
        	                   words[i] = pSmall.sub(substitute,words[i])
        	        	i+=2
        	    	   for word in words:
        	        	page_body+=word
		
    return page_body

def answer(answer):
 	w = db.plugin_wiki_page
 	page = w(slug=request.arg[0])
	return dict(answer=answer, page=page) 

   
def wsimage():
    subdirectory = '/uploads/media/images/'# directory
    filename = request.args(0)
    fullpath = os.path.join(subdirectory, filename)
    if request.args(1):
            filenameadd = request.args(1)
            fullpath = os.path.join(fullpath, filenameadd)
    response.stream(os.path.join(request.folder,fullpath))
 
