import redis
import http
import loop
import logging

def main():
    fmt = '%(asctime)-15s %(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    lo = loop.Loop()
    redisServer = redis.RedisServer(lo, ('0.0.0.0', 9000)) 
    httpServer = http.HTTPServer(lo, ('0.0.0.0', 9001)) 
    redisServer.start()
    httpServer.start()
    lo.loop()

if __name__ == '__main__':
    main()
