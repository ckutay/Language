dblanguage.define_table('CLW',
   Field('id', 'integer'),
   Field('CLW','string'),
   Field('ALC','integer'),
   Field('image','upload',autodelete=True),
   Field('Alt_Name','string'),
     Field('Phone','string'),
  Field('Office_Phone', 'string'),
  Field('Office_Fax', 'string'),
Field('Postal_Address', 'string'),
  Field('Languages', 'string'),
   
 Field('latitude', 'double', default="-25.2328"),
  Field('longitude', 'double', default="130.9872"),

   Field('Location','string', default='NT'),
   Field('Web_URL','string'),
   Field('created_by', db.auth_user, default=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, readable=False,
            writable=False),

   migrate=False)

dblanguage.CLW.created_by.represent = represent_author
dblanguage.CLW.ALC.requires = IS_IN_DB(db, 'ALC.id', '%(ALC)s', multiple=False)
dblanguage.CLW.Web_URL.requires=IS_EMPTY_OR(IS_URL())


dblanguage.define_table('CLW_archive',
                Field('current_record',dblanguage.CLW),
                dblanguage.CLW,
                format = '%(id) %(modified_on)s', migrate=False)

dblanguage.define_table('ALC',
   Field('ALC_id', 'integer',unique=True,readable=False , writable=False),
Field('ALC_Name','string'),
Field('Organisation','string', default='ALC', requires=IS_IN_SET(('ALC','Other Community Organisation'))),
   Field('ALC_Full_Name','string'),
Field('image','upload',autodelete=True),
   Field('Phone', 'string'),
   Field('Office_Phone', 'string'),
Field('Fax', 'string'),
Field('Postal_Address', 'string'),
Field('Email', 'string'),
Field('Description', 'string'),
Field('Chairperson', 'string'),
Field('Web_URL','string'),
Field('Other_Services', 'string'),

  Field('latitude', 'double', default="-25.2328"),
  Field('longitude', 'double', default="130.9872"),
  
Field('History','string'),
Field('Constitution','upload',autodelete=True),
Field('Strategic_Plan','upload',autodelete=True),
Field('Other_docs','upload',autodelete=True),
Field('Languages', 'string'),

Field('Colour','string',default="Red"),
     Field('created_by', db.auth_user, default=who, readable=False,
            writable=False),
   Field('created_on', 'datetime', default=now, readable=False,
            writable=False),
migrate=False)

dblanguage.ALC.Web_URL.requires = (IS_URL())
dblanguage.ALC.created_by.represent= represent_author
dblanguage.ALC.Colour.requires=IS_IN_SET(("Blue","DarkBlue",'Purple','Green','DarkGreen','Yellow','Orange', 'DarkRed','Red','Black','White','Grey','Transparent'))



dblanguage.define_table('ALC_archive',
                Field('current_record',dblanguage.ALC),
                dblanguage.ALC,
                format = '%(id) %(modified_on)s', migrate=False)



from gluon.storage import Storage
plugin_gmap=Storage()
plugin_gmaps=Storage()
plugin_gmaps.set=dblanguage(dblanguage.ALC.id>0)
plugin_gmaps.alcs= lambda row: '%(ALC)s' % {'ALC': row.ALC_Full_Name}
plugin_gmaps.color= lambda row: '%(COLOR)s' % {'COLOR': row.Colour.lower()}
plugin_gmaps.image= lambda row: '%(IMAGE)s' % {'IMAGE': row.image}
plugin_gmaps.address=lambda row: '%(Address)s' %{'Address' : row.Postal_Address}
plugin_gmap.set=dblanguage(dblanguage.CLW.id>0) ### change this to a query that lists records with latitude and longitute
plugin_gmap.id= lambda row: '%(id)s' % {'id': row.ALC}
plugin_gmap.alt=lambda row: '%(Alt Name)s' % {'Alt Name': row.Alt_Name}

plugin_gmap.ALC=lambda row: '%(ALC)s' % {'ALC': dblanguage.ALC(id='%(id)s' % {'id':row.ALC}).ALC_Full_Name}
plugin_gmap.clw=lambda row: '%(CLW)s' % {'CLW': row.CLW}
plugin_gmap.address=lambda row: '%(Address)s' %{'Address' : row.Postal_Address}

plugin_gmap.image= lambda row: '%(image)s' % {"image": row.image or dblanguage.ALC(id='%(id)s' % {'id':row.ALC}).image}
plugin_gmap.represent = lambda row: '%(ALC)s' % {'ALC': row.ALC}
# include plugin in views with {{=LOAD('plugin_gmap')}}

