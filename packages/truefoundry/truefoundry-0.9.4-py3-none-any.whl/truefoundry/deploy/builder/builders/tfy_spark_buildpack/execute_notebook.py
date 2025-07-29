# This script is used as the main application file for spark applications
# when the application to be run is a notebook, the actual notebook to be
# executed is passed as an argument to this script.


import papermill as pm
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python execute_notebook.py <notebook_path>")
        sys.exit(1)

    notebook_path = sys.argv[1]

    pm.execute_notebook(
        notebook_path,
        "output.ipynb",
        parameters=dict(),
    )