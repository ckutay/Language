#################
#Interface to nltk for languages
#
#################
# -*- coding: utf-8 -*-
# try something like

import altk
from altk.dictionary import *
from altk.tagger import *
from altk.stemmer import *
import urllib
import nltk, re, pprint # NLTK and related modules -- are these all needed?
from nltk.corpus import abc

import os, sys
from  nltk.tokenize.punkt import PunktWordTokenizer


def translate_word(word, lang, ws, wd):
                reduced_word = ws.stem(word, hide_suffixes = False, show_translation = True, show_pos=True)

                stem = reduced_word[0]
                translated_stem = translate_stem(stem, lang, wd)

                translated_suffixes = reduced_word[1]
                # if translated_stem[0]=="": return (translated_stem, translated_suffixes)

                reduced_word_part = ws.stem(translated_stem[0], hide_suffixes = False, show_translation = True)

                translated_stem = translated_stem + translate_stem(reduced_word_part[0],lang, wd)
                translated_suffixes = translated_suffixes + reduced_word_part[1]

                return (translated_stem, translated_suffixes)

def translate_stem(stem, lang, wd):

                if lang!="English":
			if wd.has_word(stem):

	                        return (stem, wd.getEnglish(stem), wd.getPartEng(stem))
		else:	
			
			if wd.has_eng_word(stem):		
				return (stem, wd.getLanguage(stem), wd.getPartLang(stem))
		return (stem, stem, 'Unknown')

def print_words(words):
                AboriginalLanguage = ""
                english = ""
                pos=""
                for word in words:

                        printed_word = print_word(word)

                        AboriginalLanguage += printed_word[0] +" "
                        english +=  printed_word[1] +" "
                        pos+= printed_word[2]+" "

                return [AboriginalLanguage, english, pos]

def print_word(word):
    stem = word[0]
    suffixes = word[1]

    printed_stem = print_stem(stem)
    AboriginalLanguage = printed_stem[0]
    english = printed_stem[1]
    pos=printed_stem[2]
    for suffix in suffixes:
        printed_suffix = print_suffix(suffix)
        AboriginalLanguage +=  printed_suffix[0]
        english += printed_suffix[1]
        pos+=printed_suffix[2]
    return [AboriginalLanguage, english,pos]

def print_stem(stem):

                AboriginalLanguage = stem[0]
                english = stem[1]
                 #create array
                pos=stem[2]
                w_length = len(AboriginalLanguage)
                e_length = len(english)

                length = max(w_length, e_length)
                AboriginalLanguage = AboriginalLanguage.center(length)
                english = english.center(length)
                if pos: pos = pos.center(length)
                return [AboriginalLanguage, english, pos]

def print_suffix(suffix):
                AboriginalLanguage = "-" + suffix[0]
                english = " " + suffix[1]
                pos = " "+suffix[2]
                w_length = len(AboriginalLanguage)
                e_length = len(english)

                length = max(w_length, e_length)
                AboriginalLanguage = AboriginalLanguage.center(length)
                english = english.center(length)
                pos= pos.center(length)
                return [AboriginalLanguage, english, pos]


def parser():
    words=None
    searchterm=request.vars.query
    lang=request.vars.lang
	#null searches
    if not(request.vars):
    	return dict(wordlist=True, words=words)
    elif not(searchterm):
    	redirect (URL(r=request,c="language",f="dictionary"))

### add reference to example sentences
    #wordlist=searchterm.split()
    #for word in wordlist:
#	pass
    if lang=="English":
                query= dblanguage.BundjalungExamples.English.like('%% %s %%' % searchterm)
    else:
                query= dblanguage.BundjalungExamples.Language.like('%% %s %%' % searchterm)
    words=dblanguage(query)
    try:
	words=words.select()
    except:
	redirect (URL(r=request,c="language",f="dictionary",vars={'query':searchterm, 'lang':lang}))
##else load dictionary
    wd = dictionary.AboriginalLanguageDictionary()
    ws = stemmer.AboriginalLanguageStemmer()

    if (words):
	return dict(wordlist=False, words=words, query=searchterm)
    else:
		newwords = PunktWordTokenizer().tokenize(searchterm)
		words = []
	
                for word in newwords:
                	words+= [translate_word(word, lang, ws, wd)]   
    		lang=[]
    		english=[]
    		pos=[]
    		for word in words:
                        printed_word = print_word(word)
                        lang.append(printed_word[0])
                        english.append(printed_word[1])
                        pos.append(printed_word[2])
		leng=len(lang)

    		words=[lang,english,pos]
    return dict(wordlist=True, words=words, query=request.vars.query)


def pages():
    w = db.plugin_wiki_page
    t=db.plugin_wiki_tag
    taglist=db(t.id>0).select(orderby=t.id)
    words=None
    if plugin_wiki_editor:
            pages = db(w.worksheet==True).select(orderby=w.title)
    else:
                pages = db(w.worksheet==True)(w.is_public==True).select(orderby=w.title)

    if plugin_wiki_editor:
                form=SQLFORM.factory(Field('title',requires=db.plugin_wiki_page.title.requires),
                             Field('from_template',requires=IS_EMPTY_OR(IS_IN_DB(db,db.plugin_wiki_page.title))))
                if form.accepts(request.vars):
                        title=request.vars.title
                        page =db(w.title==title).select().first()
                        if not page:
                                page = w.insert(slug=title.replace(' ','_'),
                                title=title,
                                body=request.vars.template and w(slug=request.vars.template).body or '')
                        redirect(URL(r=request,f='edit_page',args=form.vars.title,vars=dict(template=request.vars.from_template or '')))
    else:
                form=''
    return dict(query=request.vars.query, taglist=taglist, pages=pages, form=form)

def page():
    """
    shows a page
    """
    slug= request.args(0)
    import re
    if slug=="Index" or slug==None:
        redirect(URL(r=request, c='plugin_wiki', f='index.html'))
    if slug=="Admin_Help" and not auth.user:
        redirect(URL(r=request, c='plugin_wiki', f='pages'))


    w = db.plugin_wiki_page
    page = w(slug=slug)
    #for template
    if (not page or not page.is_public or not page.is_active):
         if plugin_wiki_editor:
                redirect(URL(r=request, c='plugin_wiki', f='edit_page', args=request.args))
         if (session):session.flash=T("Page not available")

         redirect(URL(r=request, c='plugin_wiki', f='pages'))
    elif page and page.role and not auth.has_membership(page.role):
        raise HTTP(404)
        # parse pages. First History
    if page.worksheet:
        page.questions=[]
    page.attachments=[]
    a=db.plugin_wiki_attachment
    query = (a.tablename=="page")&(a.record_id==page.id)
    page.attachments=db(query).select()
    page_body=page.body
    if (page.worksheet):
	page_body = wsread_page(page)
    page=wsread_question(page_body, page)
    title=page.title
    page_body=page.body

    return dict(form="", title=page.title, page=page, page_body=page_body, slug=slug )

def list():
    page_id=request.args(0)
    print page_id
    wl=wordlist(page_id)
    print wl
    if wl: words=wl['words'];
    else: wl=None
    return dict(words=words, page_id=page_id)



@auth.requires_login()
def edit_page():
    """
    edit a page
    """
    slug = request.args(0) or 'Index'
    tags=""
    if request.args(1): tags='|'+request.args(1)+'|'
    slug=slug.replace(' ','_')
    w = db.plugin_wiki_page
    w.role.writable = w.role.readable = plugin_wiki_level>1
    page = w(slug=slug)
    """
    db.plugin_wiki_page.tag.default=""
    db.plugin_wiki_page.update.tags=db.plugin_wiki_page.tags
    """
    if not page:
        db.plugin_wiki_page.tags.default=tags

        page = w.insert(slug=slug,
                        title=slug.replace('_',' '),
                        tags=tags,
                        body=request.vars.template and w(slug=request.vars.template).body or '')
    else:
        tags = page.tags #in practice 'xyz' would be a variable
    if page.title=="Index":
        form = crud.update(w, page, deletable=True, onaccept=crud.archive,
                       next=URL(r=request, c='plugin_wiki', f='index'))
    else:
                form = crud.update(w, page, deletable=True, onaccept=crud.archive,
                next=URL(r=request,c='learning', f='page',args=slug))

    return dict(form=form,page=page,tags=tags)

