import os

PROJ_ROOT = os.getenv("BENCH_F_HOME")
assert PROJ_ROOT is not None, "Please source env.sh"

# define paths relative to the project root
DATA_FILE_PATH = os.path.join(PROJ_ROOT, "data/meta/haskell.txt")
REPO_ROOT_PATH = os.path.join(PROJ_ROOT, "data/repos")
SOURCE_ROOT_PATH = os.path.join(PROJ_ROOT, "data/source")
