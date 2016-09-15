
import json, csv
import gzip
import hashlib
import string
import argparse
import sys, os
import re,codecs,collections
import json, pprint



#patterns
#each word divided by lexocon entry
entry=re.compile(r'\\lx[\w\W]*?\\lx')
#lexicon at start of word
lexicon=re.compile(r'\\lx[\w\W]*?\\')
#domain - may need to replace
domain=re.compile(r'\\do[\w\W]*?\\')
#comments
comment=re.compile(r'\\co[\w\W]*?\\')
#part of speech
ps=re.compile(r'\\ps[\w\W]*?\\')

reverse_english=re.compile(r'\\re[\w\W]*?\\')
english=re.compile(r'\\de[\w\W]*?\\')
scientific=re.compile(r'\\sf[\w\W]*?\\')
reference_green=re.compile(r'\\rfg[\w\W]*?\\')
reference_blue=re.compile(r'\\rfb[\w\W]*?\\')
reference_black=re.compile(r'\\rfk[\w\W]*?\\')
reference_red=re.compile(r'\\rfr[\w\W]*?\\')
reference_orange=re.compile(r'\\rfo[\w\W]*?\\')

example_line=re.compile(r'\\xv[\w\W]*?\\xv')
example_line1=re.compile(r'\\xv[\w\W]*?\\')
example_line2=re.compile(r'\\xe[\w\W]*?\\')




def dictlist_to_toolbox(typefile, exfile):
    """Convert a typesetting file to list of dictionaries,
    one per headword"""

    result=[]

    with open(typefile) as fd:
        typetext = fd.read()

    results=combine_entries(typetext, exfile)
    fd.close()
    return results

def combine_entries(typetext, extext):
    """Extract information from each dictionary entry
    Return a dictionary with the entry properties.
    """

    line_info_default={
        'id':1,
        'lexicon' : "",
        'ps':"",
        'domain':'',
        'english':'',
        'reverse_english':'',
        'scientific':'',
        'example':[],
        'comment':'',
        'reference_green':'',
        'reference_blue':'',
        'reference_black':'',
        'reference_red':'',
        'reference_orange':'',
        'rest':''
    }
    example_info_default={
        'id':1,
        'Language' :'',
        'Translation':''}

    entries=[]
    examples=[]
    word_count= 1


    #find lexicon
    matches=entry.findall(typetext)




    if matches:
        for wordlist in matches:


            ##print ('word:', wordlist)
            line_info = line_info_default.copy()

            line_info['id']=word_count
            #collect the first \\ separated part and remove \\lx

            line_info['lexicon']=clean_char(lexicon.search(wordlist),'\\lx')

            line_info['ps']=clean_char(ps.search(wordlist),'\\ps')
            line_info['domain']=clean_char(domain.search(wordlist),'\\do')

            line_info['scientific']=clean_char(scientific.search(wordlist),'\\sf')
            line_info['english']=clean_char(english.search(wordlist),'\\de')

            line_info['reverse_english']=clean_char(reverse_english.search(wordlist),'\\re')
            line_info['comment']=clean_char(comment.search(wordlist),'\\co')
            line_info['reference_green']=clean_char(reference_green.search(wordlist),'\\rfg')
            line_info['reference_blue']=clean_char(reference_blue.search(wordlist),'\\rfb')
            line_info['reference_black']=clean_char(reference_black.search(wordlist),'\\rfk')
            line_info['reference_orange']=clean_char(reference_orange.search(wordlist),'\\rfo')
            line_info['reference_red']=clean_char(reference_red.search(wordlist),'\\rfr')
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
                example_list.append(example_info)


            if example_list:

                    examples.append(example_list)

            entries.append(line_info)

            word_count=word_count+1



            #return words and examples as separate lists

    return [entries, examples]


mapping=collections.OrderedDict([
    ('\\',''),
    ('\n','')])

def clean_char(text, extra,group=True):
    #remove special chars
    iter=0
    if text:
        if group:
            text=text.group(0)

        text=re.sub(re.escape(extra), '', text).strip(' ')
        for item in mapping:

                text=re.sub(re.escape(item), mapping[item], text)

                iter+=1


    return text


def get_part(text, word_part, pattern, line_txt,sub_str=1, exitnum=0, many=False):



    return text





if __name__=="__main__":


        fileinW='MYSQLExportWords.csv'
        fileinE='MYSQLExportExamples.csv'
        filedir='./'
        filename='ToolboxInput.txt'

        #words and examples as separate lists
        text=toolbox_to_dictlist(filedir+fileinW, filedir+fileinE)


        out = open(filename, 'w+',encoding='utf-8')
        for line in text:
              json.dump(line, out, indent=4)
              out.write(os.linesep)
        out.close()


    #output to RDF
