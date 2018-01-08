'''
Created on 7 janv. 2018

@author: tuco
'''
import argparse
import os

from celery.bin.worker import worker
from api.newsparsing.sourcers.celery_app import celery

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(
        description='Launch newsparsing-sourcers celery worker.'
    )
    parser.add_argument('-a',
                        '--application-config',
                        dest='sourcers_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/application.conf"),
                        help='newsparsing-sourcers configuration')
    parser.add_argument('-f',
                        '--flask-config',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/flask.conf"),
                        help='newsparsing-sourcers flask configuration')
    parser.add_argument('-c',
                        '--celery-config',
                        dest='celery_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/celery.conf"),
                        help='newsparsing-sourcers celery configuration')
    args = parser.parse_args()

    # Build worker
    celery_worker = worker(app=celery)
    # Start worker
    celery_worker.run(**{
        '--application-config': args.sourcers_configuration,
        '--flask-config': args.flask_configuration,
        '--celery-config': args.celery_configuration,
    })
