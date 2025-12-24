import unittest
import os
import sys
import yaml
import tempfile

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import load_config

class TestConfigLoading(unittest.TestCase):
    def setUp(self):
        self.test_config = {
            'timezone': 'Australia/Sydney',
            'sharepoint': {'site_url': 'https://example.sharepoint.com'},
            'powerbi': {'workspace_id': '12345'}
        }
        self.tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml')
        yaml.dump(self.test_config, self.tmp_file)
        self.tmp_file.close()

    def tearDown(self):
        os.unlink(self.tmp_file.name)

    def test_load_valid_config(self):
        config = load_config(self.tmp_file.name)
        self.assertEqual(config['timezone'], 'Australia/Sydney')
        self.assertEqual(config['sharepoint']['site_url'], 'https://example.sharepoint.com')

    def test_load_missing_config(self):
        with self.assertRaises(FileNotFoundError):
            load_config("non_existent_file.yaml")

    def test_load_invalid_yaml(self):
        invalid_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml')
        invalid_file.write("invalid: [ yaml: content") # Broken yaml
        invalid_file.close()
        try:
            with self.assertRaises(yaml.YAMLError):
                load_config(invalid_file.name)
        finally:
            os.unlink(invalid_file.name)

if __name__ == '__main__':
    unittest.main()
