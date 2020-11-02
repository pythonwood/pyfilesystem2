from .init import fs2, click, errors
from fs.path import relpath, normpath

from .words2lines import words2lines

@fs2.command()
@click.argument('paths', nargs=-1, required=False) # 不限个数
@click.pass_context
def ls(ctx, paths):
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    paths = paths or ['.']
    for path in paths:
        _path = path
        path = relpath(normpath(path))
        try:
            names = fs.listdir(path)
            if url.lower().startswith('file://') or url.lower().startswith('osfs://'):
                names.sort(key=lambda x: x.lstrip('.').lstrip('_').lower()) # sort as /bin/ls do
                # names = ['.', '..'] + names       # need not
            if len(paths) > 1:
                print('%s/:' % _path.rstrip('/'))
            print('\n'.join(words2lines(names)))
        except errors.DirectoryExpected:
            print('%s:' % _path.rstrip('/'))
        print()
