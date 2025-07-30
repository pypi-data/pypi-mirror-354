# USCG Leetcode Validator

A secure Python code validator for coding challenge platforms like LeetCode-style or CTF environments.

This package runs and validates submitted Python functions under strict constraints using Python's AST (Abstract Syntax Tree). It ensures that only allowed operations (like basic loops, arithmetic, and safe built-ins) are used. This is ideal for running untrusted user code in coding competitions, while preventing unsafe or unwanted behavior.

---

## 🚀 Features

- ✅ Accepts only a single top-level function in the submitted code
- ✅ Rejects all imports, lambdas, classes, and custom function definitions
- ✅ Optionally allows safe built-ins like `len()` and `range()`
- ✅ Enforces AST-level constraints before execution
- ✅ Runs submitted function against a list of test cases
- ✅ Outputs time taken and pass/fail result for each test case

---

## 📦 Installation

To install from PyPI:

```bash
pip install uscg-leetcode-validator
```