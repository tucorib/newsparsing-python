'''
Created on 7 janv. 2018

@author: tuco
'''
import types

from celery import Celery, bootsteps
from celery.bin import Option

from api.newsparsing.sourcers.flask_app import create_flask_app, \
    load_flask_configuration
from core.newsparsing.sourcers.core.config.application import load_configuration


def load_celery_configuration(celery_configuration_file=None):
    if not celery_configuration_file is None:
        d = types.ModuleType('config')
        d.__file__ = celery_configuration_file
        try:
            with open(celery_configuration_file, mode='rb') as config_file:
                exec(compile(config_file.read(), celery_configuration_file, 'exec'), d.__dict__)
        except IOError as e:
            raise e
        celery.conf.update(d.__dict__)

        
class CelerySourcersArgs(bootsteps.Step):

    def __init__(self, parent, **options):
        # Sourcers configuration
        if '--application-config' in options:
            load_configuration(options['--application-config'])
        # Sourcers configuration
        if '--flask-config' in options:
            load_flask_configuration(parent.app.flask_app, options['--flask-config'])
        # Sourcers configuration
        if '--celery-config' in options:
            load_celery_configuration(options['--celery-config'])

            
def create_celery_app():
    # Celery app
    celery_app = Celery(__name__)
    # Flask app
    celery_app.flask_app = create_flask_app()
    
    # Worker arguments
    celery_app.user_options['worker'].add(
        Option('--application-config',
               dest='sourcers_configuration',
               default=None,
               help='API sourcers configuration.')
    )
    celery_app.user_options['worker'].add(
        Option('--flask-config',
               dest='flask_configuration',
               default=None,
               help='API flask configuration.')
    )
    celery_app.user_options['worker'].add(
        Option('--celery-config',
               dest='celery_configuration',
               default=None,
               help='API celery configuration.')
    )

    celery_app.steps['worker'].add(CelerySourcersArgs)
    
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with celery_app.flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    
    return celery_app


celery = create_celery_app()
