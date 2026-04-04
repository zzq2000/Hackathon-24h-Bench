"""
模块入口点

允许通过 python -m code_agent_controller 运行。
"""

import sys
from .controller import main

if __name__ == "__main__":
    sys.exit(main())
