import os

# Get the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define paths relative to the project root
DATA_FILE_PATH = os.path.join(project_root, 'data/meta/haskell.txt')
REPO_ROOT_PATH = os.path.join(project_root, 'data/repos')
SOURCE_ROOT_PATH = os.path.join(project_root, 'data/source')

