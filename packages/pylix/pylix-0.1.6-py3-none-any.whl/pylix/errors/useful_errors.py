from enum import Enum
from typing import Union

import numpy as np

from pylix.errors.error_messages import *
from pylix.errors.enums import *

class BaseError(Exception):
    def __init__(self, code, msg="", wrong=None, right=None, err: str = "Error"):
        if isinstance(code, Enum):
            if len(msg) == 0:
                if isinstance(code, ArgumentCodes):
                    msg = ARGUMENT_ERROR_MESSAGES.get(code, "")
                elif isinstance(code, BaseCodes):
                    msg = BASE_ERROR_MESSAGES.get(code, "")
                elif isinstance(code, MathCodes):
                    msg = MATH_ERROR_MESSAGES.get(code, "")
            code = code.value
        if wrong is not None:
            msg += f"\nWrong: {wrong}"
        if right is not None:
            msg += f"\nRight (Pattern): {right}"
        self.wrong = wrong
        self.right = right
        self.msg = msg
        super().__init__(f"{err} {code}: {msg}")

class ArgumentError(BaseError):
    def __init__(self, code: ArgumentCodes, msg="", wrong_argument=None, right_argument=None):
        super().__init__(code, msg, wrong_argument, right_argument, "Argument Error")

class MathError(BaseError):
    def __init__(self, code: MathCodes, msg="", wrong_argument=None, right_argument=None):
        super().__init__(code, msg, wrong_argument, right_argument, "Math Error")

class StateError(BaseError):
    def __init__(self, msg=""):
        super().__init__(BaseCodes.NONE, msg, None, None, "State Error")

