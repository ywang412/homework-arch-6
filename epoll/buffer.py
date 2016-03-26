class Buffer:
    def __init__(self):
        self.buf = ""

    def Len(self):
        return len(self.buf)

    def Append(self, buf):
        self.buf += buf

    def Peek(self, n):
        return self.buf[:n]

    def Buffer(self):
        return self.buf

    def Skip(self, n):
        self.buf = self.buf[n:]

    def Read(self, n):
        b = self.buf[:n]
        self.buf = self.buf[n:]
        return b

    def ReadAll(self):
        return self.Read(self.Len())

    def ReadUtil(self, sub):
        i = self.buf.find(sub)
        if i == -1:
            return ""
        return self.Read(i + 1)

    def Send(self, sock):
        n = sock.send(self.buf)
        if n > 0:
            self.buf = self.buf[n:]
        return n
