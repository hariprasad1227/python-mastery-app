"""
Python Mastery - Hardened AST Security Analyzer
Statically analyzes submitted learner code to reject dangerous calls, imports,
dunder-based sandbox escapes, and system introspection before execution.
"""

import ast
from typing import Tuple, Optional

# Forbidden module imports
BLOCKED_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "http", "urllib", "requests",
    "pty", "threading", "multiprocessing", "asyncio", "ctypes", "builtins",
    "importlib", "pickle", "shelve", "tempfile", "pathlib", "posix", "nt",
    "winreg", "signal", "_thread", "code", "inspect", "gc", "platform", "resource"
}

# Forbidden function calls and identifiers
BLOCKED_NAMES = {
    "eval", "exec", "compile", "open", "__import__", "globals", "locals",
    "vars", "dir", "breakpoint", "getattr", "setattr", "delattr",
    "memoryview", "quit", "exit", "help"
}

# Dangerous dunder attributes used in Python sandbox escapes
BLOCKED_DUNDERS = {
    "__subclasses__", "__bases__", "__class__", "__mro__", "__globals__",
    "__code__", "__closure__", "__builtins__", "__dict__", "__reduce__",
    "__reduce_ex__", "__getstate__", "__setstate__", "__import__", "__loader__",
    "__spec__"
}

ALLOWED_MAGIC_METHODS = {
    "__init__", "__str__", "__repr__", "__len__", "__getitem__", "__setitem__",
    "__iter__", "__next__", "__eq__", "__ne__", "__lt__", "__gt__", "__le__",
    "__ge__", "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__",
    "__mod__", "__pow__", "__contains__"
}


class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violation: Optional[str] = None

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            base_mod = alias.name.split(".")[0]
            if base_mod in BLOCKED_MODULES:
                self.violation = f"Importing module '{alias.name}' is prohibited in the sandbox."
                return
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            base_mod = node.module.split(".")[0]
            if base_mod in BLOCKED_MODULES:
                self.violation = f"Importing from module '{node.module}' is prohibited in the sandbox."
                return
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Detect calls to eval(), exec(), open(), getattr(), etc.
        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_NAMES:
                self.violation = f"Calling '{node.func.id}()' is prohibited for sandbox safety."
                return
        # Detect dunder function calls: e.g. ().__class__.__subclasses__()
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if attr_name in BLOCKED_DUNDERS:
                self.violation = f"Accessing attribute '{attr_name}' is prohibited."
                return
            if attr_name.startswith("__") and attr_name not in ALLOWED_MAGIC_METHODS:
                self.violation = f"Accessing special dunder attribute '{attr_name}' is prohibited."
                return
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        attr_name = node.attr
        if attr_name in BLOCKED_DUNDERS:
            self.violation = f"Direct introspection of '{attr_name}' is prohibited."
            return
        if attr_name.startswith("__") and attr_name not in ALLOWED_MAGIC_METHODS:
            self.violation = f"Access to special attribute '{attr_name}' is prohibited."
            return
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        # Catch string literals trying to pass dunder names to indirect reflection
        if isinstance(node.value, str) and node.value in BLOCKED_DUNDERS:
            self.violation = f"Referencing restricted identifier '{node.value}' is prohibited."
            return
        self.generic_visit(node)


def check_code_safety(source_code: str) -> Tuple[bool, Optional[str]]:
    """
    Parses and checks user Python source code for sandbox safety.
    Returns: (is_safe, error_message_if_any)
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} on line {e.lineno}"

    visitor = SecurityVisitor()
    visitor.visit(tree)

    if visitor.violation:
        return False, visitor.violation

    return True, None
