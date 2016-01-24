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
        s = self.f.read(8)
        #klen, vlen, = struct.unpack("<II", s)
        self.f.seek(pos + 8 + klen)
        v = self.f.read(vlen)
        return v

    def size(self):
        return os.path.getsize(self.f.name)

    def scan(self):
        self.f.seek(0)
        pos = self.f.tell()
        head = self.f.read(8)
        while len(head) > 0:
            klen, vlen= struct.unpack("<II", head)
            k = self.f.read(klen)
            v = self.f.read(vlen)
            yield pos, k, v
            pos = self.f.tell()
            head = self.f.read(8)

    def close(self):
        self.f.close()


class IndexRecord:
    def __init__(self, pos):
        self.pos = pos

class DB:
    def __init__(self, name):
        self.index = {}
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
        
