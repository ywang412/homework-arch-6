import urllib
import re
import pybloomfilter
import urlparse

class spider:
    def __init__(self, startURL):
        self.startURL = startURL
        self.targetNetloc = urlparse.urlparse(startURL).netloc
        self.downloadList = []
        self.lurl = []
        self.bloomfilter = pybloomfilter.BloomFilter(100000, 0.1, '/tmp/words.bloom')
        self.dep = 0

    def download(self,url):
        #filename = url.split('/')[-1]
        #urllib.urlretrieve(url,filename)
        print(url)
        self.bloomfilter.update(url)

    def getNext(self,url):
        print(url+'________________ing')
        result = urllib.urlopen(url)
        html = result.read()
        pattern = re.compile(r'<a.*?href="(?!#|mailto|location.|javascript|.*css|.*this\.)(.*?)".*?>.*?<\/a>')
        next = re.findall(pattern, html)
        for path in next:
            if path in self.bloomfilter:
                print("skiping ____",path)
                next.remove(path)
        print(next)
        return next

    def decorateURL(self,lurl):
        l = []
        for url in lurl:
            urlinfo = urlparse.urlparse(url)
            if urlinfo.netloc == "":
                url = urlparse.urljoin(self.startURL,url)
            l.append(url)
        return l


    def depthWalk(self, depth):
        if depth < 1:
            raise 'error'
        if self.dep == 1:
            self.getNext(self.startURL)
            self.lurl = self.getNext(self.startURL)
        if self.dep < depth:
            print(self.dep)
            self.dep = self.dep +1
            for url in self.lurl:
                lurl = self.getNext(url)
                self.lurl.extend(lurl)
                self.download(url)
            self.lurl = list(set(self.lurl))
            self.depthWalk(depth)
            print(self.lurl)
        else:
            print("done")


if __name__ == '__main__':
    s = spider("http://www.qq.com/")
    s.depthWalk(2)
