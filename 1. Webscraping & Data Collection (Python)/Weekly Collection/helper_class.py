import os
import shutil

class Helper:

    def delete_file(self, filepath):
        try:
            # Check if path exists
            if os.path.exists(filepath):
                # Remove file
                os.remove(filepath)
                print(f"Succesfully deleted {filepath}")
        except Exception as e:
            # Print error
            print(f'Error deleting {filepath}:', str(e))

    def copy_from_location1_to_location2(self, filepath1, filepath2):
        try:
            if os.path.exists(filepath1):
                # Make copy in archive
                shutil.copyfile(filepath1, filepath2)
                print(f"Succesfully copied {filepath1} to {filepath2}.")
        except Exception as e:
            # Print error
            print(f'Error copying {filepath1} to {filepath2}:', str(e))