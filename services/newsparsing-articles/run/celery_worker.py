'''
Created on 7 janv. 2018

@author: tuco
'''
import argparse
import os

from celery.bin.worker import worker
from api.newsparsing.articles.celery_app import celery

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(
        description='Launch newsparsing-articles celery worker.'
    )
    parser.add_argument('-a',
                        '--application-config',
                        dest='articles_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/application.conf"),
                        help='newsparsing-articles configuration')
    parser.add_argument('-f',
                        '--flask-config',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/flask.conf"),
                        help='newsparsing-articles flask configuration')
    parser.add_argument('-c',
                        '--celery-config',
                        dest='celery_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/celery.conf"),
                        help='newsparsing-articles celery configuration')
    args = parser.parse_args()

    # Build worker
    celery_worker = worker(app=celery)
    # Start worker
    celery_worker.run(**{
        '--application-config': args.articles_configuration,
        '--flask-config': args.flask_configuration,
        '--celery-config': args.celery_configuration,
    })
