import sys
from .init import fs2, click, errors
from fs.path import relpath, normpath

@fs2.command()
@click.argument('paths', nargs=-1)
@click.option('--force', '-f', is_flag=True, help='force skip if instead of aborting')
@click.pass_context
def cat(ctx, paths, force):
    fs = ctx.obj['fs']
    for path in paths:
        path = relpath(normpath(path))
        try:
            result = fs.readbytes(path)
        except errors.FileExpected:
            if not force:
                click.confirm('Error: %s/ is a dir. Skip?' % path, abort=True, default=True)
        except errors.ResourceNotFound:
            if not force:
                click.confirm('Error: %s is not exist. Skip?' % path, abort=True, default=True)
        else:
            click.echo(result.decode(sys.getdefaultencoding(), 'replace'))

