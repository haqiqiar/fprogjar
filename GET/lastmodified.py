import os.path, time

print "last modified: %s" % time.ctime(os.path.getmtime('cobastatus.py'))
print "created: %s" % time.ctime(os.path.getctime('cobastatus.py'))
