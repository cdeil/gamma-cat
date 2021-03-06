#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Make catalog (multiple steps available)
"""
import logging
import warnings
import click
import gammacat

log = logging.getLogger(__name__)


@click.group()
@click.option('--loglevel', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']))
@click.option('--show-warnings', is_flag=True,
              help='Show warnings?')
def cli(loglevel, show_warnings):
    """
    Make catalog (multiple steps available)
    """
    levels = dict(
        debug=logging.DEBUG,
        info=logging.INFO,
        warning=logging.WARNING,
        error=logging.ERROR,
        critical=logging.CRITICAL,
    )
    logging.basicConfig(level=levels[loglevel])
    log.setLevel(level=levels[loglevel])

    if not show_warnings:
        warnings.simplefilter('ignore')


@cli.command(name='output')
def make_output():
    """Re-generate files in `output`.
    """
    log.info('Re-generate files in `output` ...')
    gammacat.OutputDataMaker().make_all()


@cli.command(name='cat')
def make_cat():
    """Make catalog in HGPS format
    """
    log.info('Making catalog ...')
    gammacat.GammaCatMaker().run()


# @cli.command(name='webpage')
# def make_webpage():
#     """Re-generate webpage in `docs`.
#     """
#     log.info('Re-generate webpage in `docs` ...')
#     gammacat.webpage.make()


@cli.command(name='all')
@click.pass_context
def make_all(ctx):
    """Run all steps.
    """
    log.info('Run all steps ...')
    ctx.invoke(make_check)
    ctx.invoke(make_output)
    ctx.invoke(make_cat)
    # ctx.invoke(make_webpage)


@cli.command(name='check')
def make_check():
    """Run automated tests
    """
    log.info('Run automated checks ...')
    gammacat.checks.check_input_files()


@cli.command(name='web')
def serve_webpage():
    """Serve gamma-cat webpage locally.

    This is equivalent to:

        cd docs && python -m http.server
    """
    # import subprocess
    # import webbrowser
    # from http.server import HTTPServer, SimpleHTTPRequestHandler
    # server_address = ('localhost', 8000)
    # httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # httpd.serve_forever()
    # subprocess.Popen('cd docs && python -m http.server', shell=True)
    # webbrowser.open('http://localhost:8000/docs')
    # click.pause('asdf')

    print('\nTo serve the gamma-cat webpage locally use these commands:\n')
    print('  cd docs && python -m http.server && cd ..')
    print('  open http://localhost:8000\n')


if __name__ == '__main__':
    cli()
