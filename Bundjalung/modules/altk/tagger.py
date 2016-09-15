# 2014.07.21 13:51:05 EST
# Embedded file name: C:\PROGRA~1\Python25\Lib\SITE-P~1\altk\tagger.py
import nltk
import dictionary
#
verb_patterns = [('.*ni$', 'VER+PRS'),
 ('.*nyun$', 'V+S'),
 ('.*ye$', 'V+POT'),
 ('.*n$', 'V+NOM'),
]
noun_patterns = []
misc_patterns = [('[^A-Za-z0-9]', 'PCT'), ('^-?[0-9]+(.[0-9]+)?$', 'CN')]
sample_verbs = []

class AboriginalLanguageTagger:
    wdict = dictionary.AboriginalLanguageDictionary()
    pos_lookup = wdict.getPartDict()
    tag_lookup = {}

    def __init__(self):
        noun_tagger = nltk.RegexpTagger(noun_patterns)
        verb_tagger = nltk.RegexpTagger(verb_patterns)
        for word, pos in self.pos_lookup.items():
            if pos == 'N':
                self.tag_lookup[word] = 'NOU+ABS'
            elif pos == 'ADJ':
                self.tag_lookup[word] = 'ADJ+ABS'
            else:
                self.tag_lookup[word] = pos

    def tag(self, words):
        noun_tagger = nltk.RegexpTagger(noun_patterns)
        verb_tagger = nltk.RegexpTagger(verb_patterns, backoff=noun_tagger)
        misc_tagger = nltk.RegexpTagger(misc_patterns, backoff=verb_tagger)
        AboriginalLanguage_tagger = nltk.UnigramTagger(model=self.tag_lookup, backoff=misc_tagger)
        return AboriginalLanguage_tagger.tag(words)
# okay decompyling tagger.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2014.07.21 13:51:06 EST
