class State:
    def __init__(self):
        self.length = 0
        self.done = False
        self.data = []

def readBulk(b):
    s = b.Buffer()
    i = s.find('\n')
    if i == -1:
        return None

    length = int(s[1:i-1])
    headerlen = i + 1
    bodylen = length + 2
    if b.Len() < headerlen + bodylen:
        return None

    b.Skip(headerlen)
    s = b.Read(bodylen)
    return s[:-2]

def readMessage(b, stat):
    if b.Len() == 0:
         return stat

    if stat.length == 0:
        s = b.Buffer()
        i = s.find('\n')
        if i == -1:
            return stat

        s1 = b.ReadUtil('\n')
        length = int(s1[1:i-1])
        stat.length = length

    while True:
        elem = readBulk(b)
        if not elem:
            break
        stat.data.append(elem)
        if len(stat.data) == stat.length:
            stat.done = True
            break

    return stat

def writeMessage(s):
    if not s:
        return '$-1\r\n'
    return '+%s\r\n'%(s)
