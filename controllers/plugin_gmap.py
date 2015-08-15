
def index():

    width = request.vars.width or 500
    height = request.vars.height or 500

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
		row.plugin_gmap_popup = plugin_gmap.represent(row)
		row.login = auth.is_logged_in()
        except:
                pass
    for alc in alcs:
        alc.plugin_gmaps_alc=plugin_gmaps.alcs(alc)
        alc.plugin_gmaps_color = plugin_gmaps.color(alc)
        alc.plugin_gmaps_image= plugin_gmaps.image(alc)
        alc.plugin_gmaps_address=plugin_gmaps.address(alc)
  	alc.login=auth.is_logged_in()  
    return dict(width=width, height=height, alcs=alcs,  rows=rows)



def user():
	redirect(URL(r=request, c='default', f='user'))

#view many clws
def clws():
    if not request.args:
        redirect(URL(r=request, c='plugin_gmap', f='alcs'))
    alc=request.args(0) or ''
    clws=''
    try:
      	clws=dblanguage(dblanguage.CLW.id>0)( dblanguage.CLW.ALC==alc).select( orderby=dblanguage.CLW.CLW)
    	alc=dblanguage.ALC[alc].ALC

    except:
    	alc=alc.replace('_',' ')

        alcs=dblanguage.ALC(ALC=alc)
        if alcs: 
        	clws=dblanguage(dblanguage.CLW.id>0)( dblanguage.CLW.ALC==alcs.id).select( orderby=dblanguage.CLW.CLW)
 
    if not clws:
        redirect(URL(r=request, c='plugin_gmap', f='create_clws'))
    return dict(alc=alc,clws=clws)

# view one clws table
def clw():
    name = request.args(0) or ''
    if not request.args:
        redirect(URL(r=request, c='plugin_gmap' ,f='alcs'))
    dbase=request.args(1)

    if not dbase: dbase="CLW"
    else: dbase= 'CLW'+str(dbase)

    clw = dblanguage(dblanguage.CLW.CLW==request.args(0)).select()
    id=clw[0].id
    if not dbase: dbase="CLW"
    w = db[dbase]
    clw= request.args(0).replace('_',' ') 
    data=dblanguage[dbase](CLW=clw)
    
    if not data:
        
  	redirect(URL(r=request, c='plugin_gmap', f='create_clws', args=clw))
    if not (data.image):
       data.image=dblanguage.ALC(id=data.ALC).image
    form=crud.read(w,data.id)
    data.ALC_Name=dblanguage.ALC(id=data.ALC).ALC
    data.base =request.args(1)
    if not(data.image):
	data.image=dblanguage.ALC(id=data.ALC).image
    return  dict(data=data,form=form)

def alcs():
    alcs=dblanguage(dblanguage.ALC.ALC_id>0).select(orderby=dblanguage.ALC.id)
    if not alcs:
        redirect(URL(r=request, c='plugin_gmap',f='create_clws'))
    return dict(language=language, alcs=alcs)

# view clws of one alc
def alc():
    if not request.args:
        redirect(URL(r=request, c='plugin_gmap', f='alcs'))
    dbase=request.args(1)
    
    if not dbase: dbase="ALC"
    else: dbase= 'ALC'+str(dbase)

    id = request.args(0)
    if not dbase: dbase="ALC"
    data=dblanguage[dbase](ALC_id=id)

    if not data:
        redirect(URL(r=request, c='plugin_gmap', f='create_alc'))
    return dict(dbase=dbase,data=data)

# create clws
@auth.requires_login()
def create_clws():
    if not request.args:
        redirect(URL(r=request,c='plugin_gmap', f='alcs'))
    create_clws = request.args(0)
    name=create_clws.replace('_',' ')

    alc=dblanguage.ALC(ALC=name)
    dblanguage.CLW.ALC.default=alc.id
    form = crud.create(dblanguage.CLW)
    return dict( alc=alc, form=form)

    
# edit clws
@auth.requires(auth.user and (auth.user.ALC_Staff or auth.user.CLW_Staff) )
def edit_clw():

    name = request.args(0) or ''
    w = dblanguage.CLW
    name=name.replace('_',' ')
 
    clws = w(CLW=name)
    if not clws:
        clws = w.insert(CLW=name)
    ALC_Name=dblanguage.ALC(id=clws.ALC).ALC_Name

    if not (auth.user.ALC_Name == ALC_Name or auth.user.CLW_Name==name ):
       redirect(URL(r=request, c='plugin_gmap',f='clw', args=request.args) )
    form = crud.update(w, clws, deletable=True, onaccept=crud.archive,
                       next=URL(r=request,c='plugin_gmap', f='clw',args=request.args))
    return dict(form=form,clws=clws)

@auth.requires(auth.user and (auth.user.ALC_Staff or auth.user.CLW_Staff) )
def clws_history():
    """
    show clws changelog
    """
    slug = request.args(0)
    w = dblanguage.CLW
    h = dblanguage.CLW_archive
    page = w(slug=slug)
    history = dblanguage(h.current_record==page.id).select(orderby=~h.modified_on)
    return dict(page=page, history=history)

 
# edit alc 
@auth.requires(auth.user and auth.user.ALC_Staff )
def edit_alc():
    if not request.args:
        session.flash = T('Invalid page')
        redirect(URL(r=request, c='plugin_gmap',  f='alcs'))
    try:
        w = dblanguage.ALC
        db_id = int(request.args(0))
	alcs = w(id=db_id)
    except (ValueError, TypeError):
        session.flash = T('Invalid data id')
        redirect(URL(r=request,c='plugin_gmap', f='clws'))
    else:
	data = dblanguage.ALC[db_id]
        if not data:
            session.flash = T('Invalid ALC id')
            redirect(URL(r=request, c='plugin_gmap', f='alcs'))
	if not (auth.user.ALC_Name==data.ALC_Name or auth.has_membership(role='developer')):
                redirect(URL(r=request, c='plugin_gmap',f='alc', args=request.args) )
	form = crud.update(w, alcs, deletable=True, onaccept=crud.archive,
                       next=URL(r=request,c='plugin_gmap', f='alc', args=request.args))

        return dict(data=data, form=form)


@auth.requires(auth.user and (auth.user.ALC_Staff or auth.user.CLW_Staff) )
def create_alc():
	 
    form= crud.create(dblanguage.ALC,
                               next=URL(r=request, c='plugin_gmap', f='alcs'))
    return dict(form=form)

