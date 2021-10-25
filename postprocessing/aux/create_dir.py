def create_dir(fname):
    '''Create directory with fname in current path'''
    import os
    # get the absolute error in ROM
    path = os.path.join(os.getcwd(), fname)
    isExist = os.path.exists(path)
    if isExist:
        print("The target directory "+fname+" has existed")
        pass
    else:
        os.mkdir(path)
        print("The target directory "+fname+" is created successfully")
