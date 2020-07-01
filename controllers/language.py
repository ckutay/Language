import string

# NOte the existence of languageList!=None means this is part of dictinary interface
langaugeList=language
@auth.requires_login()
def index():
    
        words=dblanguage(languagewords.id>0).select( orderby=languagewords.English)

    	return dict(words=words)


#FIXME language dependant
import os
import ftfy

def fix_word(word):

    word.Comment=fix_bad_unicode(word.Comment.strip())
    word.Gold_Coast_Tweed=fix_bad_unicode( word.Gold_Coast_Tweed.strip())
    word.Lower_Richmond=fix_bad_unicode(word.Lower_Richmond.strip())
    word.Middle_Clarence=fix_bad_unicode( word.Middle_Clarence.strip())
    word.Condamine_Upper_Clarence=fix_bad_unicode(word.Condamine_Upper_Clarence.strip())
    word.Copmanhurst=fix_bad_unicode(   word.Copmanhurst.strip())

    return word

def translateunicode():
    s=None
    t=None
    if (request.vars):
	    text=request.vars.text_input
	    s=unicode(text,'UTF-8')
	    t=ftfy.fix_text_encoding(s)
    return dict(string=s, translate=t)

def  fix_bad_unicode(text):
    s=unicode(text,"UTF-8")
    s=ftfy.fix_text_encoding(s)
    return s

def search(orderbys, searchterm,typequery, dialect, extra):
    words=None
    queryexact=""
    if typequery=="English":
    		queryexact=(dblanguage.Bundjalung.Search_English==searchterm)|dblanguage.Bundjalung.Search_English.startswith(searchterm+' ;')|dblanguage.Bundjalung.Search_English.startswith(searchterm+',')|(dblanguage.Bundjalung.Search_English.contains("; "+searchterm+' ' ))|(dblanguage.Bundjalung.Search_English.endswith("; "+searchterm))
    elif typequery==language:
                queryexact= dblanguage.Bundjalung.Language_Word==searchterm
    else:
		queryexact= dblanguage.Bundjalung.Category==searchterm
    query=queryexact
    if extra!="Exact":
	 if typequery=="English":
		query= dblanguage.Bundjalung.Search_English.contains(searchterm)
	 elif typequery==language:
	        query= dblanguage.Bundjalung.Language_Word.contains(searchterm)
	 else:
		query= dblanguage.Bundjalung.Category.contains(searchterm)
    if dialect!="All":
	if dialect=="Middle Clarence":
		query=query&(dblanguage.Bundjalung.Middle_Clarence!="")
	elif dialect=="Condamine Upper Clarence":

		query=query&(dblanguage.Bundjalung.Condamine_Upper_Clarence!="")
	elif dialect=="Lower Richmond":
		 query=query&(dblanguage.Bundjalung.Lower_Richmond!="")
	elif dialect=="Gold Coast Tweed":
		 query=query&(dblanguage.Bundjalung.Gold_Coast_Tweed!="")
	else:	
		query=query&(dblanguage.Bundjalung.Copmanhurst!="")
   #check not uncertain origina
    query = query & (dblanguage.Bundjalung.uncertain==0)
    words=dblanguage(query).select(orderby=orderbys)
    if extra!="Exact":
	exactwords=dblanguage(queryexact).select(orderby=orderbys)
	words.exclude(lambda r: r in exactwords)
    return words


def lesson():
    import json
    index=0
    name=None
    try:
 	    name=request.args[0]
    except:
 	    name=None
    words=[]
    if name and name!="all":
        page_id=db(db.plugin_wiki_page.slug==name).select()
       # logging.warn(page_id)
        try:
		wl=wordList(page_id[0].id)
       # logging.warn(wl)
	except:
		return response.json (None)	
    else: #full list not lesson
        wl=wordDict()

    if wl:
            for word in wl['words']:
		index+=1
	#too many words
		if index>100:
			return response.json (words)
		for row in dblanguage(dblanguage.Bundjalung.Language_Word==word.Language_Word).select():
			word=row
		word,examples=read_word(word)
		word.dialect=""
		try:
			if word.Comment: pass;
		
		except : word.Comment=""	
	        colour="black"
        	try:

		   if word.Gold_Coast_Tweed.strip() !="":
                	word.dialect+="Gold Coast Tweed, "
        	   if word.Lower_Richmond.strip()!="":
                	word.dialect+="Lower Richmond, "

        	   if word.Middle_Clarence.strip()!="":
                	word.dialect+="Middle Clarence, "

        	   if word.Condamine_Upper_Clarence.strip()!="":
                	word.dialect+="Condamine Upper Clarence, "

        	   if word.Copmanhurst.strip()!="":
                	word.dialect+="Copmanhurst "
           	except:
			pass
		condition = dblanguage.BundjalungExamples.language_id==word.id
       		#repeating from above?
		examples=dblanguage(condition).select(dblanguage.BundjalungExamples.ALL)
		exampleList=[]
           	for example in examples:
			try:
                		exampleList.append({"ex": example.Language, "ft": example.English})
			except Exception:
				pass
           	pub=False
		try:
			if word.uncertain>0 : pub=False
           		else: pub=True
		except:
			word.uncertain=1
           	try:
		  if word.Language_Word:
                	wordTrans={"def": word.English , "examples":exampleList,"ge": word.Search_English, "ps": word.Part_of_Speech}
                except:
                        wordTrans={}
 		try:
		#	logging.warn(word)
			words.append({"initial": word.Language_Word[0].lower(),"lx":word.Language_Word,"image": word.Image, "sound": word.Sound,"lxc": word.Comment, "publish": pub , "ge":word.English, "senses": wordTrans, "dialect": word.dialect})
		except AttributeError as errore:
			logging.warn(error)
	    return response.json (words)

    else: 
	wl=None
        name=name.replace(" ","_")
      
	w = db.plugin_wiki_page
    	
    	name_id=w(page.slug==name).select()
        words=dblanguage(dblanguage.Bundjalung.topics.page_id==name_id).select()
        rows = [word for word in words]
 #
 #	words=dblanguage(dblanguage.Bundjalung.Lesson==name).select()
 #    	rows = [word for word in words]
     	#cols = [word for word in words.description]
    wordjson=[]
    for row in words:
     		wordjson.append(row)

    return dict(wordlist=wordjson)


def wordDict ():

     wordlist=None
     try:
               wordlist=dblanguage(dblanguage.Bundjalung.id>0).select()
     except:
         pass
     return dict(words=wordlist)

def dictionary():
    names = db(db.dialect.id>0).select(db.dialect.name)
    numerics=[]
    dialectid=None
    alphanumeric="Exact"
    sort=request.vars['type']
    order=sort
    orderbys=dblanguage.Bundjalung.Search_English
    if order==language:
                orderbys=dblanguage.Bundjalung.Language_Word
    elif order=='Category':
                orderbys=dblanguage.Bundjalung.Category

    searchterms=request.vars['query']
    if searchterms=="None":
    	searchterms=""
    try:
	alphanumeric=request.vars['numeric']
    	dialectid=request.vars['dialect']
    except:
	pass
    exact=alphanumeric 
    dialect=""
    wordlist=[]
    if dialectid: 
	for name in names:
		if dialectid in name.name:
			dialect=name.name
    if searchterms and searchterms!="":
        response.start=False	
	wordlist =search(orderbys,searchterms,sort,dialect,alphanumeric)
	if order=="Category":
                numerics=["food","location","body_part","language","senses","time","fish","natural_environment","insect", "plant","artifact", "people","animal","bird",""]
                if (not alphanumeric in numerics):
                        alphanumeric=searchterms

	else:
		numerics=['Exact','Related']
		exact="Exact"	
	if (not wordlist) or wordlist==[]:
		wordlist =search(orderbys, searchterms,sort,dialect,'Related')
    else:
    	wordlist=[]
    	if (not(sort)):
 		sort="English"
	if (not alphanumeric or alphanumeric==""):
		alphanumeric='A'
    	if order=="Category":
 		numerics=["food","location","body_part","language","senses","time","fish","natural_environment","insect", "plant","artifact", "people","animal","bird",""]
		if (not alphanumeric in numerics):
		# queyr and sort is the same
                        alphanumeric='Exact'

	elif(sort=='English'):
		numerics=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		condition = dblanguage.Bundjalung.Search_English.startswith(alphanumeric.lower())|dblanguage.Bundjalung.Search_English.startswith('-'+alphanumeric.lower())

	        wordlist=dblanguage(condition).select(orderby=orderbys)
	else:
		numerics=['A','BA','BE','BI', 'BU','D','J','L','M','N','NG','NY','O','S','WA', 'WE', 'WI', 'WU','YA','YE','Yi','YU']
		if (not alphanumeric in numerics):
			alphanumeric="A"
		condition = dblanguage.Bundjalung.Language_Word.startswith(alphanumeric.lower())|dblanguage.Bundjalung.Language_Word.startswith('-'+alphanumeric.lower())
		if alphanumeric=='N':
			c2= (dblanguage.Bundjalung.Language_Word.startswith("na"))
			c3=(dblanguage.Bundjalung.Language_Word.startswith("ne"))
			c4=(dblanguage.Bundjalung.Language_Word.startswith("ni"))
			c5= (dblanguage.Bundjalung.Language_Word.startswith("nu"))
        		wordlist=dblanguage(c2|c3|c4|c5).select(dblanguage.Bundjalung.ALL, orderby=orderbys)
			wl2=dblanguage(c3).select(dblanguage.Bundjalung.ALL, orderby=orderbys)
	 	else:
			wordlist=dblanguage(condition).select(orderby=orderbys)
    for word in wordlist:
	read_word(word)
    if order=='Dialect':
	#this is so cool
	wordlist=sorted(wordlist,key= lambda word: word['dialect'])		
    else:
	#sort words by sound - only added now
	
    	wordlist=sorted(wordlist,key=lambda word: word['Sound'],reverse=True)


    top_message = language +" Dictionary"
    w = db.plugin_wiki_page
    page = w(slug='usedictionary')    
    if page: pageteaser=page.summary
    else: pageteaser=""
    return dict(start=response.start, page=pageteaser, dialect= dialect, sort=sort, exact=exact, names=names, query=searchterms, words=wordlist, top_message=top_message, numeric= alphanumeric, numerics=numerics)


def wordList(topic_id):
     wordlist=None
     try:
         wordlist=db(db.topics.page_id==topic_id).select()
     except:
         pass
     return dict(words=wordlist)

def translate_old():
    word = request.args(0) or ''
    if not request.args:
        redirect(URL(r=request, c='language' ,f='index'))
    lang= request.args(1)

    if lang=='English':
	words=(languagewords.id>0)(languagewords.Search_English==word).select( orderby=languagewords.language)
    elif not lang: 
	lang=language
	words=(languagewords.id>0)(languagewords.language==word).select( orderby=languagewords.Search_English)
	
    return  dict(words=words)

def translate():
     import json
     searchterm=None
     try:
         searchterm=request.args[0]
 	 lang=request.args[1]
     except:
         pass
     if searchword:
         if lang=="English" :
                 query=(dblanguage.Bundjalung.Search_English==searchterm)|dblanguage.Bundjalung.Search_English.startswith(searchterm+' ;')|dblanguage.Bundjalung.Search_English.startswith(searchterm+',')|(dblanguage.Bundjalung.Search_English.contains("; "+searchterm+' ' ))|(dblanguage.Bundjalung.Search_English.endswith("; "+searchterm))
         words=[]
         page_id=dblanguage(dblanguage.English==name).select()
         #logging.warn(page_id)
         wl=wordList(page_id[0].id)
         #logging.warn(wl)
         if wl:
                 for word in wl['words']:
 
                         words.append({"English":word.English,"Language_Word":word.Language})
         else: wl=None
         wordlist=[]
         for row in words:
                 word_json=row
                 wordlist.append(word_json)
 
     return dict(wordlist=wordlist)


def dictionarysort():
    sort=request.args(0)
    if(sort==None):sort='English'
    wordlist=dblanguage(dblanguage.Bundjalung.Category==sort).select(dblanguage.Bundjalung.ALL, orderby=dblanguage.Bundjalung.Language_Word)
    for word in wordlist:
        read_word(word)
    top_message = language +" List sorted for "+sort
    return dict(words=wordlist, top_message=top_message)


def view_word():
    word_id=request.args(0)
    words=dblanguage.Bundjalung
    word, examples=read_word(dblanguage.Bundjalung(dblanguage.Bundjalung.id==word_id))
    word=fix_word(word)
    link=None

    link = URL(r=request, c='language' ,f='edit_word', args=word_id)

    related = []
    if word.RelatedWord:

        relates=word.RelatedWord.split(',')
        for relate in relates:
                relate=relate.strip()
                relateid=dblanguage.Bundjalung(dblanguage.Bundjalung.Language_Word.like( "%%%s%%" %relate, case_sensitive=False))
                if relateid:
                        relateid=relateid.id
                        relate=A(relate,_target="_blank",_href="/language/view_word/"+str(relateid))
                related.append(relate)
    relatenew=dblanguage(dblanguage.Bundjalung.English.like( "%%%s%%" %word.English, case_sensitive=False))
    if relatenew:
            related.append(BR()+"With same English translation:")
            for relate in relatenew.select():
                if str(relate.id)!=word_id:
			relateid=relate.id
                	relate=A(relate.Language_Word,_target="_blank",_href="/language/view_word/"+str(relateid))
                	related.append(relate)
    return dict(link = link, word=word, related=related,exampleSentences=examples, language=language )

def view_word_popup():
    word_id=request.args(0)
    words=dblanguage.Bundjalung
    word,examples =read_word(dblanguage.Bundjalung(dblanguage.Bundjalung.id==word_id))
    word=fix_word(word)
    link = URL(r=request, c='language' ,f='edit_word', args=word_id)
    return dict(link = link, word=word)



def category():

    word = request.args(0) or ''
    if not request.args:
        redirect(URL(r=request, c='language' ,f='index'))
    category= request.args(1)

    words=(languagewords.id>0)(languagewords.Category==category).select( orderby=languagewords.language)

    return  dict(words=words)

@auth.requires_login()
def create_word():
    if not request.args:
        redirect(URL(r=request,c='language', f='index'))
    create_word = request.args(0)
    name=create_word.replace('_',' ')

    word=languageword(Search_English==name)
    form = crud.create(dblanguageword)
    return dict(word=word, form=form)

    
# edit clws
@auth.requires_login()
def edit_word():
    word_id=request.args(0)
    try:
        integer=True
        word_id=int(word_id)
    except :
        integer=False
	word_id=0
    try:
 	name=word_id.replace('_',' ')
    except: 
	name=""
    w = dblanguage.Bundjalung
    if integer:
	word = w(id=word_id)
    else:
	word = w(Language_Word=name)
    if not word:
        word = w.insert(Language_Word=name)
    word, examples =read_word(word)
    if word: 
	word_id=word.id
    	if auth.has_membership(auth.id_group('developer')):

	    form = crud.update(w, word, deletable=True, onaccept=crud.archive,
                       next=URL(r=request,c='language', f='view_word',args=word_id))
    	else:
            form = crud.update(w, word, deletable=False, onaccept=crud.archive,
                       next=URL(r=request,c='language', f='view_word',args=word_id))
    return dict(form=form,word=word,examples=examples)

def read_word(word):
	word.Sound=None
	try:
	  word.Sound=word.SoundFile	
	except:
		pass
	if (not word.Sound or word.Sound==''or word.Sound==" "): 
		
		parts= word.Language_Word.split(',')
		word.Sound=parts[0]+".mp3"
		#word.Sound=word.Language_Word+".mp3"
        	if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+word.Sound)):
	    		word.Sound = URL(r=request, c='default',f='sounds', args=word.Sound)
        	else:
			
	   		if (not word.Sound or word.Sound==''): 
				word.Sound=parts[0]+".wav"
           		if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+word.Sound)):
				word.Sound = URL(r=request, c='default',f='sounds', args=word.Sound)
	   		else: word.Sound=None
	#add transcript sound
	try:	
		word.Image=word.Image.strip()
		word.ImageLink=word.Image
		if(word.Image==None or word.Image==""):word.Image=word.Search_English
		end=string.find(word.Image,';');
		if end>0:word.Image=word.Image[0:end]
		word.Image=word.Image.strip('(generic)')
        	word.Image.strip()
		word.Image=word.Image.replace(', ','_')

		word.Image=word.Image.replace(' ','_')
		word.Image.strip()
        	if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.gif')):
                	word.ImageLink = URL(r=request, c='default',f='images', args=word.Image+'.gif')
        	else: word.ImageLink=""
        	if(word.ImageLink==""):
                	if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.jpg')):
				word.ImageLink = URL(r=request, c='default',f='images', args=word.Image+'.jpg')
                	else: word.Image=""
	except:
		word.Image=""
	condition = dblanguage.BundjalungExamples.language_id==word.id
        examplelist=dblanguage(condition).select(dblanguage.BundjalungExamples.ALL)
	word.dialect=""
	colour="black"
	try:
	  if word.Gold_Coast_Tweed.strip() !="":
		word.dialect+="Gold Coast Tweed, "
	  if word.Lower_Richmond.strip()!="":
		word.dialect+="Lower Richmond, "

          if word.Middle_Clarence.strip()!="":
                word.dialect+="Middle Clarence, "

          if word.Condamine_Upper_Clarence.strip()!="":
                word.dialect+="Condamine Upper Clarence, "

          if word.Copmanhurst.strip()!="":
                word.dialect+="Copmanhurst "
#remove ','
	  word.dialect = word.dialect.strip()[:-1]
	  if word.dialect.strip()=="": word.dialect="All"
# if only one dialect
 	  if word.dialect!="" and word.dialect.find(',')<0:
		colour=db(db.dialect.name==word.dialect).select()
		if colour: word.color=colour[0].color
		else: word.color='black'
	  else:
		word.color='black'
	except:
	   pass
        return word, examplelist

