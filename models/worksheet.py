def wsread_question(page_body, page):
	return page

def wsread_page(page ):
    import re
    page_body=page.body
    worksheet= db(db.plugin_wiki_tag.name=="WorkSheet").select().first()
    if(worksheet!=None):
      if(page.tags=="|"+str(worksheet.id)+"|"):
	#replace Answer with textbox
	return page.body
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
	logging.warn('here')
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

#  else do wiki pages  last

    query = (db.plugin_wiki_page)
    pages=db(query).select(orderby="slug DESC")
 
    for pageslug in pages:

        		if(pageslug.slug!=page.slug):
        	    	   page_slug=re.sub('_',' ',pageslug.slug)
        	    	   pCap  = re.compile('\\b'+page_slug+'\\b')
        	    	   pSmall = re.compile('\\b'+page_slug.lower()+'\\b')
        	     	   words=re.split(r"(<a.*?</a>)",page_body)
        	    	   i=0
        	    	   page_body=""
        	    	   while i<len(words):
        	        	substitute = '<a href="/Bundjalung/plugin_wiki/page/'+pageslug.slug+'">'+page_slug+'</a>'
        	        	words[i]= pCap.sub(substitute,words[i])
        	        	if(pCap!=pSmall):
        	                   substitute = '<a href="/Bundjalung/plugin_wiki/page/'+pageslug.slug+'">'+page_slug.lower()+'</a>'
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
    logging.warn(fullpath)
    response.stream(os.path.join(request.folder,fullpath))
 
