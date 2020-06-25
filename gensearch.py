def gensearch (byear: int=1950) -> str:
    """return the generation (Boomer, X, Y, etc) of year bday"""
    if byear < 1944:
        return("Silent Generation")
    elif byear < 1964:
        return("Baby Boomer")
    elif byear < 1979:
        return("Generation X")
    elif byear < 1981:
        return("Generation Y")
    elif byear < 1996:
        return("Millenial")
    elif byear < 2015:
        return("Generation Z")
    else:
        return("TBD")
