
import json, csv
import gzip
import rdflib
import hashlib
import string
import argparse
import sys, os
import re,codecs,collections
import json, pprint


from rdflib.namespace import XSD



#patterns
entry=re.compile(r'\\tx[\w\W]*?\\lx')
#each word divided by lexocon entry
Speech=re.compile(r'\\tx[\w\W]*?\\')
#Language_Word at start of word
Start=re.compile(r'\\ELANBegin[\w\W]*?\\')
#domain - may need to replace
End=re.compile(r'\\ELANEnd[\w\W]*?\\')
#Comments
Translation=re.compile(r'\\ft[\w\W]*?\n')
#part of speech

from collections import OrderedDict


import codecs

def shoebox_to_dictlist(typefile):
    """Convert a typesetting file to list of dictionaries,
    one per headword"""

    result=[]

    with codecs.open(typefile,"r", "utf-8") as fd:
        typetext = fd.read()
    fd.close()
    os.remove(typefile)
    results=split_entries(typetext)
    #print (results)
    return results

def split_entries(typetext):
    """Extract information from each dictionary entry
    Return a dictionary with the entry properties.
    """
#line_info_default=OrderedDict([
#        ('id',1),
 #       ('Speech' , ""),
  #      ('Translation',''),
   #     ('Start',""),
    #    (  'End',"")
     #   ])

    line_info_default= {
        'speech' : "",
        'translation':'',
        'start':"",
          'end':""
        }

    entries=[]

    word_count= 1


    #find Language_Word
    matches=entry.findall(typetext)


    if matches:
        for wordlist in matches:

            ##print ('word:', wordlist)
            line_info = line_info_default.copy()
		#do not know starting id
            #line_info['id']=word_count
            #collect the first \\ separated part and remove \\lx

            line_info['speech']=clean_char(Speech.search(wordlist),'\\tx')
            line_info['start']=clean_char(Start.search(wordlist),'\\ELANBegin')
            line_info['end']=clean_char(End.search(wordlist),'\\ELANEnd')
            line_info['translation']=clean_char(Translation.search(wordlist),'\\ft')


            ordered_fieldnames = line_info #OrderedDict(line_info)
            entries.append(ordered_fieldnames)

            word_count=word_count+1



            #return words and examples as separate lists

    return entries


mapping=collections.OrderedDict([
    ('\\',''),
    ('\n',' ')])



def clean_char(text, extra,group=True):
    #remove special chars
    iter=0
    if text:
        if group:
            text=text.group(0)

        text=re.sub(re.escape(extra), '', text).strip(' ')
        text=re.sub(re.escape('\r'), ' ', text).strip(' ')
        for item in mapping:

                text=re.sub(re.escape(item), mapping[item], text)

                iter+=1
        text=text.strip(' ')

    return text








if __name__=="__main__":



        fileoutW='elanCrowley_3222A.tbt'

        filedir='./'
        filename='Crowley_3222A.tbt'

        #words and examples as separate lists
        text=shoebox_to_dictlist(filedir+filename)


        words=text

        keys = words.keys()

        with codecs.open(filedir+fileoutW, 'w+',encoding='utf8') as output_file:

            dict_writer = csv.DictWriter(output_file, fieldnames=keys,dialect='excel',delimiter=';')
            dict_writer.writeheader()

            dict_writer.writerows(words)
            #Which one?
            #for row in words:


                #word = {key: row[key] for key in keys}
               #
                #dict_writer.writerows(word)


