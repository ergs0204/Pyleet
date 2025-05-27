# Project Brief: Pyleet

## Overview
Pyleet is a Python tool designed to allow users to run and test their LeetCode solutions locally with minimal modification. Since LeetCode's code structure is tailored for their online judge, running the same code locally is often cumbersome. Pyleet aims to bridge this gap by providing a simple CLI utility that can parse user-inserted test cases within their solution files and execute them seamlessly.

## Goals
- Enable running LeetCode Python solutions locally without significant code changes.
- Allow users to provide test cases in a separate file (e.g., `.txt` or `.json`).
- Parse these external test cases and execute the solution accordingly.
- Provide a CLI command `pyleet solution.py --testcases cases.txt` to run the solution with test cases.
- Package the tool so it can be installed via `setup.py` or `pip`.
- Support common LeetCode data structures (lists, trees, linked lists, etc.) in test case parsing.

## Core Features
- CLI interface (`pyleet`) to run solutions.
- Test case loading from external files.
- Input parsing compatible with LeetCode-style data structures.
- Output comparison to expected results.
- Minimal setup required for users.

## Out of Scope (Initial Version)
- Automatic test case generation.
- Web scraping or integration with LeetCode's platform.
- Support for languages other than Python.

## Success Criteria
- Users can install Pyleet via pip or setup.py.
- Users can save test cases in a separate file.
- Running `pyleet solution.py --testcases cases.txt` executes the solution with those test cases.
- No modification needed to the original LeetCode code.
