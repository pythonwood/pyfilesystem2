from fs import open_fs, errors
import shutil
import click

FS2_NOEXIST, FS2_ISFILE, FS2_ISDIR = 0, 1, 2

def _listopener():
    from fs.opener  import registry
    openers = set(registry.get_opener(i).__class__ for i in  registry.protocols)
    for opener in openers:
        print(str(opener), 'for', ['%s://' % i for i in opener.protocols])

@click.group(invoke_without_command=True) #https://click.palletsprojects.com/en/7.x/commands/#group-invocation-without-command
@click.option('--listopener', '-l', is_flag=True, help='list supported file system')
@click.option('--url', '-u', default='.', help='filesystem url: default is ".", eg. file:///tmp or webdav://user:pass@127.0.0.1/webdav/subdir/')
@click.pass_context
def fs2(ctx, listopener, url):
    # print(vars(ctx), listopener, url)
    if listopener:
        _listopener()
        return
    if not (ctx.args or ctx.invoked_subcommand):
        click.echo(ctx.get_help())
    if '://' not in url:
        url = 'file://' + url
    ctx.ensure_object(dict)
    ctx.obj['url'] = url
    ctx.obj['fs'] = open_fs(url)
