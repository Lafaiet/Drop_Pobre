
def as2_utf(s):
    r=""
    for i in s:
        r=r+i.decode("utf-8")

    return r
