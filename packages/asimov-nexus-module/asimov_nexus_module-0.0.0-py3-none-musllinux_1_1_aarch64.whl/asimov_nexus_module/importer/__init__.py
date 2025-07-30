import sys

__version__ = "0.0.0"

def main(argv=sys.argv):
    import os, subprocess
    argv = [os.path.join(os.path.dirname(__file__), "asimov-nexus-importer"), *argv[1:]]
    subprocess.call(argv)
