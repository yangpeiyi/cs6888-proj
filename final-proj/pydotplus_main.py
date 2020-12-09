import os
import random
import sys


from pythonfuzz.main import PythonFuzz
import pydotplus


@PythonFuzz(dirs=[sys.argv[1]])
def fuzz(buf):
    try:
        string = buf.decode("ascii")
        graphs = pydotplus.graph_from_dot_data(string)
    except UnicodeDecodeError:
        pass


if __name__ == '__main__':
    fuzz()