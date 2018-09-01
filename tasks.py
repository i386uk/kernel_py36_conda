from __future__ import print_function
from invoke import task, Collection
import os
from subprocess import check_output

from shutil import which
import shutil

env_name = 'kernel_py36_conda'
source = '' if os.name == 'nt' else 'source'


def rmdir(dirname):
    """Safely remove a directory, cross-platform
    """
    if not os.path.exists(dirname):
        return
    if os.name == 'nt':
        check_output('rmdir {0!s} /S /Q'.format(dirname), shell=True)
    else:
        check_output(['rm', '-rf', dirname])


@task
def environment(ctx, clean=False, env_name=env_name):
    '''
    Creates environment for demo
    Args:
    clean: deletes environment prior to reinstallation
    env_name: name of environment to install
    '''
    if clean:
        print('deleting environment')
        ctx.run('{0!s} deactivate; conda remove -n {1!s} --all'.format(source, env_name))
    # Create a new environment
    print('creating environment {0!s}'.format(env_name))
    ctx.run("conda env create -f binder/environment.yml -n {0!s}".format(env_name))

    build(ctx, env_name=env_name)


@task
def build(ctx, env_name=env_name, kernel=True):
    '''
    Builds an environment with appropriate extensions.
    '''
    ctx.run("""
        {0!s} activate {1!s} &&
        jupyter labextension install @jupyterlab/fasta-extension@0.16 --no-build &&
        jupyter labextension install @jupyterlab/geojson-extension@0.16 --no-build &&
        jupyter labextension install @jupyterlab/google-drive@0.12 --no-build &&
        jupyter labextension install @jupyterlab/plotly-extension@0.16 --no-build &&
        jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.35 --no-build &&
        jupyter labextension install bqplot@0.3.6 --no-build &&
        jupyter labextension install jupyter-matplotlib@0.3.0 --no-build &&
        jupyter labextension install jupyterlab_bokeh &&
        jupyter lab clean && jupyter lab build
        """.format(source, env_name).strip().replace('\n', ''))
    if kernel:
        ctx.run("{0!s} activate {1!s} && ipython kernel install --name {1!s} --display-name {1!s} --sys-prefix".format(source, env_name))

# Configure cross-platform settings.
ns = Collection(environment, build)
ns.configure({
    'run': {
        'shell': which('bash') if os.name != 'nt' else which('cmd'),
        'pty': False if os.name == 'nt' else True
    }
})
