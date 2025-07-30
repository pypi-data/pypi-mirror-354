import typer
from typing_extensions import Annotated
from . import app


@app.command()
def ppa(dst: Annotated[str, typer.Argument()] = "", path='', src=''):
    from ...file import write_file, read_file, iter_relative_path

    path = path or '/etc/apt/sources.list.d'
    src = src or 'ppa.launchpadcontent.net'
    dst = dst or 'launchpad.proxy.ustclug.org'

    for _, fp in iter_relative_path(path):
        txt = read_file(fp)
        if src in txt:
            write_file(fp, s=txt.replace(src, dst))
