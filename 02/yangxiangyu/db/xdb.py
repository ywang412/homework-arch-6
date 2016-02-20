#!/bin/bash/env python

import struct
import os

class LogFile:
    def __init__(self, name, mode):
        if mode == 'r':
            self.f = open(name)
        elif mode == "w":
            self.f = open(name, "a")
        else:
            raise Exception("bad mode")

    def name(self):
        return self.name

    def append(self, k, v):
        klen = len(k)
        vlen = len(v)
        print(klen,vlen)
        #header = struct.pack("<II", klen, vlen)
        header = '%010d%010d'%(klen, vlen)
        pos = self.f.tell()
        self.f.write(header)
        self.f.write(k)
        self.f.write(v)
        self.f.flush()
        return pos

    def read(self, pos):
        self.f.seek(pos)
        #s = self.f.read(8)
        #klen, vlen, = struct.unpack("<II", s)
        klen = int(self.f.read(10))
        vlen = int(self.f.read(10))
        print(klen,vlen)
        self.f.seek(pos + 20 + klen)
        v = self.f.read(vlen)
        print(v)
        return v

    def size(self):
        return os.path.getsize(self.f.name)

    def scan(self):
        self.f.seek(0)
        pos = self.f.tell()
        head = self.f.read(20)
        while len(head) > 0:
            klen = int(head[:10])
            vlen = int(head[10:])
            print(klen,vlen)
            #klen, vlen= struct.unpack("<II", head)
            k = self.f.read(klen)
            v = self.f.read(vlen)
            yield pos, k, v
            pos = self.f.tell()
            head = self.f.read(20)

    def close(self):
        self.f.close()

    def flush(self,d):
        with  open("tmp.db", "w") as f_tmp:
            for k in d:
                v = d[k]
                pos = f_tmp.tell()
                klen = len(k)
                vlen = len(v)
                print(klen,vlen)
                header = '%010d%010d'%(klen, vlen)
                f_tmp.write(header)
                f_tmp.write(k)
                f_tmp.write(v)
                f_tmp.flush()
        self.f.close()
        os.remove(self.f.name)
        os.rename("tmp.db",self.f.name)
        print(self.f.name)
        self.f = open(self.f.name,"a")
        print(self.f.name)

class IndexRecord:
    def __init__(self, pos):
        self.pos = pos

class DB:
    def __init__(self, name):
        self.index = {}
        self.name = name
        self.wlog = LogFile(name, "w")
        self.rlog = LogFile(name, "r")
        self._loadIndex()

    def _loadIndex(self):
        for pos, k, v in self.rlog.scan():
            self.index[k] = IndexRecord(pos)

    def set(self, k, v):
        pos = self.wlog.append(k, v)
        self.index[k] = IndexRecord(pos)

    def get(self, k):
        rec = self.index.get(k, None)
        if rec:
            return self.rlog.read(rec.pos)
        else:
            return None

    def close(self):
        self.wlog.close()
        self.rlog.close()

    def gc(self):
        d = {}
        for k in self.index:
            rec = self.index.get(k,None)
            v = self.rlog.read(rec.pos)
            d[k]=v
        self.wlog.flush(d)
        self.index = {}
        self.wlog = LogFile(self.name, "w")
        self.rlog = LogFile(self.name, "r")
        self._loadIndex()
