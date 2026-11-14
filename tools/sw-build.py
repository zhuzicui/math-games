#!/usr/bin/env python3
"""Rewrite the generated block of sw.js: the list of files to keep offline, the build stamp, and a version
that changes whenever any of those files changes. Run by tools/stamp.sh; safe to run on its own."""
import hashlib, os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(root)

SKIP_DIRS = {'.git', 'docs', 'tools', 'node_modules', '.vercel'}
SKIP_FILES = {'sw.js', 'README.md', 'vercel.json', 'write-test.html', 'og-image.png', '.gitignore', '.DS_Store',
              'icon-1024.png'}
EXTS = {'.html', '.js', '.json', '.webmanifest', '.png', '.jpg', '.svg', '.woff2', '.ico', '.mp3', '.m4a', '.wav', '.ogg'}

files = []
for d, dirs, names in os.walk('.'):
    dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
    for n in sorted(names):
        if n in SKIP_FILES or os.path.splitext(n)[1].lower() not in EXTS:
            continue
        files.append(os.path.relpath(os.path.join(d, n), '.').replace(os.sep, '/'))
files.sort()

h = hashlib.sha256()
for f in files:
    h.update(f.encode()); h.update(b'\0')
    h.update(open(f, 'rb').read()); h.update(b'\0')
version = h.hexdigest()[:12]

m = re.search(r'<meta name="build" content="([^"]+)"', open('index.html', encoding='utf-8').read())
build = m.group(1) if m else ''

urls = ['./'] + [f for f in files]          # './' = the start page, stored under the address people open
block = ("/*GEN-START*/\nvar VERSION = '%s';\nvar BUILD = '%s';\nvar ASSETS = %s;\n/*GEN-END*/"
         % (version, build, '[\n  ' + ',\n  '.join("'%s'" % u for u in urls) + '\n]'))
src = open('sw.js', encoding='utf-8').read()
new = re.sub(r'/\*GEN-START\*/.*?/\*GEN-END\*/', lambda _: block, src, flags=re.S)
if new != src:
    open('sw.js', 'w', encoding='utf-8').write(new)
print('sw %s: %d files' % (version, len(urls)))
