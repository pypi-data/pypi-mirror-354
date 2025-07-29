import pathlib
import click
from click_default_group import DefaultGroup
from .crypt import enigma

#from hakisto.click import hakisto_severity, hakisto_file

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
# @hakisto_severity()
# @hakisto_inline_location()
# @hakisto_short_trace()
@click.pass_context
def main(ctx, **kwargs):
    """Crypt utilities"""
    # hakisto_process_all(**kwargs)
    ctx.ensure_object(dict)


@main.group(
    cls=DefaultGroup,
    default="store",
    default_if_no_args=True,
)
@click.option("-f", "--file", type=click.Path(dir_okay=False, path_type=pathlib.Path), prompt=True)
@click.pass_context
def secret(ctx, file):
    """Locally stored secret"""
    ctx.obj["file"] = file


@secret.command()
@click.argument("phrase")
@click.pass_context
def store(ctx, phrase):
    """Store secret PHRASE"""
    with ctx.obj["file"].open("wb") as f:
        f.write(enigma(phrase))
