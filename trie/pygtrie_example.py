import pygtrie as trie
import sys

t = trie.CharTrie()
t['/'] = lambda url: sys.stdout.write('Root handler: %s\n' % url)
t['/foo'] = lambda url: sys.stdout.write('Foo handler: %s\n' % url)
t['/foobar'] = lambda url: sys.stdout.write('FooBar handler: %s\n' % url)
t['/baz'] = lambda url: sys.stdout.write('Baz handler: %s\n' % url)

for url in ('/', '/foo', '/foot', '/foobar', 'invalid', '/foobarbaz', '/ba'):
    key, handler = t.longest_prefix(url)
    if key is not None:
        print(key)
        handler(url)
    else:
        print('Unable to handle', repr(url))
