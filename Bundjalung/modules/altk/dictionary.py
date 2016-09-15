# Aboriginal Language Toolkit: Language Dictionary
#
# Author: Alistair Macleod

import stemmer
from gluon import *
import sys 
class AboriginalLanguageDictionary:
    "A class which provides access to data contained in the Aboriginal Language dictionary"

    __langword_pos = {}
    __langword_eng = {}
    __word_pos = {}
    __word_lang = {}
    __al="Bundjalung"
    
    def __init__(self):
    #def start():
    # Connect to the database used to store the Aboriginal Language dictionary
    	dblanguage= current.db #DAL('mysql://language_admin:budyari@localhost/language', pool_size=0,migrate=False, fake_migrate=True)

	dictionary=	dblanguage().select(dblanguage.Bundjalung.ALL)

        # Execute a query to select all relevant items, store in a dictionary
        
        # Close the connection
        #dblanguage.close()

        # Create a stemmer for removing superfluous suffixes
        ws = stemmer.AboriginalLanguageStemmer()
        ps = stemmer.PhoneticStemmer()
        dictionary = self.encodePartofSpeech(dictionary)
        # Create the POS lookup dictionary and the permanent Language/English translation lookup
        for entry in dictionary:
            langword = entry['Language_Word']
  
            langword_pos = entry['Part_of_Speech']
            langword_end = entry['Search_English'].lower()
            #word = ws.stem(langword)

            self.__langword_pos[langword] = entry['Part_of_Speech'].upper()
            self.__langword_eng[langword] = entry['Search_English'].lower()

        for entry in dictionary:
            word = entry['Search_English']
            self.__word_lang[word] = entry['Language_Word']
            self.__word_pos[word] = entry['Part_of_Speech'].upper()
            
    
    def encodePartofSpeech(self,dictionary):
        for entry in dictionary:
            pos= entry['Part_of_Speech']
            posString= pos.strip().split()
            pos=""
            for posItem in posString:
                #check we just have first three letters for pos
                pos+=posItem.upper()[0:3]
            entry['Part_of_Speech']=pos
            
        return dictionary

    # Basic implementation of dictionary lookup functionality
    def getEnglish(self, word):
        if self.__langword_eng.has_key(word):
	    lang= self.__langword_eng[word]
	    langnew=lang.replace(';','[',1)
	    if (langnew!=lang): langnew=langnew+']'

	    lang=langnew+' - '
            return  lang
        else: print "\'" + word + "\'" + " could not be found in the dictionary."

 
    def getLanguage(self, word):
        if self.__word_lang.has_key(word):
            return self.__word_lang[word] +' - '
        else: print "\'" + word + "\'" + " could not be found in the dictionary."
        
    def getPartEng(self, word):
        if self.__langword_eng.has_key(word):
            return self.__langword_pos[word]+' - '
        else: print "\'" + word + "\'" + " could not be found in the dictionary."

    def getPartLang(self, word):
        if self.__langword_pos.has_key(word):
            return self.__langword_pos[word]+' - '
        else: print "\'" + word + "\'" + " could not be found in the dictionary."
        

    def getPartDict(self):
        return self.__langword_pos

    def getAllWords(self):
        return self.__langword_eng.keys()

    def has_word(self,word):
        return self.__langword_eng.has_key(word)

    def has_eng_word(self,word):
	return self.__word_lang.has_key(word)
