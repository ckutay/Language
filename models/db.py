#auto update on change
from gluon.custom_import import track_changes; track_changes(True)
from gluon import *

EMAIL_SERVER='cities.org.au:25'
EMAIL_SENDER='ckutay@cities.org.au'
EMAIL_AUTH="ckutay@cities.org.au:AK131391"

RECAPTCHA_PUBLIC_KEY='6LefJwQAAAAAAEuj02bmS2LgiZiPhGBqKP1kbn26'
RECAPTCHA_PRIVATE_KEY='6LefJwQAAAAAAPcK2G6SO_pyJDegHi58J41bEVrV'

from gluon.validators import Validator

#distiguish in dictionary or not

languageList=None

class SlugValidator(Validator):
    def __call__(self, value):
        return (value.replace(' ', '_'), None)
#set for each language
language='Bundjalung'

import uuid
try:
    from gluon.contclw.gql import *  # if running on Google App Engine
except:
    #db = SQLDB('sqlite://storage.db')  # if not, use SQLite or other DB
    dblanguage= DAL('mysql://language_admin:budyari@localhost/language', pool_size=0,migrate=False, fake_migrate=True)

    db= DAL('mysql://language_admin:budyari@localhost/'+language, pool_size=0,migrate=False, fake_migrate=True)

session.connect(request, response, db=db)  # and store sessions there

import sys, nltk, re, pprint # NLTK and related modules -- are these all needed?
from  nltk.tokenize.punkt import PunktSentenceTokenizer


from gluon.tools import *

#need python-gdate in fdora 16
#from gdata.calendar import service, data
import logging
logger = logging.getLogger("web2py.app.Bundjalung")
logger.setLevel(logging.DEBUG)

auth = Auth(db)

mail =  Mail()
mail.settings.server = EMAIL_SERVER
mail.settings.sender =  EMAIL_SENDER
mail.settings.login = EMAIL_AUTH
mail.settings.tls = False
#mail.settings.login = 'username:password'
auth.settings.mailer=mail

service = Service()
plugins = PluginManager()

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#laouter reduced after start
response.start=True

auth.settings.captcha = None
#Recaptcha(request, RECAPTCHA_PUBLIC_KEY,          RECAPTCHA_PRIVATE_KEY)
auth.settings.login_url = URL(r=request, c='default', f='_user', args='login')
auth.settings.logged_url = URL(r=request, c='default', f='user', args='profile')
auth.settings.login_next=URL(r=request, c='plugin_wiki', f='index')
auth.settings.logout_next=URL(r=request, c='plugin_wiki', f='index')
auth.settings.verify_email_next = URL(r=request, c='default', f='user', args='login')
auth.settings.create_user_groups = False
auth.settings.register_onaccept=lambda form: mail.send(to=EMAIL_SENDER,subject='New Registration',
             message='Registration requires approval. New user id number is %s'%form.vars.id)

crud = Crud(globals(), db) #for CRUD helpers using auth
#crud.settings.auth = auth # (optional) enforces authorization on crud

auth.messages.verify_email = 'Click on the link:\n https://www.web2py.com' + \
    URL(r=request, c='default', f='user/verify_email') +  '/%(key)s\n' + \
    'to verify your email'

who = default = auth.user.id if auth.is_logged_in() else 0
now = request.now


def represent_email(id_):
    email = db.auth_user[id_]
    if not author:
        return 'Author not found'
    else:
        return '%s' % (author.email)

TOP_MESSAGE="Contact form"
VALUE=""


db.define_table('message',
   Field('your_name',requires=IS_NOT_EMPTY()),
   Field('your_email',requires=IS_EMAIL()),
   Field('your_subject','string',length=100),
   Field('your_message','text',default=VALUE),
   Field('to_group',default=False,readable=False,writable=False),
   Field('timestamp',default=now),migrate=False)

db.define_table('recipient',
   SQLField('name',requires=IS_NOT_EMPTY()),
   SQLField('email',requires=IS_EMAIL()),migrate=False)

db.define_table(auth.settings.table_user_name,
    Field('id', 'integer', default=who),
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('username', length=50),
    Field('email', length=128, default='', unique=True),
    Field('password', 'password', length=512,
          readable=False, label='Password'),
    Field('registration_key', length=512,
          readable=False, writable=False, default='pending'),
    Field('registration_id', 'integer',readable=False, writable=False),
    Field('reset_password_key', length=512,
          writable=False, readable=False, default=''),
    Field('Role_Name','string',default=''), 
	migrate=False)

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = \
  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.Role_Name.requires = IS_IN_SET(['student', 'teacher', 'editor'])

custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

#custom_auth_table.ALC_Name.requires=(IS_IN_DB(dblanguage,'ALCS.ALC_Name','%(ALC_Name)s') or '')
#custom_auth_table.CLW_Name.requires=(IS_IN_DB(dblanguage,'CLW.CLW','%(CLW)s') or '')
#custom_auth_table.CLW_Name.requires=IS_IN_SET([dblanguage]  ,error_message=T('Please select CLW or ALC '))


def represent_author(id_):
    author = db.auth_user[id_]
    if not author:
        return 'Author not found'
    else:
        return '%s %s' % (author.first_name, author.last_name)


auth.define_tables(username=True, migrate=False) #creates all needed tables
#authorize map tables
dblanguage.auth_user=db.auth_user

db.define_table('page_index',
   Field('uuid', length=128, readable=False, writable=False,
            default=str(uuid.uuid4())),
   Field('title'),
   Field('menu', length=128, readable=False, writable=False),
   Field('public', 'boolean', default=False),
   Field('active', 'boolean', default=True),
   Field('body', 'text'),
   Field('tags', 'list:integer'),
   Field('created_by', db.auth_user, default=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, readable=False,
            writable=False),
   migrate=False

)
db.page_index.title.requires = [IS_NOT_EMPTY(), SlugValidator()]
db.page_index.created_by.represent = represent_author

db.define_table('document',
   Field('slug', length=128, readable=False, writable=False),
   Field('name'),
   Field('description', 'text'),
   Field('file', 'upload'),
   Field('created_by', db.auth_user, default=who, update=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, update=now, readable=False,
            writable=False),
   migrate=False

)

db.document.slug.requires = IS_IN_DB(db, 'page.slug', '%(title)s')
db.document.name.requires = IS_NOT_EMPTY()
db.document.file.requires = IS_NOT_EMPTY()
db.document.created_by.represent = represent_author
## slide show imafes
db.define_table('image',
                Field ('id', 'integer'),
		Field('show'),
                Field('title'),
                Field('file', 'upload')
)
db.define_table('topics',

                Field ('id', 'integer'),
                Field ('page_id', 'integer'),
                Field ('English', 'string'),
                Field ('Language', 'string')
)
db.topics.page_id.requires = IS_IN_DB(db, 'page.id')
db.define_table('dialect',
	Field('id',  'integer' , requires=IS_NOT_EMPTY() ),
	Field('name'),
	Field('color'),
	Field('next'),
	migrate=False
)


if language!="Bundjalung":
   dblanguage.define_table (language,

        Field('id', 'integer' , readable=False, writable=False),
        Field('Category',requires=IS_NOT_EMPTY()),
        Field('English',requires=IS_NOT_EMPTY()),
        Field(language,requires=IS_NOT_EMPTY()),
        Field('ExampleSentence'),
        Field('ExampleTranslated'),
        Field('Derived'),
        Field('RelatedWord'),
        Field('Image'),
        Field('SoundFile'),
        migrate=False
        )
else:
   dblanguage.define_table (language,

        Field('id', 'integer' , readable=False, writable=False),
        Field('Category'),
	Field('sense'),
	Field('uncertain'),
        Field('Language_Word',requires=IS_NOT_EMPTY()),
        Field('Part_of_Speech'),

	Field('English',requires=IS_NOT_EMPTY()),
        Field('Search_English',requires=IS_NOT_EMPTY()),

        Field('Scientific'),
        Field('Comment'),
        Field('Gold_Coast_Tweed'),
        Field('Lower_Richmond'),
        Field('Middle_Clarence'),
        Field('Condamine_Upper_Clarence'),
        Field('Copmanhurst'),
        Field('RelatedWord'),
        Field('Image'),
        Field('SoundFile'),
	Field('Lesson'),
        migrate=False
        )
   dblanguage.define_table (language+"_archive",
	Field('current_record',dblanguage.Bundjalung), dblanguage.Bundjalung, format = '%(id) %(modified_on)s', migrate=False)

current.db=dblanguage

dblanguage.define_table('images',
                Field('id','integer',writable=False,readable=False),
                Field('name',requires=IS_NOT_EMPTY()),
                Field('title',requires=IS_NOT_EMPTY()),
                Field('filename','upload',requires=IS_NOT_EMPTY(),autodelete=True),
		Field('category','string'),
                migrate=False)
dblanguage.define_table (language+'Examples',

        Field('id', 'integer' , readable=False, writable=False),
        Field('language_id'),
        Field('Language',requires=IS_NOT_EMPTY()),

        Field('English',requires=IS_NOT_EMPTY()),
        migrate=False
        )

dblanguage.define_table('post',
   Field('image_id', 'reference image'),
   Field('author'),
   Field('email'),
   Field('body', 'text'),migrate=False)


db.define_table('comment',
   Field('slug', length=128, readable=False, writable=False),
   Field('body', 'text'),
   Field('created_by', db.auth_user, default=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, readable=False,
            writable=False),
   migrate=False)

db.comment.slug.requires = IS_IN_DB(db, 'page.slug', '%(title)s')
db.comment.body.requires = IS_NOT_EMPTY()
db.comment.created_by.represent = represent_author

db.define_table('calendar_event',
   Field('id', 'integer' , readable=False, writable=False),
   Field('desc', 'text'),
   Field('date_and_time', 'datetime'),
   Field('created_by', db.auth_user, default=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, readable=False,
            writable=False),
   migrate=False

)
#import altk
#from altk import *
#language_dictionary = altk.dictionary.AboriginalLanguageDictionary()
#language_stemmer = altk.stemmer.AboriginalLanguageStemmer()

users = db(db.auth_user.id > 0).select()
usernames = dict([(u.id, '%s %s' % (u.first_name, u.last_name)) for u in users])
usernames[0] = usernames[None] = 'Anonymous'

if not db(db.auth_group.role == 'developer').select():
    group_id = auth.add_group('developer')
    auth.add_membership(group_id, 1)

response.title = T('Bundjalung-Yugambeh Dictionary')
response.menuTop = [
        ['Home', False, URL(r=request, c='plugin_wiki', f='index.html')],
        ['About Us', False, URL(r=request, c='plugin_wiki',f='page', args='about_us')],
     ['Dictionary', False, URL(r=request, c='language',f='dictionary')],
	['Resources', False, URL(r=request, c='plugin_wiki', f='resources')],

	['Help', False, URL(r=request,c='plugin_wiki', f='tags_by_tag', args='17')],
        ['Contact', False, URL(r=request, c='plugin_wiki', f='contact')],
     ]

response.menuAbout = [
      ['People', False, URL(r=request, c='plugin_wiki', f='page', args='people')],
      ['Traditional country', False, URL(r=request, c='plugin_wiki', f='page', args='traditional_country')],
      ['Language background', False, URL(r=request, c='plugin_wiki', f='page', args='language_background')],
      ['Outline of the language', False, URL(r=request, c='plugin_wiki', f='page', args='outline_of_the_language')],
           ['Outline of resources', False, URL(r=request, c='plugin_wiki', f='page', args='outline_of_resources')],
      ['History of the project', False, URL(r=request, c='plugin_wiki', f='page', args='history')],

]
response.menuResource=[
      ['Dictionary Book', False, URL(r=request, c='plugin_wiki', f='page', args='dictionary')],
      ['Language Resources', False, URL(r=request, c='plugin_wiki', f='resources')],
      ['Written examples', False, URL(r=request, c='plugin_wiki', f='page', args='written_examples_of_the_language')],
      ['Work Sheets', False, URL(r=request,c='learning',f='pages')],
    ]
response.menuUploads=[
	['Audio Files',False,URL(r=request, c='default', f='upload', args='sounds')],
	['Images', False, URL(r=request, c='default', f='upload', args='images')]
]

response.menuLogin=[
      ['Login', False, URL(r=request, c='default' , f='_user', args='login')],
    ]
    
if auth.is_logged_in():

       	response.menuTop.insert(4,
                   ['Uploads', False, URL(r=request, c='default', f='uploads')])
	response.menuTop.insert(5,

		['Change Password', False, URL(r=request, c='default', f='user', args='change_password')])

	response.menuLogin=[
	      ['Logout', False, URL(r=request, c='default', f='user', args='logout')],
	    ]
	if (auth.user.Role_Name=="editor"):

 		response.menuTop.insert(4,
		     ['Edit Profile', False, URL(r=request, c='default', f='user', args='profile')])
    	elif (auth.has_membership(auth.id_group('developer'))):
		response.menuTop.insert(4,
        		['Accept Regos', False, URL(r=request, c='appadmin', f='update', args="db.auth_user/registration_key/pending")])

def menu_rec(items):
    return [(x.title,None,URL('default', 'menu',
        args=pretty_url(x.id, x.slug)), menu_rec(x.children)) for x in items or []]

def slug(page):
    return page.slug

def email_all_user(sender,message,subject="group notice"):
    import smtplib
    fromaddr=sender
    toaddrs=[x.email for x in db().select(db.auth_user.email)]
    msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,", ".join(toaddrs),subject,message)
    server = smtplib.SMTP('localhost:25')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def email_user(sender,message,subject="Web Contact"):
    import smtplib
    fromaddr=sender
    toaddrs=[EMAIL_SENDER]
    msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,", ".join(toaddrs
),subject,message)
    server = smtplib.SMTP(EMAIL_SERVER+':25')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def email_user(sender,message,subject="Web Contact"):
        from gluon.tools import Mail
	fromaddr=sender
        toaddrs=[EMAIL_SENDER]
        msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,", ".join(toaddrs),subject,message)
        mail=Mail()
        mail.settings.server=EMAIL_SERVER+":25"
        mail.settings.sender=EMAIL_SENDER
        mail.send(to=EMAIL_SENDER,subject=subject, message=msg)
      
##generic functions for layout

def slideshow(links=None,table=None,stage=0,field='image',transition='fade',width=200,height=100):
        """
        ## Embeds a slideshow
        It gets the images from a table

        - ``table`` is the table name
        - ``field`` is the upload field in the table that contains images
        - ``transition`` determines the type of transition, e.g. fade, etc.
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        """
        import random
        id=str(random.random())[2:]
        if table:
                rows = db(db[table].show==stage).select()
                if db[table][field].type=='upload':
                        images = [IMG(_src=URL('default','download',args=[row[field],'images']), _width=width,_height=height) for row in rows]
                else:
                        images = [IMG(_src=row[field]) for row in rows]
        elif links:
               images = [IMG(_src=link) for link in links.split(',')]
        else:
               images = []
        return DIV(SCRIPT("jQuery(document).ready(function() {jQuery('#slideshow%s').cycle({fx: '%s'});});" % (id,transition)),DIV(_id='slideshow'+id,_height=height,*images))


