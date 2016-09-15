# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import gluon.contrib.simplejson


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(pages=auth.wiki('help'))

def display_results():
    form = FORM(TABLE(TR('Experiment ID:',
              INPUT(_name='experiment_id', requires=IS_NOT_EMPTY())),
	     TR('Stage Number (optional)', INPUT(_name='stage_number' )),
		TR('Round ID',INPUT(_name='round_id')),
		TR(INPUT(_name='name',_value="Results",_type="hidden")),
              TR("",INPUT(_type='submit'))))
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL(f='results',vars=request.vars))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)


def help():

    return auth.wiki('help')

def participant():
    if (request.vars):
        value=request.vars
        variable=value.keys()
	participant=None

        #check what order put in - exp_id set and variableData is being reviewd
        if (variable[0]=="experiment_id"):
                participant=variable[1]
                exp_id=value[variable[0]]

	else:
            try:
                participant=variable[0]
                exp_id=value[variable[1]]
            except:
                return " You need to provide experiment id"
        ip = request.client
        part=db.participant((db.participant.IP==ip))
        ##check to see if cna fit in experiment
        max_participants=db.setupExperiment((db.setupExperiment.name=="max_participants")&(db.setupExperiment.experiment_id==exp_id))['valueString']
        parts=db(db.experiment_participant.experiment_id==exp_id)
	#eresetting to zero
	if value["participant"]=="-1":
                parts.delete()
                        ##reset participant to zero and return values
                ret=db.setupExperiment((db.setupExperiment.name=="participant") & (db.setupExperiment.experiment_id==exp_id))
                ret.update_record(valueString=0)
                db.commit()
		return "Start New Group as Host Server"
	#expereiment not fulli add expereimenter
	elif value["participant"]=="0":
		returnvar= dict([("message","experimenter"),("participant","0"),("experimental_id",exp_id),("participant_id","0")])
		return gluon.contrib.simplejson.dumps(returnvar)

	elif ((parts.count())<max_participants):
                if (part==None):
                        part_id=db.participant.insert(IP=ip,model_name="default")

                else:
                        part_id=part['id']
	else:
		returnvar= dict([("message","full"),("participant","-1"),("experimental_id",exp_id),("participant_id","-1")])
		return gluon.contrib.simplejson.dumps(returnvar)


	#setup participatn in experiment as there is room
	db.experiment_participant.insert(experiment_id=exp_id,participant_id=part_id)
        db.commit()
	#get exisitng setup data
        ret=db.setupExperiment((db.setupExperiment.name=="participant") & (db.setupExperiment.experiment_id==exp_id))
        if (ret==None):
		# no entry for participants, so create one
                if value["participant"]!="":
                        db.setupExperiment.insert(name="participant", valueString=value["participant"], experiment_id=exp_id)
                        db.commit()
			returnvar= dict([("participant",str(value["participant"])),("experimental_id",exp_id), ("participant_id",part_id)])
                        return gluon.contrib.simplejson.dumps(returnvar)
                else:
                        return "Please enter value for participant"
	#if paricipant number set and already exists
        if (value["participant"]!=""):
		#done zero already
                ##if integer increment, if not, just put in data given
                ret.update_record(valueString=int(ret.valueString)+int(value[participant]))

	#return all values

        returnvar= dict([("participant",str(ret.valueString)),("experimental_id",exp_id),("participant_id",part_id)])
        return gluon.contrib.simplejson.dumps(returnvar)
    else:
        return "Error no parameter provided to read for participant"

def reset():
        ret = db().select(db.experiment.ALL)

        form=FORM("Experiment record to delete: ",SELECT(_name='title', *[OPTION(ret[i].title,_value=ret[i].title) for i in range (len(ret))]),INPUT(_type="Submit"))
        if form.accepts(request.vars):

                ret=db.experiment((db.experiment.title==request.vars['title']))
                if (ret!=None):
                        form=FORM(INPUT(_name="experiment_id",_value=ret.id,_type="hidden"),"Delete ?:",INPUT(_type="Checkbox",_name="delete"),INPUT(_type='submit'))
                        returnvar=dict([("Title",ret.title),("ExperimentType",ret.typeExperiment), ("start", False), ("delete",False),("form", form)])

                        return returnvar
                else:
                        return "No such experiment"
        else:
                #second pass- so using different form
                if request.vars:
                        if (request.vars['delete']=='on'):
                        #delete
                                ret=db.setupExperiment((db.setupExperiment.name=="Host_IP") & (db.setupExperiment.experiment_id==request.vars['experiment_id']))
                                if ret:ret.update_record(valueString="127.0.0.1")

                                ret=db.setupExperiment((db.setupExperiment.name=="Port") & (db.setupExperiment.experiment_id==request.vars['experiment_id']))
                                if ret:ret.update_record(valueString="1100")

                                ret=db.setupExperiment((db.setupExperiment.name=="participant") & (db.setupExperiment.experiment_id==request.vars['experiment_id']))
                                if ret:ret.update_record(valueString="0")

                                ret=db((db.results.experiment_id==request.vars['experiment_id']))
                                if (ret):ret.delete()

                                return dict(start=False, delete=True)
                return dict(form=form, start=True, delete=False)

def setup_interface():

        #request for form from interface
        form=FORM("Experiment Title",INPUT(_name="Title"),
                INPUT(_value="max_participants",_type="hidden"),"Maximum Participants: ",INPUT(_name="valueString"),
                INPUT(_value="Host_IP",_type="hidden"),"Host: ",INPUT(_value="127.0.0.1",_name="valueString"),
                INPUT(_value="Port",_type="hidden"),"Port: ",INPUT(_value="1100",_name="valueString"),
                "Type of Experiment",SELECT('coin effort', 'stag and hare' ,_name="typeExperiment"),
                "A Parameter: ", INPUT(_name='valueString'),
                "B Parameter: ", INPUT(_name='valueString'),
                "Rounds : ", INPUT(_name="rounds"),
                INPUT(_type="submit"))
        if form.accepts(request.vars):
                name=['max_participants','Host_IP','Port','a_parameter','b_parameter']
                values=request.vars['valueString']

                #insert experiment name etc
                exp_id=db.experiment.insert( title=request.vars['Title'],typeExperiment=request.vars['typeExperiment'],rounds=request.vars['rounds']).id
                
                #now insert the array of named vars
                i=0
                while i<len(values):
                        db.setupExperiment.insert(name=name[i], valueString=values[i], experiment_id=exp_id)
                        i+=1
                #default
                db.setupExperiment.insert(name="participant", valueString=0, experiment_id=exp_id)
                response.flash = 'form accepted'
                #cheating a bit
                return dict(form="Experiment entered, id ="+str(exp_id))
        elif form.errors:
                response.flash = 'form has errors'
        else:
                response.flash = 'please fill the form'
        return dict(form=form)


def setup():
    if (request.vars):
	value=request.vars
    	variable=value.keys()
	#check what order put in - exp_id set and variableData is being reviewd
        if (variable[0]=="experiment_id"):
		variableData=variable[1]
		exp_id=value[variable[0]]
	else:
	    try:
		variableData=variable[0]
		exp_id=value[variable[1]]
	    except:
		return " You need to provide experiment id"
	#setup has all paraamenter set

        ret=db.setupExperiment((db.setupExperiment.name==variableData) & (db.setupExperiment.experiment_id==exp_id))
	#if this experiment data not entered yet
	if (ret==None):
		if value[variableData]!="":
			db.setupExperiment.insert(name=variableData, valueString=value[variableData], experiment_id=exp_id)
                	db.commit()
			returnvar= dict([(variableData,str(value[variableData])),("experimental_id",exp_id)])
			return gluon.contrib.simplejson.dumps(returnvar)
		else:
			return "Please enter value for "+variableData
    	if (value[variableData]!=""):
        	if value[variableData]=="0":
                	ret.update_record(valueString=0)
        	else:
			ret.update_record(valueString=value[variableData])

	returnvar= dict([(variableData,str(ret.valueString)),("experimental_id",exp_id)])
    	return gluon.contrib.simplejson.dumps(returnvar)
    else:
	form
        return "Error no parameter provided to read from data"
   
def experiment():
    type=['Unknown','stag and hare', 'coin effort']
    if (request.vars):
        value=request.vars
        variable=value.keys()
	## if id given
        if (value['id']>0):
		ret=db.experiment(db.experiment.id==value['id'])
	else:
		
	##check if exists by title and return id
		ret=db.experiment(db.experiment.title==value['title'])
        if (ret!=None):
		##return if already found
		returnvar = dict([("id",ret["id"])])
		return gluon.contrib.simplejson.dumps(returnvar)

	else:
		#create if can, if not send error
		try:
			ret=db.experiment.insert(title=value['title'], typeExperiment=type[int(value['type'])], rounds=value['rounds'])
                	db.commit()
			returnvar = dict([("id",ret['id']), ("title",ret['title']),("typeExperiment",ret['typeExperiment']),("rounds",ret['rounds'])])
			return gluon.contrib.simplejson.dumps(returnvar)

		except Exception, e:
			
			return "Error no parameter or incorrect parameter provided for data entry [title,type,rounds(number): %s" %e

    else:
        return "Error no parameter provided to read from data"

def check_part(value, stage_id):
    type=['Request', 'Receive', 'Wait','End']
    # not return if not all participants ready
    participants=db((db.results.experiment_id==value['experiment_id'])&(db.results.stage_id==stage_id)&(db.results.name=="response"))
    parts=db(db.experiment_participant.experiment_id==value['experiment_id'])
    if int(participants.count())<int(parts.count()):
        returnvar = dict([("id",value["id"]),("experiment_id",value['experiment_id']), ("stage_number",value['stage_number']),("type_stage",type[2])])
	return gluon.contrib.simplejson.dumps(returnvar)

def stages():
    type=['Request', 'Response', 'Wait','End']
    # not return if not all participants
    if (request.vars):
        value=request.vars
        variable=value.keys()
	stage_number=int(value["stage_number"])
	if stage_number>0:
	   try:
                ret=db.stages((db.stages.experiment_id==value['experiment_id'])&(db.stages.stage_number==(int(value["stage_number"]))))
                stage_id=db.stages(db.stages.stage_number==stage_number).id

           except Exception, e:
                return "Stage_number required "+str(e)
	   if (ret==None): step=type[2]
	   else: step=ret.type_stage
##check if participants full or results full as appropraite for that stage
	   if step==type[1] or step==type[2]:
		typeS="participants"
	   else:
		typeS="results"	
        ## if id given
        if (value['id']>0):
                ret=db.stages(db.stages.id==value['id'])

	if (stage_number==0 or complete(value,typeS, stage_id)):
		#completed stage
		stage_number+=1

        ##check if exists by exp and stage number and return id
        	ret=db.stages((db.stages.experiment_id==value['experiment_id'])&(db.stages.stage_number==stage_number))
        	if (ret!=None):
                ##return if already found
                	returnvar = dict([("id",ret["id"]),("experiment_id",ret['experiment_id']), ("stage_number",ret['stage_number']),("type_stage",ret['type_stage']),("message",ret['message'])])
                	return gluon.contrib.simplejson.dumps(returnvar)

        	elif value['stage_number']>0:  
##skip error in entry
                #create if can, if not send error
                	try:
                        	ret=db.stages.insert(experiment_id=value['experiment_id'], type_stage=type[int(value['type'])],stage_number=value['stage_number'] )
                        	db.commit()
                        	returnvar = dict([("id",ret['id']),("experiment_id",ret['experiment_id']),("stage_number",ret['stage_number']),("type_stage",ret['type_stage']),("message",ret['message'])])
                        	return gluon.contrib.simplejson.dumps(returnvar)

                	except Exception, e:

                        	return "Error no parameter or incorrect parameter provided for data entry [experiment_id,stage_number, type]: %s" %e
	else:
		return "Stage not complete"
    else:
        return "Error no parameter provided to read from data eg check stage_number>0"

def get_round():

    if request.vars:
        value=request.vars
        ret=db.setupExperiment((db.setupExperiment.experiment_id==value['experiment_id'])&(db.setupExperiment.name=="rounds"))
    	if ret!=None:
		
		return ret['valueString']
    	else:
		return 1
    else: 
	return "Unknown experiment"

def next_round():
    if request.vars:
	value=request.vars
	ret=db((db.results.experiment_id==value['experiment_id']))
	if ret!=None: 
		rounds=ret.select()
	exp_id=value['experiment_id']
	round_id=1
	for row in rounds:
		if row["round_id"]>=round_id:	
			round_id=row["round_id"]+1
	##add to setupExp
	ret=db.setupExperiment((db.setupExperiment.name=="rounds") & (db.setupExperiment.experiment_id==exp_id))
	if ret!=None:
		ret.update(valueString=round_id)
	else:
	 	db.setupExperiment.insert(name="rounds", valueString=round_id, experiment_id=exp_id)
	db.commit()		
	returnvar=dict([("round_id",round_id)])
        return gluon.contrib.simplejson.dumps(returnvar)
	
##resets experimetn
def delete_results():
    if (request.vars):
        value=request.vars
        variable=value.keys()

 	ret=db((db.results.experiment_id==value['experiment_id'])&(db.results.round_id==value['round_id']))
	ret.delete();
	return "Done"

def exportCSV():
     input=request.args[0]

     experiment_id=int(input[19:])
     results=db(db.experiment.id==experiment_id).select()
     return dict(results=results)

def results():
    if (request.vars):
        value=request.vars
        variable=value.keys()
	stage_id=0

	try:
		ret=db.stages((db.stages.experiment_id==value['experiment_id'])&(db.stages.stage_number==value["stage_number"]))
        	stage_number=value["stage_number"]
        	stage_id=db.stages(db.stages.stage_number==stage_number).id

	except Exception, e:
		##not selected a stage_number
        	stage_id=0
	## if id given
        if (value['id']>0):

                ret=db.results(db.results.id==value['id'])
		return dict(results=ret)
	#request to print results for all rounds
        elif value['name']=="Results":
		exp_id=int(value["experiment_id"])
 		if (stage_id!=0):

                        if (value['round_id']!="") & (value["round_id"]!=None) : ret=db((db.results.experiment_id==exp_id)&(db.results.stage_id==stage_id)&(db.results.round_id==value['round_id'])).select()

                        else: ret=db((db.results.experiment_id==value['experiment_id'])&(db.results.stage_id==stage_id)).select()
                elif (value['round_id']!="") & (value["round_id"]!=None): ret=db((db.results.experiment_id==exp_id)&(db.results.round_id==value['round_id'])).select()
                else:  ret=db((db.results.experiment_id==exp_id)).select()
		exp=db.experiment(db.experiment.id==exp_id)
		logging.warn(experiment)
		stages=db(db.stages.experiment_id==exp_id).select()
                parameters=db(db.setupExperiment.experiment_id==exp_id).select()
		return dict(results=ret, exp=exp, parameters=parameters,stages=stages)

	elif value['name']=="Result":

		part_result=db.results((db.results.experiment_id==value['experiment_id'])&(db.results.stage_id==stage_id)&(db.results.round_id==value['round_id'])&(db.results.participant_id==value['participant_id']))['valueString']
		result=add_results(dict([("experiment_id",value['experiment_id']),("stage_id",stage_id),("round_id",value['round_id'])]))
		exp_type=db.experiment(db.experiment.id==value['experiment_id'])
		if exp_type.typeExperiment=="coin effort":
			a=db.setupExperiment((db.setupExperiment.name=="a_parameter")&(db.setupExperiment.experiment_id==value['experiment_id']))['valueString']

			b=db.setupExperiment((db.setupExperiment.name=="b_parameter")&(db.setupExperiment.experiment_id==value['experiment_id']))['valueString']

			result=float(a)*float(result)-float(b)*float(part_result)
		else:
			pass
		returnvar=dict([("message","Your return is: "),("Results",result)])
		logging.warn("Result")
		logging.warn(results)
		return gluon.contrib.simplejson.dumps(returnvar)
	else:
        ##check if exists by exp and stage number and return id
                try:
			resultEnter=db.results((db.results.experiment_id==value['experiment_id'])&(db.results.participant_id==value['participant_id'])&(db.results.round_id==value['round_id'])&(db.results.stage_id==stage_id)&(db.results.name==value['name'])&(db.results.valueString==int(value['value'])))
		except Exception , e:
			return "Incorrect call to api: "+str(e)
	if (resultEnter!=None):
                ##return if already found
                returnvar = dict([("id",resultEnter["id"]),("experiment_id",resultEnter['experiment_id']),("stage_id",stage_number),("round_id",resultEnter['round_id']),("name",resultEnter["name"]),("value",resultEnter['valueString'])])
                return gluon.contrib.simplejson.dumps(returnvar)

        else:
                try:
                        ret=db.results.insert(experiment_id=value['experiment_id'], participant_id=value['participant_id'],stage_id=stage_id,round_id=value['round_id'],name=value['name'],valueString=int(value['value']))
                        db.commit()
                        returnvar = dict([("id",ret["id"]),("experiment_id",ret['experiment_id']),("stage_number",stage_number),("round_id",ret['round_id']),("name",ret["name"]),("value",ret['valueString'])])
			return gluon.contrib.simplejson.dumps(returnvar)

                except Exception, e:

                        return "Error no parameter or incorrect parameter provided for data entry [experiment_id,participant_id, round_id,name,value]: %s" %e

    else:
        return "Error no parameter provided to read from data"

def add_results(variable):
	results=db((db.results.experiment_id==variable['experiment_id'])&(db.results.stage_id==variable['stage_id'])& (db.results.round_id==variable['round_id'])).select()
	returnResult=[]
	for res in results:	
		returnResult.append(res.valueString)
	ret=min(returnResult)
	return ret
		

def complete(value,step, stage_id):
        variable=value.keys()
        max_participants=db.setupExperiment((db.setupExperiment.name=="max_participants")&(db.setupExperiment.experiment_id==value['experiment_id']))['valueString']
	if step=="participants":parts=db(db.experiment_participant.experiment_id==value['experiment_id'])
	if step=="results":parts=db((db.results.experiment_id==value['experiment_id'])&(db.results.round_id==value['round_id'])&(db.results.stage_id==stage_id))
	if int(parts.count())>=int(max_participants):
		return True
	else:
		return False

 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
