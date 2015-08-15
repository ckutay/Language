# coding: utf-8

def index():

 redirect(URL(r=request, c='plugin_wiki', f='index.html'))

@auth.requires_membership('editor')
def edit_page():
	 redirect(URL(r=request, c='plugin_wiki', f='edit_page', args=request.args))

def images():
    subdirectory = 'uploads/media/images/'# directory
    filename = request.args(0)
    fullpath = os.path.join(subdirectory, filename)
    if request.args(1):
            filenameadd = request.args(1)
            fullpath = os.path.join(fullpath, filenameadd)
    response.stream(os.path.join(request.folder,fullpath))

def video():
    subdirectory = 'uploads/media/video/'# directory
    filename = request.args(0)
    fullpath = os.path.join(subdirectory, filename)
    if request.args(1):
            filenameadd = request.args(1)
            fullpath = os.path.join(fullpath, filenameadd)
    return response.stream(open(os.path.join(request.folder,fullpath),'rb'),chunk_size=4096)

def sounds():
    subdirectory = 'uploads/media/sounds/'# directory
    filename = request.args(0)
    fullpath = os.path.join(subdirectory, filename)
    if request.args(1):
            filenameadd = request.args(1)
            fullpath = os.path.join(fullpath, filenameadd)
    return response.stream(open(os.path.join(request.folder,fullpath),'rb'),chunk_size=4096)


def doc():
    subdirectory = 'uploads/media/docs/'# directory
    filename = request.args(0)
    fullpath = os.path.join(subdirectory, filename)
    if request.args(1):
            filenameadd = request.args(1)
            fullpath = os.path.join(fullpath, filenameadd)
    return response.stream(open(os.path.join(request.folder,fullpath),'rb'),chunk_size=4096)

##generic controller
@auth.requires_membership('editor')
def manage():
    tableName=request.args[0]
    if (tableName !="ALC" and tableName !="CLW"):

	    table=db[tableName]
    else:
	table=dblanguage[tableName]
    form = crud.update(table,request.args(1))
    table.id.represent = lambda id: \
       A('edit:',id,_href=URL(args=(request.args(0),id)))
    search, rows = crud.search(table)
    return dict(form=form,search=search,rows=rows)

@auth.requires_membership('editor')
def _tags():
    form = crud.create(db.tag)
    tags = db(db.tag.id > 0).select(orderby=db.tag.name)
    return dict(form=form, tags=tags)

@auth.requires_membership('editor')
def _edit_tag():
    if not request.args:
        session.flash = T('Invalid tag')
        redirect(URL(r=request,c='default', f='_tags'))
    form = crud.update(db.tag, request.args[0])
    return dict(form=form)

def map():
    rows=db(db.alc.id>0).select()
    return dict(rows=rows, googlemapkey=plugin_gmap.key)

def _pages():
    if request.vars.query:
        query = (db.plugin_wiki_page.tags.like('%%%s%%' % request.vars.query)) & \
                (db.plugin_wiki_page.is_active == True) & (db.plugin_wiki_page.body!="")
        pages = db(query).select(db.plugin_wiki_page.id, db.plugin_wiki_page.slug, db.plugin_wiki_page.title,
                                 orderby=db.plugin_wiki_page.title)
    else:
        query = (db.plugin_wiki_page.is_active == True) & (db.plugin_wiki_page.body!="")
        pages = db(query).select(db.plugin_wiki_page.id, db.plugin_wiki_page.slug, db.plugin_wiki_page.title,
                                 orderby=db.plugin_wiki_page.title)
    return dict(pages=pages)


def _pages_by_tag():
      if not(request.args):
	 redirect(URL(r=request, c='plugin_wiki', f='pages'))

      try:
    	tag_id= str(request.args[0])

      except (KeyError, ValueError, TypeError):
        redirect(URL(r=request, c='plugin_wiki', f='pages'))
      else:
        if (tag_id=="0"):
            redirect(URL(r=request, c='plugin_wiki', f='pages'))
	tag_name=db.plugin_wiki_tag(id=tag_id).name
	
	query = ((db.plugin_wiki_page.tags.like('%%|%s|%%' % tag_id)) |
                (db.plugin_wiki_page.title.like('%s' % tag_name) )) 
        pages = db(query).select(orderby =~db.plugin_wiki_page.created_on)
        if not pages:
	        redirect(URL(r=request, c='plugin_wiki', f='pages'))

        return dict(pages=pages, selected_tag=tag_name)

def _create_page():
 	search_page = 'New_Page'
	redirect(URL(r=request, c='default', f='_create', args=search_page))


def _page():
    redirect(URL(r=request, c='plugin_wiki', f='page', args=request.args)) 
    if not request.args:
        redirect(URL(r=request,c='default' , f='HOME'))
    search_page = request.args[0] #web2py changes ' ' with '_' for us!
    query = (db.plugin_wiki_page.title == search_page) & (db.plugin_wiki_page.is_active == True)
    pages = db(query).select()
    if not pages:
        redirect(URL(r=request, c='default', f='_create', args=search_page))
    
    page = pages[0]
   # response.title+= ' - '+page.title.replace('_', ' ') 
    docs = db(db.document.slug== page.slug).select(orderby=db.document.name)
    db.comment.slug.default = page.slug
    form_comment = crud.create(db.comment,
                               next=URL(r=request, args=request.args))
    form_comment[0][0][0][0] = '' #Delete 'Body:'
    coms = db(db.comment.slug == page.slug).\
           select(orderby=db.comment.created_by)
    return dict(page=page, docs=docs, coms=coms, form_comment=form_comment)


@auth.requires_membership('editor')
def _page_history():
    if not request.args:
        session.flash = T('Invalid page')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    search_page = request.args[0].replace('%20', ' ')
    pages = db(db.plugin_wiki_page.title == search_page).\
            select(orderby=~db.plugin_wiki_page.created_on)
    return dict(pages=pages)


@auth.requires_membership('editor')
def _diff():
    from gluon.contclw.markdown import WIKI
    from applications.wiki.modules.diff import textDiff
    if not request.args:
        session.flash = T('Invalid page')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    search_page = request.args[0].replace('%20', ' ')
    page = db(db.plugin_wiki_page.id == search_page).select()[0]
    cpage = db(db.plugin_wiki_page.slug== page.slug)(db.plugin_wiki_page.is_active == True).select()[0]
    return dict(difference=XML(textDiff(page.body, cpage.body)))


@auth.requires_membership('editor')
def _create():
    db.plugin_wiki_page.title.requires.append(
        IS_NOT_IN_DB(db, 'page.title',
                     error_message=T('This page titele already exists!'))
    )
    form = crud.create(db.plugin_wiki_page, next='_pages')
    if len(request.args): form.custom.widget.title['_value'] = request.args[0]

    return dict(form=form)


@auth.requires_membership('editor')
def _new_document():
    if not request.args:
        session.flash = T('Invalid tag')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    search_page = request.args[0].replace('%20', ' ')
    db.document.slug.default = search_page
    form = crud.create(db.document, next='_pages')
    return dict(form=form)


@auth.requires_membership('editor')
def _edit_document():
    if not request.args:
        session.flash = T('Invalid document')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    form = SQLFORM(db.document, request.args[0], showid=False, deletable=True)
    if form.accepts(request.vars, session):
        message = T('Document updated') if len(request.args) else \
                  T('Document posted')
        session.flash = message
        page = db(db.plugin_wiki_page.slug== form.record.slug).select()
        if page:
            redirect(URL(r=request,c='default',  f='_page', args=page[0].title))
        else:
            redirect(URL(r=request, c='default',  f='index'))
    return dict(form=form)


@auth.requires_membership('editor')
def _edit_page():
    if not request.args:
        session.flash = T('Invalid page')
        redirect(URL(r=request, c='default',  f='_pages'))
    try:
        page_id = int(request.args(0))
    except (ValueError, TypeError):
        session.flash = T('Invalid page id')
        redirect(URL(r=request,c='default', f='_pages'))
    else:
        page = db.plugin_wiki_page[page_id]
        if not page:
            session.flash = T('Invalid page id')
            redirect(URL(r=request, c='plugin_wiki', f='_pages'))
        db.plugin_wiki_page.title.default = page.title
        db.plugin_wiki_page.title.requires = []
        db.plugin_wiki_page.title.readable = True
        db.plugin_wiki_page.title.writable = False
    
    form = SQLFORM(db.plugin_wiki_page, page_id, showid=False)
    if FORM.accepts(form, request.vars, session):
       db(db.plugin_wiki_page.title == form.record.title).update(is_active=False)
       d = db.plugin_wiki_page._filter_fields(form.vars)
       d.update(is_active=True, slug=form.record.slug)
       page_id = db.plugin_wiki_page.insert(**d)
       redirect(URL(r=request, c='default', f='_page', args=slug(db.plugin_wiki_page[page_id])))
    return dict(form=form)


def _revert():
    if not request.args:
        session.flash = T('Invalid page')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    try:
        page_id = int(request.args(0))
    except (ValueError, TypeError):
        session.flash = T('Invalid page id')
        redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    else:
        page = db.plugin_wiki_page[page_id]
        if not page:
            session.flash = T('Invalid page id')
            redirect(URL(r=request, c='plugin_wiki', f='_pages'))
    
    db(db.plugin_wiki_page.title == page.title).update(is_active=False)
    db(db.plugin_wiki_page.id == page.id).update(is_active=True)
    session.flash = T('Page reverted')
    redirect(URL(r=request, c='default', f='_page', args=page.title))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

def user():
	from gluon.tools import Mail
	form=auth()
	if request.args(0)=='register':
               if form.accepts(request.vars, session):
                   try: 
                        mail=Mail()
                        mail.settings.server=EMAIL_SERVER+":25"
                        mail.settings.sender=EMAIL_SENDER
                        mail.send(to=[EMAIL_SENDER],subject="Registration for approval",             message='Registration requires approval. New user email is %(email)s. Click on link to view pending requests: http://www.irca.net.au/appadmin/update/db/auth_user/registration_key/pending'% {'email' : form.vars.email})
                        session.flash=T("Your registration is being held for approval")

                   except:
		    	session.flash=T("Mail being held for approval")

                   	redirect(URL(r=request, c='plugin_wiki', f='index'))
 	    	   db.auth_user[form.vars.id] = dict(registration_key='pending')
	       else:
			form=auth.register()
        elif request.args(0)=='login':
		if request.env.http_referrer:

			auth.settings.login_next =redirect(request.env.http_referrer)
		return dict(form=auth.login())

	else:
		if request.env.http_referrer:
    			auth.settings.login_next =redirect(request.env.http_referrer)
        return dict(form=form)

def _user():
   #without layout and need to direct form to this method
        from gluon.tools import Mail
        form=auth()
	if request.args(0)=='register':
                if form.accepts(request.vars, session):
                   try:
                        mail=Mail()
                        mail.settings.server=EMAIL_SERVER+":25"
                        mail.settings.sender=EMAIL_SENDER
                        mail.send(to=[EMAIL_SENDER],subject="Registration for approval",             message='Registration requires approval. New user email is %(email)s. Click on link to view pending requests: http://www.irca.net.au/appadmin/update/db/auth_user/registration_key/pending'% {'email' : form.vars.email})
                        session.flash=T("Your registration is being held for approval")

                   except:
                        session.flash=T("Mail being held for approval")

                        redirect(URL(r=request, c='plugin_wiki', f='index'))
                   db.auth_user[form.vars.id] = dict(registration_key='pending')

        elif request.args(0)=='login':
                if request.env.http_referrer:

                        auth.settings.login_next =redirect(request.env.http_referrer)
		form=auth.login()
		redirect (URL('user',args='login'))

        else:
                if request.env.http_referrer:
                        auth.settings.login_next =redirect(request.env.http_referrer)
        return dict(form=form)



def langdownload(): return response.download(request, dblanguage)

##def download(): return response.download(request, db)

def download():
    from gluon.contenttype import contenttype
    filename=request.args[0]
    try:
	type=request.args[1]
    except:
	type=None

    response.headers['Content-Type']=contenttype(filename)
    if type:
	return open(os.path.join(request.folder,'uploads/','%s/%s' % (type, filename )),'rb').read()
    else:
        return open(os.path.join(request.folder,'uploads/','%s' % filename),'rb').read()

def _download(): return response.download(request, db)

import os
import logging
logger = logging.getLogger("web2py.app.myapp")
logger.setLevel(logging.DEBUG)


def filedown():
    subdirectory = 'uploads/'# directory
    i=1
    filename = request.args(0)
    while(filename!=None):
	subdirectory = os.path.join(subdirectory, filename)
	filename = request.args(i)
	i+=1
    fullpath=subdirectory
    response.stream(os.path.join(request.folder,fullpath))

import re
def references():
    subdirectory = 'applications/'+language.title()+'/uploads/media/docs/'# directory
    i=1
    fullpath= request.args(0)
    index=request.args(1)
    if (index==None): index=1
    files=[]
    i=1
    fullpathfile=fullpath +str(i)+'.jpg'
    while (os.path.exists(os.path.join(subdirectory,fullpathfile))):
	files.append(fullpathfile)
	i+=1
	fullpathfile=fullpath+str(i)+'.jpg'
    link =URL(r=request, c='default',f='reference', args=files[int(index)-1])
    fullpath = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', fullpath)
    fullpath=re.sub('([a-z0-9])([A-Z])', r'\1 \2', fullpath)
    return dict(link=link, filelist=fullpath, files=files, index=index)
    #response.stream(os.path.join(request.folder, fullpath))


def reference():
    subdirectory = 'uploads/media/docs/'# directory
    i=1
    filename = request.args(0)
    while(filename!=None):
        subdirectory = os.path.join(subdirectory, filename)
        filename = request.args(i)
        i+=1
    fullpath=subdirectory
    response.stream(os.path.join(request.folder, fullpath))
