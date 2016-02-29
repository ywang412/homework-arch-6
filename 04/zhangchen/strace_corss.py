#!/usr/bin/env python
#coding:utf-8



import sys,os,linecache,time
def trace(f):
  def globaltrace(frame, why, arg):
    if why == "call": return localtrace
    return None
  def localtrace(frame, why, arg):
    if why == "line":
      # record the file name and line number of every trace 
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      bname = os.path.basename(filename)
      print "{}({}): {}".format(  bname,
                    lineno,
                    linecache.getline(filename, lineno)),
    return localtrace
  def _f(*args, **kwds):
    sys.settrace(globaltrace)
    result = f(*args, **kwds)
    sys.settrace(None)
    return result
  return _f



if __name__ == '__main__':
    @trace
    def test():
        print time.time()
        print time.sleep(2)
        print time.time()
    
    test()
