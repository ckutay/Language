#localhost
#plugin_gmap.key='ABQIAAAAJ1CDsdbAKA65HnQ7t-2vdRQrZ3hpGx_7_TccLF7cx3k6pplgxxRZphrXQKKc-TcWtjZQjr9qylR4Mg' # key for localhost
#irca.teachingforchange
#plugin_gmap.key='ABQIAAAAJ1CDsdbAKA65HnQ7t-2vdRQf2HeO-pUFbIIYBlsdpaxARL3FsBS12UImKWkvGiDS8--IvsfQz_FOfQ' 
#top site
#GOOGLEMAP_KEY="ABQIAAAAJ1CDsdbAKA65HnQ7t-2vdRRUlOG9qJIroEAuogNlnP0txuwBIxTAoO4gRd_PMTBEPfs5dKlOnSWD7Q" 
#http:////IRCA
#GOOGLEMAP_KEY="ABQIAAAAJ1CDsdbAKA65HnQ7t-2vdRS-GPBnv52JkKUK0SCCrtSFoJJm-hRrFQL1aIB43unCdRXpm_ar8boZMQ"
#for http://
GOOGLEMAP_KEY="ABQIAAAAgmnPur4uFr3tfb2KjkqXHxRUlOG9qJIroEAuogNlnP0txuwBIxQxpGXF06NPhGKQ0uBcy_OLlgghdA"

#try:
#    import google    
#    GOOGLEMAP_KEY="ABQIAAAAJ1CDsdbAKA65HnQ7t-2vdRTVLgfiuU3D6RXQ0Cu_n5ehkLpQWxQ0LQ6UZCV_ZwMgxhGZyIXPBvwjDg"
#except: pass

EMAIL_SERVER='129.94.172.253'
EMAIL_SENDER='ckutay@cities.org.au'
EMAIL_AUTH=False

RECAPTCHA_PUBLIC_KEY='6LefJwQAAAAAAEuj02bmS2LgiZiPhGBqKP1kbn26'
RECAPTCHA_PRIVATE_KEY='6LefJwQAAAAAAPcK2G6SO_pyJDegHi58J41bEVrV'

from gluon.validators import Validator

class SlugValidator(Validator):
    def __call__(self, value):
        return (value.replace(' ', '_'), None)
