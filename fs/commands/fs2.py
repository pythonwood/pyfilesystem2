#!/usr/bin/env python

import sys,os,time
import click
from fs import open_fs, errors
from fs.path import relpath, normpath, basename, dirname

@click.group()
@click.option('--url', default='.', help='example e.g. . or file:///tmp or webdav://user:pass@127.0.0.1/webdav/subdir/')
@click.pass_context
def fs2(ctx, url):
    if '://' not in url:
        url = 'file://' + url
    ctx.ensure_object(dict)
    ctx.obj['url'] = url
    ctx.obj['fs'] = open_fs(url)

@fs2.command()
# @click.option('--path', default='.', help='ls <path>')
@click.argument('paths', nargs=-1, required=False) # 不限个数
@click.pass_context
def ls(ctx, paths):
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    print('-------------------- fs %s --------------------' % url)
    paths = paths or ['.']
    for path in paths:
        path = relpath(normpath(path))
        try:
            result = fs.listdir(path)
            print('-------------------- dir %s/ --------------------' % path)
            print('\n'.join(result))
        except errors.DirectoryExpected:
            print('-------------------- file %s --------------------' % path)
            print(path)

@fs2.command()
@click.argument('paths', nargs=-1)
@click.pass_context
def cat(ctx, paths):
    fs = ctx.obj['fs']
    for path in paths:
        path = relpath(normpath(path))
        try:
            print('-------------------- cat %s --------------------' % path)
            result = fs.readbytes(path)
        except errors.FileExpected:
            print('Error: %s/ is a dir' % path, file=sys.stderr)
        else:
            print(result.decode(sys.getdefaultencoding(), 'replace'))

