import os
import unittest

from aplos_nca_saas_sdk.utilities.file_utility import FileUtility
class FileUtilityTest(unittest.TestCase):

    def test_find_file(self):

        fu: FileUtility = FileUtility()
        file = fu.find_file(starting_path=__file__, file_name="test.txt", raise_error_if_not_found=False)
        self.assertIsNone(file)


        file = fu.find_file(starting_path=__file__, file_name="readme.md", raise_error_if_not_found=False)
        self.assertIsNotNone(file)
        file_exists = os.path.exists(file)
        self.assertTrue(file_exists)



def main():
    unittest.main()


if __name__ == "__main__":
    main()