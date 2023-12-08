import urllib, urllib.request

url = 'http://arxiv.org/rss/cs.IR'
data = urllib.request.urlopen(url)
print(data.read().decode('utf-8'))
