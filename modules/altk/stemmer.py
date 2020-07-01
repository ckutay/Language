# Aboriginal Language Toolkit: Stemmer and related functionality
#
# Author: Alistair Macleod

from nltk.stem.api import *

stem_ay = [
    'yurruga']

stem_rr = [
    'yuwar']

def combine(stem,suffix):
    return [word+suffix for word in stem]

conjunctions = [
    ("-bu", 0, "",  "and", [])
    ]

noun_and_adj_cases = [
    # instrumentive
    ("-duradhu",    0,      "",     "using",     []),

    # dative / gentive
    ("-gu",         1,      "",     "for/of",     []),

    # ablative
    ("aa-dhi",      3,      "y",    "(from)",     []),
    ("a-dhi",       2,      "",     "(from)",     ['ngadhi',combine(stem_ay,'dhi')]),
    ("a-dhi",       2,      "y",    "(from)",     ['ngadhi']),
    ("r-ri",        2,      "",     "(from)",     combine(stem_rr,"ri") + ["-girri","mirri"]),
    ("r-ri",        2,      "r",    "(from)",     ["-girri","mirri"]),
    ("n-dhi",       2,      "",     "(from)",     []),
    ("-li",         1,      "l",    "(from)",     ['bali', 'bamali', 'garingali', 'gulambali', 'wandaayali', 'widyali', 'yali', 'yurali']),
    ("aa-ri",       3,      "",     "(from)",     []),
    ("i-dyi",       2,      "",     "(from)",     []),
    ("ny-dyi",      3,      "",     "(from)",     []),
    ("n-dhi",       2,      "g",    "(from)",     []),
    ("u-dyi",       2,      "",     "(from)",     []),

    # locative
    ("aa-dha",      3,      "y",    "(at/near/in)",     []),
    ("a-dha",       2,      "",     "(at/near/in)",     combine(stem_ay,'dha')),
    ("a-dha",       2,      "y",    "(at/near/in)",     []),
    ("r-ra",        2,      "",     "(at/near/in)",     combine(stem_rr,'ra') + ['bubadyarra', 'dhandarra', 'ganhawaadharra', 'garra', 'gidharra', 'marra', 'murun_garra', 'ngarra'] + ['bannawirra', 'birra', 'birra', 'birrabirra', 'gadhawirra', 'gadhawirra', 'girragirra', 'mirra', 'mirralbirra', 'ngandabirra']),
    ("r-ra",        2,      "r",    "(at/near/in)",     ['bubadyarra', 'dhandarra', 'ganhawaadharra', 'garra', 'gidharra', 'marra', 'murun_garra', 'ngarra'] + ['bannawirra', 'birra', 'birra', 'birrabirra', 'gadhawirra', 'gadhawirra', 'girragirra', 'mirra', 'mirralbirra', 'ngandabirra']),
    ("n-dha",       2,      "",     "(at/near/in)",     []),
    ("-la",         1,      "l",    "(at/near/in)",     ["-bula","gila"] + ['gunggula','dhala', 'gawala', 'gundala', 'marrala', 'yarruwala']),
    ("aa-ra",       3,      "",     "(at/near/in)",     []),
    ("i-dya",       2,      "",     "(at/near/in)",     []),
    ("ny-dya",      3,      "",     "(at/near/in)",     []),
    ("ng-ga",       3,      "",     "(at/near/in)",     []),
    ("u-dya",       2,      "",     "(at/near/in)",     []),
    # ergative
    ("aa-dhu",      3,      "y",    "(doer)",           []),
    ("a-dhu",       2,      "",     "(doer)",           combine(stem_ay,'dhu')),
    ("a-dhu",       2,      "y",    "(doer)",           []),
    ("r-ru",        2,      "",     "(doer)",           combine(stem_rr,'ru')),
    ("r-ru",        2,      "r",    "(doer)",           []),
    ("n-dhu",       2,      "",     "(doer)",           ['nhindhu']),
    ("-lu",         1,      "l",    "(doer)",           []),
    ("aa-ru",       3,      "",     "(doer)",           []),
    ("i-dyu",       2,      "",     "(doer)",           []),
    ("ny-dyu",      3,      "",     "(doer)",           []),
    ("ng-gu",       3,      "",     "(doer)",           []),
    ("u-dyu",       2,      "",     "(doer)",           []),
    ]

quantifiers_and_numbers = [ # nb: presently conflicts with pronouns
    ("bula-ngunbaay",       1,  "", "three",            []),
    ("-ngunbay",            1,  "", "one/single",       []),
    ("-bula",               1,  "", "two/pair",         ["bungubulabula","galgambula","gulambula"]),
    ("-bunggu",             1,  "", "four or more",     []),
    ("-bung",             1,  "", "many",     ["marambungiiy","nanhaybungarra"]),
    ("-girbang",            1,  "", "several",          ["balaagangirbang","balugirbang"]),
     ("-gir",    1,  "", "all",             []),
    ("-ngunbaaymarrang",    1,  "", "some",             []),
    ("-ngunbaayngunbaay",   1,  "", "a few",            []),
    ("-galang",             1,  "", "many",             ["winhangalang","ngunhangalang","magalang"]),
    ("-bunggubunggu",       1,  "", "very many",        []),
    ]
    
verb_sense_patterns = [
    # Subject
    ("-ndhu",      2,      "",    "you",           ['nhindhu']),
    ("-dhu",      2,      "",    "I",           ['nhadhu']),
    ("-nhiin",      2,      "",    "he/she/it",           []),
   
    # object
    ("-nhal",      2,      "",    "to me",           ['nganhal']),
    ("-nyal",      2,      "",    "to you",           ['nginyal']),
    ("-ngin",      2,      "",    "to him/her/it",           []),
    
    # genitive
     ("-dhi",      2,      "",    "mine",           ['ngadhi']),
     ("-nhu",      2,      "",    "your",           []),
     #("-la",      2,      "",    "his/her/its",           []),
    # present tense
    ("a-nha",       2,      "",     "do/does",          []),
    ("u-nha",       2,      "",     "do/does",             []),
    ("i-nya",       2,      "",     "do/does",             []),
    ("a-rra",       2,      "",     "do/does",             combine(stem_rr,'ra') + ['bubadyarra', 'dhandarra', 'ganhawaadharra', 'garra', 'gidharra', 'marra', 'murun_garra', 'ngarra']),
    ("i-rra",       2,      "",     "do/does",             combine(stem_rr,'ra') + ['bannawirra', 'birra', 'birra', 'birrabirra', 'gadhawirra', 'gadhawirra', 'girragirra', 'mirra', 'mirralbirra', 'ngandabirra']),

    # simple past tense
    ("a-nhi",       2,      "",     "did",              []),
    ("u-nhi",       2,      "",     "did",              []),
    ("i-nyi",       2,      "",     "did",              []),
    ("a-yi",        2,      "",     "did",              []),
    ("i-yi",        2,      "",     "did",              []),

    # future tense
    ("a-girri",     2,      "",     "will",             []),
    ("u-nggirri",   2,      "",     "will",             []),
    ("i-girri",     2,      "",     "will",             []),
    ("a-lgirri",    2,      "",     "will",             []),
    ("i-lgirri",    2,      "",     "will",             []),

    # infinitive
    ("a-gi",        2,      "",     "to",               []),
    ("u-ngi",       2,      "",     "to",               []),
    ("i-gi",        2,      "",     "to",               []),
    ("a-li",        2,      "",     "to",               ['bali', 'bamali', 'garingali', 'gulambali', 'wandaayali', 'widyali', 'yali', 'yurali']),
    ("i-li",        2,      "",     "to",               []),

    # imperative
    ("a-dha",       2,      "",     "do!",              []),
    ("u-nga",       2,      "",     "do!",              []),
    ("i-gya",       2,      "",     "do!",              []),
    ("a-la",        2,      "",     "do!",              ['dhala', 'gawala', 'gundala', 'marrala', 'yarruwala']),
    ("i-ya",        2,      "",     "do!",              [])
    ]
    

class AboriginalLanguageStemmer(StemmerI):
    """
    AboriginalLanguage Stemmer
    """
    
    def reduce_word(self, word, show_translation=False, show_pos=True):
        "word = word.lower()"
        morphemes = []

        # check for "bu" conjunction
        if word.endswith('bu'):
            reduction = self.apply_reduction(word, conjunctions, show_translation, show_pos)
            word = reduction[0]
            morphemes = reduction[1:] + morphemes

        # verb sense reduction
        old_word = word
        reduction = self.apply_reduction(word, verb_sense_patterns, show_translation)

        word = reduction[0]
        morphemes = reduction[1:] + morphemes
        if word != old_word:

            return (word, morphemes) # end if it was a verb

  
        # case reduction (nouns and adjectives)
        reduction = self.apply_reduction(word, noun_and_adj_cases, show_translation, show_pos)
        word = reduction[0]
        morphemes = reduction[1:] + morphemes

        # quantifier and number reduction
        reduction = self.apply_reduction(word, quantifiers_and_numbers, show_translation, show_pos)
        word = reduction[0]
        morphemes = reduction[1:] + morphemes

        return (word, morphemes)

    def apply_reduction(self, word, rules, show_translation=False, show_pos=True):

        if show_translation:
            morpheme = ()
        else:
            morpheme = []
        for rule in rules:
            suffix = rule[0].split("-")[-1]
            ending = rule[0].replace("-","")
            suffix_length = len(suffix)
            ending_length = len(ending)
            if word.endswith(ending):
                if len(word) - rule[1] >= suffix_length:                     
                    if self.not_in_exceptions(word, rule[4]):
                        word = word[:-suffix_length] + rule[2]
                        if show_translation:
                            translation = rule[3]
                            morpheme = (suffix, translation)
                        else:
                            morpheme = [suffix]
                        break
        if show_translation:
            
            if morpheme == ():
                return [word]
            else:
                return [word, morpheme]
        else:
            return [word] + morpheme

    def not_in_exceptions(self, word, exceptions):
        for exception in exceptions:
            if exception.startswith("-"):
                if word.endswith(exception[1:]):
                    return False
            if word == exception:
                return False
        return True

    def stem(self, word, hide_suffixes=True, show_translation=False, show_pos=True):
        
        if hide_suffixes == True:
            return self.reduce_word(word, False, show_pos)[0]
        else:
            return self.reduce_word(word, show_translation, show_pos) 
    
    #def stem(self, word):
    #    return self.reduce_word(word)[0]
    
class PhoneticStemmer(StemmerI):
    """
    Phonetic Stemmer
    """
    
    def reduce_word(self, word, show_translation=False):
        "word = word.lower()"
        morphemes = []

        # check for "bu" conjunction et al
        if word.endswith('bu'):
            reduction = self.apply_reduction(word, conjunctions, show_translation)
            word = reduction[0]
            morphemes = reduction[1:] + morphemes

        # verb sense reduction
        old_word = word
        reduction = self.apply_reduction(word, verb_sense_patterns, show_translation)
        word = reduction[0]
        morphemes = reduction[1:] + morphemes
        if word != old_word:
            return (word, morphemes) # end if it was a verb

        # case reduction (nouns and adjectives)
        reduction = self.apply_reduction(word, noun_and_adj_cases, show_translation)
        word = reduction[0]
        morphemes = reduction[1:] + morphemes

        # quantifier and number reduction
        reduction = self.apply_reduction(word, quantifiers_and_numbers, show_translation)
        word = reduction[0]
        morphemes = reduction[1:] + morphemes

        return (word, morphemes)

    def apply_reduction(self, word, rules, show_translation=False):
        if show_translation:
            morpheme = ()
        else:
            morpheme = []
        for rule in rules:
            suffix = rule[0].split("-")[-1]
            ending = rule[0].replace("-","")
            suffix_length = len(suffix)
            ending_length = len(ending)
            if word.endswith(ending):
                if len(word) - rule[1] >= suffix_length:                     
                    if self.not_in_exceptions(word, rule[4]):
                        word = word[:-suffix_length] + rule[2]
                        if show_translation:
                            translation = rule[3]
                            morpheme = (suffix, translation)
                        else:
                            morpheme = [suffix]
                        break
        if show_translation:
            if morpheme == ():
                return [word]
            else:
                return [word, morpheme]
        else:
            return [word] + morpheme

    def not_in_exceptions(self, word, exceptions):
        for exception in exceptions:
            if exception.startswith("-"):
                if word.endswith(exception[1:]):
                    return False
            if word == exception:
                return False
        return True

    def stem(self, word, hide_suffixes=True, show_translation=False):
        if hide_suffixes == True:
            return self.reduce_word(word)[0]
        else:
            return self.reduce_word(word, show_translation) 
    
    def stem(self, word):
        return self.reduce_word(word)[0]
    
