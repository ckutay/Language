# This file was developed by Massimo Di Pierro
# It is released under BSD, MIT and GPL2 licenses

##########################################################
# code to handle wiki pages
##########################################################

###
#@auth.requires_login()
###
import os

def search():
    words=None
    pages=None
    if request.vars.query:
	searchterm=request.vars.query
	typequery=request.vars.type
        query = (db.plugin_wiki_page.body.like('%%%s%%' % searchterm) |db.plugin_wiki_page.title.like('%%%s%%' % searchterm) )
        pages = db(query).select(db.plugin_wiki_page.title,db.plugin_wiki_page.summary, db.plugin_wiki_page.slug,db.plugin_wiki_page.tags,
                                 orderby=db.plugin_wiki_page.title)
	if typequery=="English":
		query= dblanguage.Bundjalung.English.like('%%%s%%' % searchterm) 
	else:
		query= dblanguage.Bundjalung.Language_Word.like('%%%s%%' % searchterm) 
	words=dblanguage(query).select()
    return dict(words=words, pages=pages, query=request.vars.query)


def pages():
    w = db.plugin_wiki_page
    t=db.plugin_wiki_tag
    taglist=db(t.id>0).select(orderby=t.id)
    words=None
    if plugin_wiki_editor:
    	    pages = db(w.id>0)(w.is_active==True).select(orderby=w.title)
    else:
        	pages = db(w.is_active==True)(w.is_public==True).select(orderby=w.title)
     
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
    return dict(taglist=taglist, pages=pages, form=form,query=request.vars.query)

def index():
    page= db.plugin_wiki_page(slug="Introduction")
    if page: pageteaser=page.summary
    else: pageteaser=""
    return dict(page=pageteaser,title=page.title,images=images)

def about():
    images=db(db.image.show==0).select()
    w = db.plugin_wiki_page
    page = w(slug="about_us")
    if page: pageteaser=page.summary
    else: pageteaser=""
    return dict(page=pageteaser,title='Language Locations',images=images)

def teaching():
        #redirect(URL('index'))
    images=db(db.image.show==1).select()
    return dict(title='Language Teaching',images=images)

def map():
    w = db.plugin_wiki_page
    page = w(title="Index")
    if plugin_wiki_editor:
        form=SQLFORM.factory(Field('title',requires=db.plugin_wiki_page.title.requires),  Field('from_template',requires=IS_EMPTY_OR(IS_IN_DB(db,db.plugin_wiki_page.title))))
        if form.accepts(request.vars):
            redirect(URL(r=request,f='page',args=form.vars.title.replace(' ','_'),vars=dict(template=request.vars.from_template or '')))
    else:
        form=''
    width = request.vars.width or 600
    height = request.vars.height or 600


    rows = plugin_gmap.set.select()
    alcs= plugin_gmaps.set.select()
    for row in rows:
        row.plugin_gmap_clw= plugin_gmap.clw(row)
        try:
                if not row.Web_URL:
                        row.Web_URL=dblanguage.ALC(id=plugin_gmap.id(row)).Web_URL
                row.plugin_gmap_color = dblanguage.ALC(id=plugin_gmap.id(row)).Colour.lower()
                row.plugin_gmap_address= plugin_gmap.address(row)
                row.plugin_gmap_image= plugin_gmap.image(row)
                row.plugin_gmap_ALC=plugin_gmap.ALC(row)
                row.plugin_gmap_alt=plugin_gmap.alt(row)
                row.plugin_gmap_popup=plugin_gmap.represent(row)
		row.login=auth.is_logged_in()
        except:
                pass
    for alc in alcs:
        alc.plugin_gmaps_alc=plugin_gmaps.alcs(alc)
        alc.plugin_gmaps_color = plugin_gmaps.color(alc)
        alc.plugin_gmaps_image= plugin_gmaps.image(alc)
        alc.plugin_gmaps_address=plugin_gmaps.address(alc)
	alc.login=auth.is_logged_in()
    #return LOAD('plugin_gmap','map', ajax=True)

    return dict(width=width,height=height, alcs=alcs,  rows=rows,page=page, form=form)

def contact():

    form=SQLFORM.factory(
        Field('your_email',requires=IS_EMAIL()),
        Field('question','text', requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        if mail.send(to ="ckutay@cities.org.au",
        subject="From %s website" % language,
	reply_to="%s" % form.vars.your_email,
	message=form.vars.question):
          pass#   redirect(URL('contact'))
    elif form.errors:
        form.errors.your_email='Unable to send email'
    top_message = "This form will send an email to Muurrbay. We will try to answer your request quickly"   
    return dict(form=form, top_message=top_message)


@auth.requires_login()
def edit_resource():
	form=None
        resource_title=request.args(0)
        if(resource_title==None):redirect(URL(r=request, c='plugin_wiki', f='resources'))
        transcript=db(db.plugin_wiki_transcript.title==resource_title).select().first()
        w = db.Resources
        resource = w(title=resource_title)
        if not  resource:
           	redirect(URL(r=request, c='plugin_wiki', f='resources'))
	else:
                #tags = page.tags #in practice 'xyz' would be a variable
                form = crud.update(w, resource, deletable=True, onaccept=crud.archive,
                next=URL(r=request,c='plugin_wiki', f='resource',args=resource_title))

	resource_name=os.path.join('file',resource.name)
	return dict(resources=None,resource=resource,resource_name=resource_name, transcript=transcript,form=form)


@auth.requires_login()
def edit_resource_transcript():
        resource_title=request.args(0)
	form=None
        if(resource_title==None):redirect(URL(r=request, c='plugin_wiki', f='resources'))
        resource=db(db.Resources.title==resource_title).select().first()
        if(resource==None):redirect(URL(r=request, c='plugin_wiki', f='resources'))
        transcript=db(db.plugin_wiki_transcript.title==resource_title).select().first()
	if plugin_wiki_editor:
           slug=resource_title.replace(' ','_').lower() 
    	   w = db.plugin_wiki_transcript
    	   transcript= w(title=resource_title)
    	   if not transcript:
        	transcript= w.insert(slug=slug,
                        title=resource_title,
                        body=request.vars.template and w(slug=request.vars.template).body or '')
           form = crud.update(w, transcript, deletable=True, onaccept=crud.archive,
                next=URL(r=request,c='plugin_wiki', f='resource',args=resource_title))


	return dict(form=form, resources=None,resource=resource,transcript=transcript)

def resources():
	Resources=db.Resources
	resources = db(Resources.id>0).select(orderby=Resources.title)            
        if(resources==None):redirect(URL(r=request, c='plugin_wiki', f='pages'))
        return dict(resource=None,resources=resources)

def resource():
	resource_title=request.args(0)
	if(resource_title==None):redirect(URL(r=request, c='plugin_wiki', f='resources'))
	resource=db(db.Resources.title==resource_title).select().first()
	if(resource==None):redirect(URL(r=request, c='plugin_wiki', f='resources'))   
	page=db(db.plugin_wiki_transcript.title==resource_title)
	if (page): page=page.select().first()     
	resource_name=os.path.join("file",resource.name)
	return dict(resources=None,resource=resource, resource_name=resource_name, page=page)



def tags_by_tag():
	import re
	if not(request.args):
    	     redirect(URL(r=request, c='plugin_wiki', f='pages'))
	pages=None
	page=None
	page_body=None
	title="No results"
	try:
			tag_id= str(request.args[0])
	except (KeyError, ValueError, TypeError):
        		redirect(URL(r=request, c='plugin_wiki', f='pages'))
      	
	tag=db.plugin_wiki_tag(id=tag_id)
	if (tag!=None):
			tag.is_active=True;
		 	tags=db(db.plugin_wiki_tag.parent==tag.name).select()
	try:
		page_id= str(request.args[1])
	except(KeyError, IndexError,ValueError, TypeError):
		page_id=str(request.args[0])
	if (page_id.isdigit()):
		tag_name=db.plugin_wiki_tag(id=tag_id).name

        try:
                tag=db.plugin_wiki_tag(id=tag_id)
        except (KeyError, ValueError, TypeError):
                tag=db.plugin_wiki_tag(name=tag_id)
                tag_id=tag.id
        if (tag!=None):
                tag.is_active=True;
                tags=db(db.plugin_wiki_tag.parent==tag.name).select()
        tag_name=tag.name
        try:
                page_id= str(request.args[1])
        except(KeyError, IndexError,ValueError, TypeError):
                page_id=str(request.args[0])
        #if(page_id.isdigit()):
        tag_obj=db.plugin_wiki_tag(id=tag_id)
	if tag_obj: tag_name=tag_obj.name
	else: tag_name=None
        tag_parent=tag_obj.parent
        tag=db.plugin_wiki_tag(name=tag_parent)
        if (tag): tag.is_active=True
        

	query = ((db.plugin_wiki_page.tags.like('%%|%s|%%' % tag_id)))
#        pages = db(query).select(orderby=~db.plugin_wiki_page.created_on)
        if (tags):
                        page = db(query).select(orderby=~db.plugin_wiki_page.created_on).first()
                        if (page and page.worksheet):
                                page.body=wsread_page(page)
                                title="Latest article:"
        else:
                        pages = db(query).select(orderby=~db.plugin_wiki_page.created_on)
                        if(len(pages)>0):
                                title="Pages available are:"
                                page=pages[0]
                                try:
                                        page=pages[1]
                                except:
                                        title="Page:"
                                        page=pages[0]
                                        page.body=wsread_page(pages[0])
                                        pages=None

        #else:
    #           w = db.plugin_wiki_page
   #            page = w(slug=page_id)
#               if page:
#                       page=page.select()
#                       if (page.worksheet):page.body=wsread_page(page)
        if(page!=None):
                page_body=page.body
                #if tag_name!=None:
                #       page_body=''
        form=""
        #read wordlist
        query = (dblanguage.Bundjalung.Category==tag_name)

        words=  dblanguage(query).select(orderby=dblanguage.Bundjalung.English)
        for word in words:
                word=read_word(word)
        if (words and page==None):
                title="Words in Category"
        return dict(tag=tag, words=words,form=form,pages=pages,title=title,page=page,page_body=page_body)



def pages_by_tag():
      if not(request.args):
         redirect(URL(r=request, c='plugin_wiki', f='pages'))

      try:
        tag_name= str(request.args[0])

      except (KeyError, ValueError, TypeError):
        redirect(URL(r=request, c='plugin_wiki', f='pages'))
      else:
        if (tag_name==None):
            redirect(URL(r=request, c='plugin_wiki', f='pages'))
        if(tag_name=="Contact"):
	#contact form
		redirect(URL(r=request, c='plugin_wiki', f='contact'))
        if (tag_name=="WordList"):
	#word list
		redirect(URL(r=request, c='plugin_wiki', f='dictionary'))	
	tag_obj=db.plugin_wiki_tag(name=tag_name)

	if tag_obj: 
		tag_id = tag_obj.id
		
	else: 
		try:
			tag_obj=db.plugin_wiki_tag(id=tag_name)
        		if tag_obj: 
				tag_id = tag_obj.id
				tag_name=tag_obj.name
        		else: tag_id=None
		except: tag_id=None 
	#find parent tag to keep menu open
	tag_parent=tag_obj.parent
	tag=db.plugin_wiki_tag(name=tag_parent)
	if (tag): tag.is_active=True
        query = ((db.plugin_wiki_page.tags.like('%%|%s|%%' % tag_id))) 
#        pages = db(query).select(orderby=~db.plugin_wiki_page.created_on)
	pages = db(query).select()
	if pages:
    		sorted_pages = []



    		for row in pages.sort(lambda row: row.created_on,reverse=True):
        		sorted_pages.append(row)
		pages=sorted_pages
		if (pages[0].worksheet):
			pages[0].body=wsread_page(pages[0])
        else:
                redirect(URL(r=request, c='plugin_wiki', f='pages'))

        return dict(tag=tag, pages=pages, selected_tag=tag_name)

def user():
	redirect(URL(r=request, c='default', f='user'))

def cache_in_ram():
    import time
    t=cache.ram('time',lambda:time.ctime(),time_expire=5)
    return dict(time=t,link=A('click to reload',_href=URL(r=request)))

#@cache(request.env.path_info,time_expire=5,cache_model=cache.disk)


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
	redirect (URL(r=request,c='learning',f='page'))
	page.questions=[]
    page.attachments=[]
    a=db.plugin_wiki_attachment
    query = (a.tablename=="page")&(a.record_id==page.id)
    page.attachments=db(query).select()
    tag=page.tags
    tags=tag.split('|')
    page_body=page.body
    if request.extension=='load':
        return plugin_wiki.render(page_body)
    if request.extension=='html':         
        return dict(form="", title=page.title, page=page, page_body=page_body, slug=slug)

def page_archive():
    """
    shows and old version of a page
    """
    id = request.args(0)
    h = db.plugin_wiki_page_archive
    page = h(id)
    if not page or (not plugin_wiki_editor and (not page.is_public or not page.is_active)):
        raise HTTP(404)
    elif page and page.role and not auth.has_membership(page.role):
        raise HTTP(404)
    if request.extension!='html': return page.body
    return dict(page=page)

def create_page():
    if plugin_wiki_editor:
                form=SQLFORM.factory(Field('title',requires=db.plugin_wiki_page.title.requires),
                             Field('from_template',requires=IS_EMPTY_OR(IS_IN_DB(db,db.plugin_wiki_page.modified_on))))
                if form.accepts(request.vars):
                        redirect(URL(r=request,c='plugin_wiki',f='page_edit',args=form.vars.title.replace(' ','_'),vars=dict(template=request.vars.from_template or '')))
    else:
                form=''

    return dict(form=form, pages=pages)

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
		images=dblanguage(dblanguage.images.id>0).select()
		
		form = crud.update(w, page, deletable=True, onaccept=crud.archive,
                next=URL(r=request,c='plugin_wiki', f='page',args=slug))

    return dict(images=images, form=form,page=page,tags=tags)


def page_history():
    """
    show page changelog
    """
    slug = request.args(0) or 'index'
    w = db.plugin_wiki_page
    h = db.plugin_wiki_page_archive
    page = w(slug=slug)
    history = db(h.current_record==page.id).select(orderby=~h.modified_on)
    return dict(page=page, history=history)


def tags():
    form = crud.create(db.plugin_wiki_tag)
    tags = db(db.plugin_wiki_tag.id > 0).select(orderby=db.plugin_wiki_tag.id)
    return dict(form=form, tags=tags)


def edit_tag():
    if not request.args:
        session.flash = T('Invalid tag')
        redirect(URL(r=request, f='_tags'))
    form = crud.update(db.plugin_wiki_tag, request.args[0], deletable=True)
    return dict(form=form)

##########################################################
# ajax callbacks
##########################################################
def attachments():
    """
    allows to edit page attachments
    """
    a=db.plugin_wiki_attachment
    a.tablename.default=tablename=request.args(0)
    a.record_id.default=record_id=request.args(1)
    #if request.args(2): a.filename.writable=False
    form=crud.update(a,request.args(2),deletable=True,
                     next=URL(r=request,args=request.args[:2]))
    if request.vars.list_all:
        query = a.id>0
    else:
        query = (a.tablename==tablename)&(a.record_id==record_id)
    rows=db(query).select(orderby=a.name)
    return dict(form=form,rows=rows)

def attachment():
    """
    displays an attachments
    """
    short=request.args(0)
    if plugin_wiki_authorize_attachments and \
            not short in session.plugin_wiki_attachments:
        raise HTTP(400)
    a=db.plugin_wiki_attachment
    record=a(short.split('.')[0])
    if not record: raise HTTP(400)
    request.args[0]=record.filename
    return response.download(request,db)


def images_by_name():
    short=request.args(0)
    a=db.plugin_wiki_images
    record=a(short[0])
    if not record:return  record
    request.args[0]=record.filename
    return response.download(request,db)

def images():
    title="Images"
    images = dblanguage().select(dblanguage.images.ALL, orderby=dblanguage.images.title)

    return dict(images=images)

def show_image():
    image = dblanguage.images(request.args(0,cast=int)) or redirect(URL('index'))
    dblanguage.post.image_id.default = image.id
    form = SQLFORM(dblanguage.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = dblanguage(dblanguage.post.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

@auth.requires_login()
def manage_images():
    grid = SQLFORM.smartgrid(dblanguage.images,linked_tables=['post'])
    return dict(grid=grid)

def download():
    return response.download(request, db)

def comment():
    """
    post a comment
    """
    tablename, record_id = request.args(0), request.args(1)
    table=db.plugin_wiki_comment
    if record_id=='None': record_id=0
    table.tablename.default=tablename
    table.record_id.default=record_id
    if auth.user:
        form = crud.create(table)
    else:
        form = A(T('login to comment'),_href=auth.settings.login_url)
    comments=db(table.tablename==tablename)\
        (table.record_id==record_id).select()
    return dict(form = form,comments=comments)
###
##@auth.requires_login()
##
def jqgrid():
    """
    jqgrid callback retrieves records
    http://trirand.com/blog/jqgrid/server.php?q=1&_search=false&nd=1267835445772&rows=10&page=1&sidx=amount&sord=asc&searchField=&searchString=&searchOper=
    """
    from gluon.serializers import json
    import cgi
    hash_vars = 'dbname|tablename|columns|fieldname|fieldvalue|user'.split('|')
    if not URL.verify(request,hmac_key=auth.settings.hmac_key,
                      hash_vars=hash_vars,salt=auth.user_id):
        raise HTTP(404)    
    tablename = request.vars.tablename or error()
    columns = (request.vars.columns or error()).split(',')
    rows=int(request.vars.rows or 25)
    page=int(request.vars.page or 0)
    sidx=request.vars.sidx or 'id'
    sord=request.vars.sord or 'asc'
    searchField=request.vars.searchField
    searchString=request.vars.searchString
    searchOper={'eq':lambda a,b: a==b,
                'nq':lambda a,b: a!=b,
                'gt':lambda a,b: a>b,
                'ge':lambda a,b: a>=b,
                'lt':lambda a,b: a<b,
                'le':lambda a,b: a<=b,
                'bw':lambda a,b: a.like(b+'%'),
                'bn':lambda a,b: ~a.like(b+'%'),
                'ew':lambda a,b: a.like('%'+b),
                'en':lambda a,b: ~a.like('%'+b),
                'cn':lambda a,b: a.like('%'+b+'%'),
                'nc':lambda a,b: ~a.like('%'+b+'%'),
                'in':lambda a,b: a.belongs(b.split()),
                'ni':lambda a,b: ~a.belongs(b.split())}\
                [request.vars.searchOper or 'eq']
    table=globals()[dbname][tablename]
    if request.vars.fieldname:
        names = request.vars.fieldname.split('|')
        values = request.vars.fieldvalue.split('|')
        query = reduce(lambda a,b:a&b,
                       [table[names[i]]==values[i] for i in range(len(names))])
    else:
        query = table.id>0
    dbset = table._db(query)
    if searchField: dbset=dbset(searchOper(table[searchField],searchString))
    orderby = table[sidx]
    if sord=='desc': orderby=~orderby
    limitby=(rows*(page-1),rows*page)
    fields = [table[f] for f in columns]
    records = dbset.select(orderby=orderby,limitby=limitby,*fields)
    nrecords = dbset.count()
    items = {}
    items['page']=page
    items['total']=int((nrecords+(rows-1))/rows)
    items['records']=nrecords
    readable_fields=[f.name for f in fields if f.readable]
    def f(value,fieldname):
        r = table[fieldname].represent
        if r: value=r(value)
        try: return value.xml()
        except: return cgi.escape(str(value))
    items['rows']=[{'id':r.id,'cell':[f(r[x],x) for x in readable_fields]} \
                       for r in records]
    return json(items)


def _tags():
    import re
    db_tag = db.plugin_wiki_tag
    db_link = db.plugin_wiki_link
    table_name=request.args(0)
    record_id=request.args(1)
    if not auth.user_id:
        return ''
    form = SQLFORM.factory(Field('tag_name',requires=IS_SLUG()))
    if request.vars.tag_name:
        for item in request.vars.tag_name.split(','):
            tag_name = re.compile('\s+').sub(' ',item).strip()
            tag_exists = tag = db(db_tag.name==tag_name).select().first()
            if not tag_exists:
                tag = db_tag.insert(name=tag_name, links=1)
            link = db(db_link.tag==tag.id)\
                (db_link.table_name==table_name)\
                (db_link.record_id==record_id).select().first()
            if not link:
                db_link.insert(tag=tag.id,
                               table_name=table_name,record_id=record_id)
                if tag_exists:
                    tag.update_record(links=tag.links+1)
    for key in request.vars:
        if key[:6]=='delete':
            link_id=key[6:]
            link=db_link[link_id]
            del db_link[link_id]
            db_tag[link.tag] = dict(links=db_tag[link.tag].links-1)
    links = db(db_link.table_name==table_name)\
              (db_link.record_id==record_id).select()\
              .sort(lambda row: row.tag.name.upper())
    return dict(links=links, form=form)

def cloud():
    tags = db(db.plugin_wiki_tag.links>0).select(limitby=(0,20))
    if tags:
        mc = max([tag.links for tag in tags])
    return DIV(_class='plugin_wiki_tag_cloud',*[SPAN(A(tag.name,_href=URL(r=request,c='plugin_wiki',f='page',args=('tag',tag.id))),_style='font-size:%sem' % (0.8+1.0*tag.links/mc)) for tag in tags])

@auth.requires(plugin_wiki_editor)
def widget_builder():
    """
    >> inspect.getargspec(PluginWikiWidgets.tags)
    (['table', 'record_id'], None, None, ('None', None))
    >>> dir(PluginWikiWidgets)
    """
    import inspect
    name=request.vars.name
    if plugin_wiki_widgets=='all':
        widgets = ['']+[item for item in dir(PluginWikiWidgets) if item[0]!='_']
    else:
        widgets = plugin_wiki_widgets
    form=FORM(LABEL('Widget Name: '), SELECT(_name='name',value=name,
                     _onchange="jQuery(this).parent().submit()",*widgets))
    widget_code=''
    if name in widgets: 
        a,b,c,d=inspect.getargspec(getattr(PluginWikiWidgets,name))
        a,d=a or [],d or []
        null = lambda:None
        d=[null]*(len(a)-len(d))+[x for x in d]
        ESC='x'
        fields = [Field(ESC+a[i],label=a[i],default=d[i]!=null and d[i] or '',
                        requires=(d[i]==null) and IS_NOT_EMPTY() or None,
                        comment=(d[i]==null) and 'required' or '') \
                      for i in range(len(a))]
        form_widget=SQLFORM.factory(hidden=dict(name=name),*fields)
        doc = getattr(PluginWikiWidgets,name).func_doc or ''
        if form_widget.accepts(request.vars):
            keys=['name: %s' % request.vars.name]
            for name in a:
                if request.vars[ESC+name]:
                    keys.append(name+': %s' % request.vars[ESC+name])
            widget_code=CODE('``\n%s\n``:widget' % '\n'.join(keys))
    else:
        doc=''
        form_widget=''
    return dict(form=form,form_widget=form_widget,doc=doc,
                widget_code=widget_code)


def star_rate():
    N=5 #max no of stars (if you use split stars you'll get a rating out of 10)
    pm = db.plugin_wiki_rating
    pa = db.plugin_wiki_rating_aux
    tablename = request.args(0)
    record_id = request.args(1)
    rating = abs(float(request.vars.rating or 0)) 
    
    try:
        db[tablename] #if there's no such table. Salute.
        if rating>N or rating<0: raise Exception #similar if rating is simulated.
        if not db[tablename][record_id]: raise Exception #also if there's no specified record in table
        if not auth.user_id: raise Exception #user has to login to rate
    except:
        return ''
        
    master = db(pm.tablename==tablename)(pm.record_id==record_id).select().first()    
    
    if master:
        master_rating, master_counter = master.rating, master.counter
    else:
        master_rating, master_counter = 0, 0
        master=pm.insert(tablename=tablename,record_id=record_id,rating=master_rating,counter=master_counter)        
        
    record = db(pa.master==master)(pa.created_by==auth.user_id).select().first()
        
    if rating:
        if not record:
           record = pa.insert(master=master,rating=rating,created_by=auth.user_id)
           master_rating = (master_rating*master_counter + rating)/(master_counter+1)
           master_counter = master_counter + 1
        else:
           master_counter = master_counter
           master_rating = (master_rating*master_counter - record.rating + rating)/master_counter
           record.update_record(rating=rating)
        master.update_record(rating=master_rating, counter=master_counter)        
    try:  
        db[tablename][record_id]['rating']
    except:
        return ''
    else:
        db[tablename][record_id].update_record(rating=master_rating)
        
    return ''
   
