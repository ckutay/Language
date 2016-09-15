
import json, csv
import gzip
import hashlib
import string
import argparse
import sys, os
import re,codecs,collections
import json, pprint
from collections import OrderedDict





#patterns
#each word divided by lexocon entry
entry=re.compile(r'\\lx[\w\W]*?\\dt')
#Language_Word at start of word
Language_Word=re.compile(r'\\lx[\w\W]*?\\')
#domain - may need to replace
Category=re.compile(r'\\do[\w\W]*?\\')
#Comments
Comment=re.compile(r'\\co[\w\W]*?\\')
#part of speech
Part_of_Speech=re.compile(r'\\ps[\w\W]*?\\')

Search_English=re.compile(r'\\re[\w\W]*?\\')
Sense=re.compile(r'\\se[\w\W]*?\\')
English=re.compile(r'\\de[\w\W]*?\\')
Scientific=re.compile(r'\\sf[\w\W]*?\\')
Gold_Coast_Tweed=re.compile(r'\\rfg[\w\W]*?\\')
Lower_Richmond=re.compile(r'\\rfb[\w\W]*?\\')
Middle_Clarence=re.compile(r'\\rfk[\w\W]*?\\')
Condamine_Upper_Clarence=re.compile(r'\\rfr[\w\W]*?\\')
Copmanhurst=re.compile(r'\\rfo[\w\W]*?\\')

example_line=re.compile(r'\\xv[\w\W]*?\\xv')
example_line1=re.compile(r'\\xv[\w\W]*?\\')
example_line2=re.compile(r'\\xe[\w\W]*?\\')


import codecs

def toolbox_to_dictlist(typefile):
    """Convert a typesetting file to list of dictionaries,
    one per headword"""

    result=[]

    with codecs.open(typefile,"r", "utf-8") as fd:
        typetext = fd.read()
    fd.close()
    results=split_entries(typetext)
    #print (results)
    return results

def split_entries(typetext):
    """Extract information from each dictionary entry
    Return a dictionary with the entry properties.
    """

    line_info_default={
        'id':1,
        'Language_Word' : "",
        'Part_of_Speech':"",
        'Sense':"",
        'Category':'',
        'English':'',
        'Search_English':'',
        'Scientific':'',
        'example':[],
        'Comment':'',
        'Gold_Coast_Tweed':'',
        'Lower_Richmond':'',
        'Middle_Clarence':'',
        'Condamine_Upper_Clarence':'',
        'Copmanhurst':'',
        'rest':''
    }
    example_info_default={
        'language_id':1,
        'Language' :'',
        'English':''}

    entries=[]
    examples=[]
    word_count= 1


    #find Language_Word
    matches=entry.findall(typetext)




    if matches:
        for wordlist in matches:


            ##print ('word:', wordlist)
            line_info = line_info_default.copy()

            line_info['id']=word_count
            #collect the first \\ separated part and remove \\lx

            line_info['Language_Word']=clean_char(Language_Word.search(wordlist),'\\lx')
            line_info['Part_of_Speech']=clean_char(Part_of_Speech.search(wordlist),'\\ps')
            line_info['English']=clean_char(English.search(wordlist),'\\de')
            line_info['Sense']=clean_char(Sense.search(wordlist),'\\se')

            line_info['Search_English']=clean_char(Search_English.search(wordlist),'\\re')
            line_info['Category']=clean_char(Category.search(wordlist),'\\do')
            line_info['Category']=domain_expand(line_info['Category'])
            line_info['Scientific']=clean_char(Scientific.search(wordlist),'\\sf')

            line_info['Comment']=clean_char(Comment.search(wordlist),'\\co')
            line_info['Gold_Coast_Tweed']=clean_char(Gold_Coast_Tweed.search(wordlist),'\\rfg')
            line_info['Lower_Richmond']=clean_char(Lower_Richmond.search(wordlist),'\\rfb')
            line_info['Middle_Clarence']=clean_char(Middle_Clarence.search(wordlist),'\\rfk')

            line_info['Condamine_Upper_Clarence']=clean_char(Condamine_Upper_Clarence.search(wordlist),'\\rfr')

            line_info['Copmanhurst']=clean_char(Copmanhurst.search(wordlist),'\\rfo')
            ##collect examples
            example_list=None
            examples_line=example_line.findall(wordlist)
            #print (wordlist)
            examples_line1=example_line1.findall(wordlist)
            #print (examples_line1)
            examples_line2=example_line2.findall(wordlist)

            for i, item  in enumerate(examples_line):
                example_info=example_info_default.copy()
                example_info['id']=word_count
                examples_line1[i]=clean_char( examples_line1[i], 'xv',False)
                example_info['Language']=examples_line1[i]
                examples_line2[i]=clean_char( examples_line2[i], 'xe',False)
                example_info['Translation']=examples_line2[i]
                if i==0:
                    example_list=[]

                ordered_fieldnames = OrderedDict(example_info)

                example_list.append( ordered_fieldnames)


            if example_list:

                    examples.append(example_list)

            ordered_words = OrderedDict(line_info)


            entries.append( ordered_words)

            word_count=word_count+1



            #return words and examples as separate lists

    return [entries, examples]


mapping=collections.OrderedDict([
    ('\\',''),
    ('\n',' ')])

def domain_expand(text):

    if not text: return text
    if "an" in text:
        text=re.sub("an", "animal", text)
    if "pl" in text:
        text=re.sub("pl", "plant", text)
    if "pp" in text:
        text=re.sub("pp", "people", text)
    if "lg" in text:
        text=re.sub("lg", "language", text)
    if "ti" in text:
        text=re.sub("ti", "time", text)
    if "art" in text:
        text=re.sub("art", "artifact", text)
    if "bp" in text:
        text=re.sub("bp", "body_part", text)
    if "ff" in text:
        text=re.sub("ff", "food", text)

    if "bd" in text:
        text=re.sub("bd", "bird", text)

    if "loc" in text:
        text=re.sub("loc", "location", text)

    if "ne" in text:
        text=re.sub("ne", "natural_environment", text)

    if "ins" in text:
        text=re.sub("ins", "insect", text)
    if "fsh" in text:
        text=re.sub("fsh", "fish", text)
    if "cl" in text:
        text=re.sub("cl", "colour", text)
    if "rep" in text:
        text=re.sub("rep", "reptile", text)
    return text

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


def get_part(text, word_part, pattern, line_txt,sub_str=1, exitnum=0, many=False):



    return text






if __name__=="__main__":

        POSSIBLE_UTF8_SEQUENCE=re.compile(r'[â€°Ã›Ã’Ã©â€“]')

        fileoutA='MYSQLExportAll.csv'
        fileoutW='MYSQLExportWords.csv'
        fileoutE='MYSQLExportExamples.csv'
        filedir='./'
        filename='ToolboxOutput.txt'

        #words and examples as separate lists
        text=toolbox_to_dictlist(filedir+filename)


        words=text[0]

        keys = words[0].keys()
        print(keys)
        with codecs.open(filedir+fileoutW, 'w+',encoding='utf8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys,dialect='excel')
            dict_writer.writeheader()

            dict_writer.writerows(words)
            #Which one?
            #for row in words:


                #word = {key: row[key] for key in keys}
               #
                #dict_writer.writerows(word)

        examples=text[1]

        keys=examples[0][0].keys()
        with codecs.open(filedir+fileoutE, 'w+',encoding='utf8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)

            dict_writer.writeheader()
            for word in examples:

                
                dict_writer.writerows(word)

#fix me - need to exttract sense from category

    #output to RDF
