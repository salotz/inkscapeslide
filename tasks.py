from invoke import task
import sys

DEV_ENV = 'inkscapeslide-dev'
PYTHON_VERSION = '3.7'



@task
def env_dev(ctx):
    """Recreate from scratch the wepy development environment."""

    ctx.run(f"conda create -y -n {DEV_ENV} python={PYTHON_VERSION}",
        pty=True)

    # install package
    ctx.run(f"$ANACONDA_DIR/envs/{DEV_ENV}/bin/pip install -e .")

    # install the dev dependencies
    ctx.run(f"$ANACONDA_DIR/envs/{DEV_ENV}/bin/pip install -r requirements_dev.txt")
