"""main entry point"""

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m jing_test"

from main import main

main()
