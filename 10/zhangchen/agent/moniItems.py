#!/usr/bin/env python
#coding=utf-8
import json
import urllib
import inspect
import os,time,socket
import threading

userDefine_check_time = 0
userDefine_json = []

class mon:
    def __init__(self):
        self.data = {}

    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            #return "%s %s %s" % (a[0],a[1],a[2])
            return   float(a[0])

    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a / 1024

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1]) #Total
                F = int(mem_open.readline().split()[1]) #Free
                B = int(mem_open.readline().split()[1]) #Buffer
                C = int(mem_open.readline().split()[1]) #Cache
                return (T-F-B-C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a / 1024

    def getMemFree(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F+B+C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1])
                return a / 1024

    def getHost(self):
        #return ['host1', 'host2', 'host3', 'host4', 'host5'][int(time.time() * 1000.0) % 5]
        #return socket.gethostname()
        return 'zc'
    def getTime(self):
        return int(time.time())

    def userDefineMon(self):
        """
        5min -> GET webapi 获取自定义监控项列表
            {"url":"脚本url","md5":"43214321","name":'eth_all'}
        -> check md5
            /home/work/agent/mon/user/$name/xxx.tgz
        -> xxx.tgz -> main -> chmod +x -> ./main
        -> output
            eth1:10
            eth2:20
            eth3:32
        -> return
            {"eth1":10,"eth2":20,"eth3":32}

        """
        data = {}
        global userDefine_check_time
        global userDefine_json
        if time.time() - userDefine_check_time > 300 or userDefine_json == []:
            url = 'http://reboot:50004/userdefine_listitem'
            try:
                userDefine_json = json.loads(urllib.urlopen(url).read())
                userDefine_check_time = time.time()
            except:
                userDefine_json = []
                return data
        print userDefine_json
        for j in userDefine_json:
            data_url,md5,name = j['url'],j['md5'],j['name']
            print data_url,md5, name

            data_dir = '/home/work/agent/mon/user/'+name
            os.system('mkdir -p %s' % data_dir)
            print 'cd %s && md5sum xxx.tgz' % (data_dir)
            if md5 in os.popen('cd %s && md5sum xxx.tgz' % (data_dir)).read():
                pass
            else:
                urllib.urlretrieve(data_url, data_dir+'/'+'xxx.tgz')
            os.system('cd %s && tar zxf xxx.tgz' % data_dir)
            os.system('chmod +x %s/main' % data_dir)
            ret = os.popen('%s/main' % data_dir).read()
            for item in ret.split("\n"):
                if not item:
                    continue
                else:
                    key, val = item.split(":")
                    data["UD_"+key] = val
        return data

#    def run(self):
#        for name, fun in inspect.getmembers(self, predicate=inspect.ismethod):
#            if name == "userDefineMon":
#                self.data.update(fun())
#            elif name[:3] == 'get':
#                self.data[name[3:]] = fun()
#        self.data = {}
#        self.data['MemTotal'] = self.getMemTotal()
#        self.data['MemFree'] = self.getMemFree()
#        self.data['MemUsage'] = self.getMemUsage()
#        self.data['LoadAvg'] = self.getLoadAvg()
#        self.data['Host'] = self.getHost()
#        self.data['Time'] = self.getTime()
        #self.data.update(self.userDefineMon())
#        return self.data

class runAllMon(threading.Thread):
    def __init__(self,fun_monitor,fun_name, data, lock):
        super(runAllMon,self).__init__()
        self.fun_monitor = fun_monitor
        self.fun_name = fun_name
        self.mutex = lock
        self.data = data

    def run(self):
        #import pdb;pdb.set_trace()
        print self.name
        if self.fun_name == "userDefineMon":
            mon_data = self.fun_monitor()
            self.mutex.acquire()
            self.data.update(mon_data)
            self.mutex.release()
        elif self.fun_name[:3] == 'get':
            mon_data = self.fun_monitor()
            self.mutex.acquire()
            self.data[self.fun_name[3:]] = mon_data
            self.mutex.release()
def main():
    data = {}
    thread_pool_list = []
    lock = threading.Lock()
    mon_instance = mon()
    for name, fun in inspect.getmembers(mon_instance, predicate=inspect.ismethod):
        print name,fun
        print '#' * 50
        run_mon = runAllMon(fun, name, data, lock)
        thread_pool_list.append(run_mon)
        run_mon.start()
    for i in thread_pool_list:
        i.join()
    print data

if __name__ == "__main__":
    main()
