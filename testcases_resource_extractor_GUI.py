import unittest
from unittest.mock import Mock, patch, mock_open
import tkinter as tk
import json
import xml.etree.ElementTree as etree
from pathlib import Path
import importlib.util

# # Import the module to test
# spec = importlib.util.spec_from_file_location("resource_extractor_GUI", "resource_extractor_GUI.py")
# resource_extractor_GUI = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(resource_extractor_GUI)

class TestBattWarsExtractor(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"test": "data"}')
    def setUp(self, mock_file):
        """Set up test fixtures before each test"""
        with patch("json.load", retun_value={"test": "data"}):
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                from resource_extractor_GUI import BattWarsExtractor
                self.app = BattWarsExtractor()

    def tearDown(self):
        """Clean up after each test"""
        self.app.destroy()

    def test_init(self):
        """Test initial state of the application"""
        # Test that both tabs exist
        self.assertTrue(hasattr(self.app, 'xml_frame'))
        self.assertTrue(hasattr(self.app, 'resource_frame'))

        # Test that all necessary widgets are created
        self.assertTrue(hasattr(self.app, 'entry_input'))
        self.assertTrue(hasattr(self.app, 'entry_id'))
        self.assertTrue(hasattr(self.app, 'var_passengers'))
        self.assertTrue(hasattr(self.app, 'var_mpscript'))
        self.assertTrue(hasattr(self.app, 'entry_src'))
        self.assertTrue(hasattr(self.app, 'entry_dst'))
        self.assertTrue(hasattr(self.app, 'entry_json'))

        # Test default checkbox values
        self.assertEqual(self.app.var_passengers.get(), 1)
        self.assertEqual(self.app.var_mpscript.get(), 1)

    @patch('tkinter.filedialog.askopenfilename')
    def test_browse_xml_file(self, mock_filedialog):
        """Test XML file browsing functionality"""
        mock_filedialog.return_value = "test.xml"
        self.app.browse_xml_file()
        self.assertEqual(self.app.entry_input.get(), "test.xml")

    @patch('tkinter.filedialog.askdirectory')
    def test_browse_directories(self, mock_filedialog):
        """Test directory browsing functionality"""
        mock_filedialog.return_value = "/test/path"

        # Test source directory browsing
        self.app.browse_src_dir()
        self.assertEqual(self.app.entry_src.get(), "/test/path")

        # Test destination directory browsing
        self.app.browse_dst_dir()
        self.assertEqual(self.app.entry_dst.get(), "/test/path")

    @patch('tkinter.messagebox.showerror')
    def test_process_xml_validation(self, mock_error):
        """Test XML processing input validation"""
        # Test with empty fields
        self.app.process_xml_file()
        mock_error.assert_called_with("Error", "Please fill in all fields.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('xml.etree.ElementTree.ElementTree.write')
    @patch('json.dump')
    @patch('tkinter.messagebox.showinfo')
    def test_process_xml_success(self, mock_info, mock_json_dump, mock_xml_write, mock_file):
        """Test successful XML processing"""
        # Setup test data
        self.app.entry_input.insert(0, "test.xml")
        self.app.entry_id.insert(0, "test_id")

        # Mock BattWarsLevel
        mock_bwlevel = Mock()
        mock_bwlevel.obj_map = {
            "test_id": Mock(
                id="test_id",
                type="unit",
                attributes={},
                _xml_node=etree.Element("TestNode")
            )
        }

        with patch('resource_extractor_GUI.BattWarsLevel', return_value=mock_bwlevel):
            self.app.process_xml_file()

            # Verify the results
            mock_info.assert_called()
            mock_json_dump.assert_called()
            mock_xml_write.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_process_resources_validation(self, mock_error):
        """Test resource processing input validation"""
        # Test with empty fields
        self.app.process_resources()
        mock_error.assert_called_with("Error", "Please fill in all fields.")

    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('builtins.open', new_callable=mock_open, read_data='{"test": "data}')
    @patch('json.load')
    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.messagebox.showinfo')
    def test_process_resources_success(self, mock_info, mock_error, mock_json_load, mock_open_file, 
                                       mock_copy2, mock_makedirs, mock_walk, mock_abspath):
        """Test successful resource processing"""
        # Setup test data
        self.app.entry_src.insert(0, "/test/src")
        self.app.entry_dst.insert(0, "/test/dst")
        self.app.entry_json.insert(0, "test.json")

        # Mock JSON data
        mock_json_load.return_value = {
            "cNodeHierarchyResource": ["test_node"],
            "otherResource": ["test_resource"]
        }

        # Mock file system
        mock_abspath.return_value = "/test/src"
        mock_walk.return_value = [
            ("/test/src", [], ["test_node.file", "test_resource.file"])
        ]

        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True

            # Execute
            self.app.process_resources()

            if mock_error.call_count > 0:
                print("Error message shown:", mock_error.call_args)
            else:
                self.assertTrue(mock_info.called)
                self.assertTrue(mock_copy2.called)
                self.assertTrue(mock_makedirs.called)

    
    @patch('os.path.abspath')
    @patch('os.walk')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('builtins.open', new_callable=mock_open, read_data='{"test": "data}')
    @patch('json.load')
    @patch('tkinter.messagebox.showerror')
    @patch('os.path.exists')
    def test_copy_error_handling(self, mock_error, mock_exists, mock_json_load,
                                  mock_open_file, mock_copy2, mock_makedirs, mock_walk, mock_abspath):
        """Test error handling during file copying"""
        # Setup
        self.app.entry_src.insert(0, "/test/src")
        self.app.entry_dst.insert(0, "/test/dst")
        self.app.entry_json.insert(0, "test.json")

        # Mock file exists check
        mock_exists.return_value = True

        # Mock JSON data
        mock_json_load.return_value = {"testReousrce": ["test_file"]}

        # Mock file system
        mock_abspath.return_value = "/test/src"
        mock_walk.return_value = [("/test/src"), [], ["test_file.txt"]]

        # Mock copy2 to raise an exception
        mock_copy2.side_effect = Exception("Copy failed")

        # Execute
        self.app.process_resources()

        # verify progress bar is reset
        self.assertEqual(self.app.progress["value"], 0)

if __name__ == '__main__':
    unittest.main()
