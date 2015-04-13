import unittest, resources

class TestLicenseChange(unittest.TestCase):

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')
		

if __name__ == '__main__':
    unittest.main()