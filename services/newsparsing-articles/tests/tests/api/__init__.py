import datetime
import os

from api.newsparsing.articles.flask_app import create_flask_app, \
    load_flask_configuration
from tests import CONFIG_DIR
from tests.core import ArticlesTestCase


class FlaskTestCase(ArticlesTestCase):

    FLASK_CONFIGURATION_FILE = os.path.join(CONFIG_DIR, "tests.flask.conf")

    def setUp(self):
        ArticlesTestCase.setUp(self)

        # Flask app
        self.flask_app = create_flask_app()
        # Load configuration
        load_flask_configuration(self.flask_app, self.FLASK_CONFIGURATION_FILE)
        # Flask TESTING flag
        self.flask_app.config['TESTING'] = True

        # Get flask app context
        self.flask_app_context = self.flask_app.app_context()
        self.flask_app_context.push()

        # Client
        self.client = self.flask_app.test_client()

    def tearDown(self):
        self.flask_app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def assertResponseCode(self, response, status_code):
        self.assertEqual(response.status_code,
                         status_code,
                         'Unexpected status code: %d' % response.status_code)


class ArticleTestCase(FlaskTestCase):

    def get_test_id(self):
        return 'test'

    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}

    def setUp(self):
        FlaskTestCase.setUp(self)
        # Clear test document
        self.client.delete('/article/%s' % self.get_test_id())
