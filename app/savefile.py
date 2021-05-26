import hashlib


def savefile(f):
    img_key = hashlib.md5(f.read()).hexdigest()
    f.save(f)

