def readfile(dirc):
    blocked=['']
    redirected={}
    try:
        f=open(dirc, 'rb')
        if dirc in blocked:
            f=open('page/403.html', 'rb')
            status=403
        else:
            status=200
    except IOError:
        if os.path.isdir(dirc):
            f=open('page/301.html', 'rb')
            status=301
        else:
            f=open('page/404.html', 'rb')
            status=404
    return status, f