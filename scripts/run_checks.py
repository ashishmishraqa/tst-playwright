#!/usr/bin/env python3
"""
Pre-commit quality checks for pytest projects with detailed output.
Run: python run_checks.py
"""

import subprocess
import sys
from pathlib import Path


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREY = "\033[90m"
    END = "\033[0m"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def run_check(
    name: str, command: str, fail_on_error: bool = True, show_output: bool = True
) -> bool:
    """Execute a check command with detailed output."""
    print(f"{Colors.CYAN}▸ {name}...{Colors.END}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{Colors.GREEN}  ✓ {name} passed{Colors.END}\n")
            return True
        else:
            # Show error message
            print(f"{Colors.RED}  ✗ {name} failed{Colors.END}\n")

            # Show stdout (usually contains the actual errors)
            if result.stdout and show_output:
                print(f"{Colors.YELLOW}Output:{Colors.END}")
                print(f"{Colors.GREY}{result.stdout}{Colors.END}\n")

            # Show stderr (error messages)
            if result.stderr and show_output:
                print(f"{Colors.RED}Errors:{Colors.END}")
                print(f"{Colors.GREY}{result.stderr}{Colors.END}\n")

            if fail_on_error:
                return False
            else:
                print(f"{Colors.YELLOW}(Non-blocking—continuing){Colors.END}\n")
                return True  # Non-blocking

    except Exception as e:
        print(f"  {Colors.YELLOW}⚠ Could not run {name}: {e}{Colors.END}\n")
        return not fail_on_error


def main():
    print_header("🔍 Pre-Commit Quality Checks")

    # Define checks with: (name, command, blocking, show_details)
    checks = [
        ("Black formatting", "python -m black --check . --verbose", True, True),
        ("isort import ordering", "python -m isort --check . --diff", True, True),
        (
            "Pylint (errors only)",
            "python -m pylint tests/ src/ --disable=all --enable=E,F --exit-zero",
            False,
            True,
        ),
        (
            "MyPy type checking",
            "python -m mypy tests/ src/ --no-error-summary 2>&1 || exit 0",
            False,
            True,
        ),
        ("Pytest test suite", "python -m pytest -v --tb=short", True, True),
        (
            "Test coverage (75%)",
            "python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=75 -q",
            True,
            True,
        ),
        (
            "Bandit security scan",
            "python -m bandit -r . -ll -f json 2>/dev/null || echo 'Bandit check complete'",
            False,
            True,
        ),
    ]

    failed_checks = []
    passed_checks = []
    skipped_checks = []

    for check_name, cmd, blocking, show_details in checks:
        success = run_check(
            check_name, cmd, fail_on_error=blocking, show_output=show_details
        )

        if success:
            passed_checks.append(check_name)
        elif blocking:
            failed_checks.append(check_name)
        else:
            skipped_checks.append(check_name)

    # Print summary
    print_header("📊 Check Summary")

    print(f"{Colors.GREEN}✓ Passed ({len(passed_checks)}):{Colors.END}")
    for check in passed_checks:
        print(f"  • {check}")

    if failed_checks:
        print(f"\n{Colors.RED}✗ Failed ({len(failed_checks)}):{Colors.END}")
        for check in failed_checks:
            print(f"  • {check}")

    if skipped_checks:
        print(f"\n{Colors.YELLOW}⚠ Non-blocking ({len(skipped_checks)}):{Colors.END}")
        for check in skipped_checks:
            print(f"  • {check}")

    print()

    # Final verdict
    if failed_checks:
        print(
            f"{Colors.RED}❌ Some checks failed. Fix them before committing.{Colors.END}\n"
        )
        print(f"{Colors.YELLOW}Quick fixes:{Colors.END}")
        print(f"  • Black:  python -m black .")
        print(f"  • isort:  python -m isort .")
        print(f"  • Tests:  python -m pytest -v --tb=short -x\n")
        return 1
    else:
        print(
            f"{Colors.GREEN}✅ All critical checks passed! Safe to commit.{Colors.END}\n"
        )
        return 0


if __name__ == "__main__":
    sys.exit(main())


# # 1. Auto-fix formatting
# python -m black .
# python -m isort .
#
# # 2. Check what fixed
# python -m black --check .
# python -m isort --check .
#
# # 3. Run tests to see failures
# python -m pytest -v --tb=short -x
#
# # 4. Fix test issues (depends on output)
#
# # 5. Run full checks again
# python run_checks.py
