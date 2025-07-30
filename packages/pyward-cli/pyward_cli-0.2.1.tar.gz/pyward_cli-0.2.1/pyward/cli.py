#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import ast

# Assume these are the correct locations of your check-running functions
from pyward.fixer.fix_imports import fix_file
from pyward.optimization.run import run_all_optimization_checks
from pyward.security.run import run_all_security_checks


def analyze_file(filepath: str, run_optimization: bool, run_security: bool, skip_list: list[str]) -> list[str]:
    try:
        source = Path(filepath).read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise IOError(f"Could not read file {filepath}: {e}") from e

    opt_issues = []
    if run_optimization:
        opt_issues = run_all_optimization_checks(source, skip=skip_list)

    sec_issues = []
    if run_security:
        sec_issues = run_all_security_checks(ast.parse(source, filename=filepath), skip=skip_list)

    return opt_issues + sec_issues


class ArgumentParser1(argparse.ArgumentParser):
    def error(self, message):
        # 🐛 FIX: now catches missing required args and prints to stdout
        if "the following arguments are required" in message:
            output_stream = sys.stdout
            print(self.format_usage().strip(), file=output_stream)
            print(f"{self.prog}: error: {message}", file=output_stream)
            sys.exit(1)
        super().error(message)


def main():
     # Print a little ASCII logo only when stdout is a real terminal
    if sys.stdout.isatty():
        print(r"""
     ____      __        __            _ 
    |  _ \ _   \ \      / /_ _ _ __ __| |
    | |_) | | | \ \ /\ / / _` | '__/ _` |
    |  __/| |_| |\ V  V / (_| | | | (_| |
    |_|    \__, | \_/\_/ \__,_|_|  \__,_|
            |___/                         
            PyWard: fast, zero-config Python linting
        """)
    parser = ArgumentParser1(
        prog="pyward",
        description="PyWard: CLI linter for Python (optimization + security checks)",
    )

    parser.add_argument(
        "-f", "--fix", action="store_true",
        help="Auto-fix unused-import issues (writes file in place)."
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Recursively lint all .py files under a directory."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-o", "--optimize", action="store_true", help="Only run optimization checks."
    )
    group.add_argument(
        "-s", "--security", action="store_true", help="Only run security checks."
    )
    parser.add_argument(
        "-k", "--skip-checks",
        help="Comma-separated list of rule names (without 'check_' prefix) to skip."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Verbose output, even if no issues."
    )
    parser.add_argument(
        "filepath", type=Path,
        help="Path to the Python file or directory to analyze."
    )

    args = parser.parse_args()

    # Build list of files to process
    paths: list[Path] = []
    if args.filepath.is_dir():
        if not args.recursive:
            print(f"Error: {args.filepath} is a directory (use -r to recurse)", file=sys.stderr)
            sys.exit(1)
        # recursive glob for .py files
        paths = list(args.filepath.rglob("*.py"))
    else:
        paths = [args.filepath]

    if not paths:
        print(f"No Python files found in {args.filepath}", file=sys.stderr)
        sys.exit(1)

    # prepare skip list
    skip_list: list[str] = []
    if args.skip_checks:
        for name in args.skip_checks.split(","):
            nm = name.strip()
            if not nm.startswith("check_"):
                nm = f"check_{nm}"
            skip_list.append(nm)

    run_opt = not args.security
    run_sec = not args.optimize

    any_issues = False

    for path in paths:
        file_str = str(path)

        # apply fixes first, if requested
        if args.fix:
            fix_file(file_str, write=True)
            if args.verbose:
                print(f"🔧 Applied import fixes to {file_str}")

        try:
            issues = analyze_file(
                file_str,
                run_optimization=run_opt,
                run_security=run_sec,
                skip_list=skip_list
            )
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            any_issues = True
            continue
        except Exception as e:
            print(f"Error analyzing {file_str}: {e}", file=sys.stderr)
            any_issues = True
            continue

        # handle verbose/no-issue messaging per file
        if args.verbose and not issues:
            print(f"✅ No issues found in {file_str} (verbose)")
            continue

        if not issues:
            print(f"✅ No issues found in {file_str}")
            continue

        # report issues
        any_issues = True
        print(f"\n❌ Found {len(issues)} issue(s) in {file_str}")
        for idx, msg in enumerate(issues, 1):
            print(f"{idx}. {msg}")

    # exit status
    if any_issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
