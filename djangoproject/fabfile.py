import os
import datetime
from importlib import import_module
import subprocess

from fabric.api import *
from fabric.context_managers import path
from fabric.contrib import files, console, django
from fabric import utils
from fabric.decorators import hosts

if "VIRTUAL_ENV" not in os.environ:
    raise Exception("$VIRTUAL_ENV not found.")

def _setup_path(name):
    import sys
    sys.path.insert(0, '.')
    settings = import_module('%s.settings_%s' % (env.project_python, name))
    env.django_settings = settings
    env.environment = name
    for key, value in settings.DEPLOYMENT.items():
        setattr(env, key, value)

    env.project_root = os.path.join(env.root, env.project)
    env.code_root = os.path.join(env.project_root, env.project_python)
    env.virtualenv_root = os.path.join(env.project_root, 'env')
    env.settings = '%(project)s.settings_%(environment)s' % env

def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    #run('mkdir -p %s' % os.path.join(env.root, 'log'))
    git_clone()
    git_checkout_branch()
    create_virtualenv()
    create_library_symlinks()
    update_requirements()
    create_symlinks()


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--setuptools'
    run('virtualenv %s %s' % (args, env.virtualenv_root))


def git_pull():
    "Updates the repository."
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.code_root):
        run("git pull")


def git_clone():
    "Updates the repository."
    require('root', provided_by=('staging', 'production'))
    with cd(env.root):
        run("git clone %s %s" % (env.git_repository, env.project))


def git_checkout_branch():
    "Checks out the correct branch."
    require('root', provided_by=('staging', 'production'))
    if env.git_branch != 'master':
        with cd(env.project_root):
            run('git checkout %s' % (env.git_branch,))


def git_reset():
    "Resets the repository to specified version."
    run("cd ~/git/$(repo)/; git reset --hard $(hash)")


def deploy():
    """ updates code base on remote host and restarts server process """
    if not env.is_stage:
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    git_pull()
    touch()


def deployfull():
    """ updates code base on remote host and restarts server process """
    if not env.is_stage:
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    git_pull()
    migrate()
    collectstatic()
    touch()


def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('pip install --requirement REQUIREMENTS_SERVER')


def manage(command):
    """runs manage.py <command> on the remote host"""
    require('code_root', provided_by=('staging', 'production'))
    manage = os.path.join(env.project_root, 'manage.py')
    with cd(env.project_root):
        run('./env/bin/python %s %s' % (manage, command))


def syncdb():
    """runs syncdb on the remote host"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./manage.py syncdb --noinput')


def createsu():
    """create superuser with sso credentials on the remote host"""
    create_allink_user()


def create_allink_user():
    """loads the allink_user.json fixture"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./manage.py loaddata allink_user.json')


def migrate():
    """migrates all apps on the remote host"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./manage.py migrate')


def compilemessages():
    """compiles all translations"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./manage.py compilemessages')


def create_symlinks():
    """ create settings feincms and admin media links"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        run('mkdir static/')
    with cd(env.code_root):
        run('ln -sf settings_%s.py settings.py' % env.environment)


def touch():
    """ touch wsgi file to trigger reload """
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        run('touch apache.wsgi')


def collectstatic():
    """runs collectstatic on the remote host"""
    require('code_root', provided_by=('staging', 'production'))
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./manage.py collectstatic --noinput')


def reset_local_database():
    """ resets the local database to the database on the server """
    require('code_root', provided_by=('staging', 'production'))
    if not console.confirm('Are you sure you want to replace the local database with the %s database data?'
                           % env.environment, default=False):
        utils.abort('Reset local database aborted.')
    filename = "tmp_dump%d_%d_%d.json" % datetime.datetime.now().isocalendar()
    require('code_root', provided_by=('staging', 'production'))
    server_manage = os.path.join(env.project_root, 'manage.py')
    server_data = os.path.join(env.project_root, filename)
    local_manage = os.path.join(os.path.dirname(__file__), 'manage.py')
    local_data = os.path.join(os.path.dirname(__file__), filename)
    with cd(env.project_root):
        with prefix('source env/bin/activate'):
            run('./env/bin/python %s dumpdata > %s' % (server_manage, server_data,))
        get(server_data, local_data)
        run('rm %s' % server_data)
    with lcd(os.path.dirname(__file__)):
        local('%s sqlflush | %s dbshell' % (local_manage, local_manage))
        local('%s loaddata %s' % (local_manage, local_data,))
        local('rm %s' % local_data)


def reset_local_media():
    """ Reset local media from remote host """
    require('root', provided_by=('staging', 'production'))
    if not console.confirm('Are you sure you want to replace the local media with the %s media data?'
                           % env.environment, default=False):
        utils.abort('Reset local media aborted.')
    remote_media = os.path.join(env.project_root, 'media',)
    local_media = os.path.join(os.path.dirname(__file__), 'media')
    local('rsync --delete --exclude=".gitignore" -rvaz %s@%s:%s/ %s' % (env.user, env.hosts[0], remote_media, local_media))


def restart_celery():
    """restarts the celery worker"""
    require('root', provided_by=('staging', 'production'))
    run('nine-supervisorctl restart %s' % env.celery_worker)


def create_local_symlinks():
    """creates the local symlinks to settings files and pre-commit hook"""
    if not os.path.isdir("media"):
        os.mkdir("media")
    if not os.path.islink("%s/settings.py" % env.project_python) and os.path.isfile("%s/settings_development.py" % env.project_python):
        os.symlink("settings_development.py", "%s/settings.py" % env.project_python)
    if not os.path.isfile(".git/hooks/pre-commit"):
        os.symlink("../../pre-commit", ".git/hooks/pre-commit")


def create_library_symlinks():
    """used on ubuntu servers to compile pil"""
    require('root', provided_by='production')
    with cd(env.project_root):
        for library in ('libfreetype.so', 'libjpeg.so', 'libz.so'):
            run("ln -s /usr/lib/`uname -i`-linux-gnu/%s env/lib/" % library)


def create_rabbitmq_vhost():
    """create a rabbitmq vhost and user"""
    require('root', provided_by='production')
    run('sudo rabbitmqctl add_user %(rabbitmq_username)s %(rabbitmq_password)s' % env.django_settings.DEPLOYMENT)
    run('sudo rabbitmqctl add_vhost %(rabbitmq_vhost)s' % env.django_settings.DEPLOYMENT)
    run('sudo rabbitmqctl set_permissions -p %(rabbitmq_vhost)s %(rabbitmq_username)s ".*" ".*" ".*"' % env.django_settings.DEPLOYMENT)


def update_local_requirements():
    """installs local requirements"""
    subprocess.call(["pip", "install", "--requirement", "REQUIREMENTS_LOCAL"])


def freeze_requirements():
    with open("REQUIREMENTS") as file:
        for line in file:
            if line.lower().startswith('-e') or line.lower().startswith('http'):
                os.system("echo '" + line.rstrip() + "' >> REQUIREMENTS_frozen")
            else:
                pkg = line.rstrip().split('==')[0]
                os.system("pip freeze | grep -i ^" + pkg + "== >> REQUIREMENTS_frozen")
    os.system("mv REQUIREMENTS_frozen REQUIREMENTS")


def production():
    env.project_python = 'myapp'
    _setup_path('production')

