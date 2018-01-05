import unittest


class ApiTest(unittest.TestCase):
    
    def get_api_url(self):
        pass
    
    def get_allowed_methods(self):
        return []
    
    def runTest(self):
        for method in ['GET', 'PATCH', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']:
            if not method in self.get_allowed_methods():
                # Test method for API url
                response = self.client.open(method=method)
                self.assertEqual(response.status_code, 404, '%s should not be allowed for URL %s' % (method, self.get_api_url()))
                
    def assertResponseCode(self, response, status_code):
        self.assertEqual(response.status_code, status_code, 'Unexpected response status code: %d' % response.status_code)
