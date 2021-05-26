import calendar
import hashlib
import time

def md5(f):
    hashlib.md5(str(f.filename).encode('utf-8')).hexdigest()
    hash = hashlib.md5(str(f.filename).encode('utf-8'))
    hashname = hash.hexdigest()
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    md5.name = hashname+"-"+str(ts)

    return md5.name
