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
 