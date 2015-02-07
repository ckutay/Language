import string

# NOte the existence of languageList!=None means this is part of dictinary interface
langaugeList=language

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
    if extra=="Exact":
    	if typequery=="English":
    		query=(dblanguage.Bundjalung.Search_English==searchterm)|dblanguage.Bundjalung.Search_English.startswith(searchterm+' ;')|(dblanguage.Bundjalung.Search_English.contains("; "+searchterm ))|(dblanguage.Bundjalung.Search_English.endswith("; "+searchterm))
    	else:
                query= dblanguage.Bundjalung.Language_Word==searchterm
    else:
	 if typequery=="English":
		query= dblanguage.Bundjalung.Search_English.contains(searchterm)
	 else:
	        query= dblanguage.Bundjalung.Language_Word.contains(searchterm)

    if dialect!="All":
	if dialect=="Middle Clarence":
		query=query&(dblanguage.Bundjalung.Middle_Clarence!="")
	elif dialect=="Condamine_Upper_Clarence":
		 query=query&(dblanguage.Bundjalung.Condamine_Upper__Clarence!="")
	elif dialect=="Lower_Richmond":
		 query=query&(dblanguage.Bundjalung.Lower_Richmond!="")
	elif dialect=="Gold_Coast_Tweed":
		 query=query&(dblanguage.Bundjalung.Gold_Coast_Tweed!="")
	else:	
		query=query&(dblanguage.Bundjalung.Copmanhurst!="")
    words=dblanguage(query).select(orderby=orderbys)
    return words

def dictionary():
    names = db(db.dialect.id>0).select(db.dialect.name)
    numerics=[]
    dialectid=None
    alphanumeric=""
    sort=request.vars['type']
    if request.args:
        order=request.args[0]
    else:
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
    if dialectid: 
	dialectRow=db.dialect(name=dialectid)
    	if dialectRow: dialect=dialectRow.name
    if searchterms and searchterms!="":
        response.start=False	
	wordlist =search(orderbys,searchterms,sort,dialect,alphanumeric)
        numerics=['Exact','Related']	
	if wordlist==[]:
		wordlist =search(orderbys, searchterms,sort,dialect,'Related')

    else:
    	wordlist=[]
    	if (not(sort)):
 		sort="English"
	if (not alphanumeric):
		alphanumeric='A'
    	if(sort=='English'):
		numerics=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		condition = dblanguage.Bundjalung.Search_English.startswith(alphanumeric.lower())|dblanguage.Bundjalung.Search_English.startswith('-'+alphanumeric.lower())

	        wordlist=dblanguage(condition).select(orderby=orderbys)
    	else:
		numerics=['A','BA','BE','BI', 'BU','D','J','L','M','N','NG','NY','O','S','WA', 'WE', 'WI', 'WU','YA','YE','Yi','YU']
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
    top_message = language +" Dictionary"
    w = db.plugin_wiki_page
    page = w(slug='usedictionary')    
    if page: pageteaser=page.summary
    else: pageteaser=""
    return dict(start=response.start, page=pageteaser, dialect= dialect, sort=sort, exact=exact, names=names, query=searchterms, words=wordlist, top_message=top_message, numeric= alphanumeric, numerics=numerics)


def wordlist():
  	results= dictionary()
	results['start']=False	
	return results


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

    link = URL(r=request, c='language' ,f='edit_word', args=word_id)
    return dict(link = link, word=word, exampleSentences=examples, language=language )

def view_word_popup():
    word_id=request.args(0)
    words=dblanguage.Bundjalung
    word,examples =read_word(dblanguage.Bundjalung(dblanguage.Bundjalung.id==word_id))
    word=fix_word(word)
    link = URL(r=request, c='language' ,f='edit_word', args=word_id)
    return dict(link = link, word=word)


def translate():
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
	word.Sound=""
	if (not word.SoundFile or word.SoundFile==''): word.Sound=word.Language_Word+".mp3"
        if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+word.Sound)):
	    word.Sound = URL(r=request, c='default',f='filedownload/media/sounds', args=word.Sound)
        else:
	   if (not word.SoundFile or word.SoundFile==''): 
		word.Sound=word.Language_Word+".wav"
           if(os.path.exists('applications/'+language+'/uploads/media/sounds/'+word.Sound)):
		word.Sound = URL(r=request, c='default',f='filedownload/media/sounds', args=word.Sound)
	   else: word.Sound=None
        word.Image=word.Image.strip()
	word.ImageLink=word.Image
	if(word.Image==None or word.Image==""):word.Image=word.Search_English
	end=string.find(word.Image,';');
	if end>0:word.Image=word.Image[0:end]
        word.Image=word.Image.replace(', ','_')

	word.Image=word.Image.replace(' ','_')
        if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.gif')):
                word.ImageLink = URL(r=request, c='default',f='image', args=word.Image+'.gif')
        else: word.ImageLink=""
        if(word.ImageLink==""):
                if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.jpg')):
			word.ImageLink = URL(r=request, c='default',f='image', args=word.Image+'.gif')
                else: word.Image=""
	condition = dblanguage.BundjalungExamples.language_id==word.id
        examplelist=dblanguage(condition).select(dblanguage.BundjalungExamples.ALL)
	word.dialect=""
	colour="black"
	if word.Gold_Coast_Tweed.strip() !="":
		word.dialect+="Gold_Coast_Tweed, "
	if word.Lower_Richmond.strip()!="":
		word.dialect+="Lower_Richmond, "

        if word.Middle_Clarence.strip()!="":
                word.dialect+="Middle_Clarence, "

        if word.Condamine_Upper_Clarence.strip()!="":
                word.dialect+="Condamine_Upper_Clarence, "

        if word.Copmanhurst.strip()!="":
                word.dialect+="Copmanhurst "

#remove ','
	word.dialect = word.dialect.strip()[:-1]
# if only one dialect
 	if word.dialect!="" and word.dialect.find(',')<0:
		colour=db(db.dialect.name==word.dialect).select()
		if colour: word.color=colour[0].color
		else: word.color='black'
	else:
		word.color='black'
        return word, examplelist

