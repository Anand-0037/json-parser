import sys
from pathlib import Path
from .json_parser import parse_json_file

def run_all_tests():
    """
    Scans the 'tests' directory and runs validation on all valid/invalid JSON files.
    it is 
    """
    test_dir = Path("tests")
    if not test_dir.exists():
        print("ERR: 'tests' directory not found. No tests to run.")
        return False

    all_passed = True
    test_files_found = False

    # for valid files
    for valid_file in sorted(test_dir.glob("**/valid*.json")):
        test_files_found = True
        try:
            parse_json_file(str(valid_file))
            print(f"OK: PASSED - {valid_file.relative_to(test_dir)}")
        except Exception as e:
            print(f"ERR: FAILED - {valid_file.relative_to(test_dir)} - Should be valid, but got error: {e}")
            all_passed = False

    # for invalid files
    for invalid_file in sorted(test_dir.glob("**/invalid*.json")):
        test_files_found = True
        try:
            parse_json_file(str(invalid_file))
            print(f"ERR: FAILED - {invalid_file.relative_to(test_dir)} - Should be invalid, but was parsed successfully.")
            all_passed = False
        except Exception as e:
            # ouptut of invalid file
            print(f"OK: PASSED - {invalid_file.relative_to(test_dir)} is invalid as expected ({e})")

    if not test_files_found:
        print("No test files found in the 'tests' directory.")
        return False

    return all_passed

if __name__ == "__main__":
    print("Running JSON Parser Test Suite...\n")
    
    success = run_all_tests()
    
    print("\n" + "-"*50)
    if success:
        print("OK: Overall Status - ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("ERR: Overall Status - SOME TESTS FAILED")
        sys.exit(1)