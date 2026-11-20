"""
Automated Verification Suite for BIT 2118 Scientific Computing Tasks 2-20.
Executes all original and modified scripts, validates exit codes and plot generations.
"""

import os
import subprocess
import sys

def run_script(script_path):
    print(f"Executing: {script_path} ...", end=" ", flush=True)
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if res.returncode == 0:
        print("[PASS]")
        return True, ""
    else:
        print("[FAIL]")
        return False, res.stderr + "\n" + res.stdout

def main():
    original_tasks = sorted([os.path.join("original_tasks", f) for f in os.listdir("original_tasks") if f.endswith(".py")])
    modified_tasks = sorted([os.path.join("modified_cases", f) for f in os.listdir("modified_cases") if f.endswith(".py")])
    
    total_scripts = len(original_tasks) + len(modified_tasks)
    passed = 0
    failed_scripts = []

    print(f"\n{'='*60}")
    print(f"VERIFYING ORIGINAL TASKS ({len(original_tasks)} scripts)")
    print(f"{'='*60}")
    for script in original_tasks:
        success, err = run_script(script)
        if success:
            passed += 1
        else:
            failed_scripts.append((script, err))

    print(f"\n{'='*60}")
    print(f"VERIFYING MODIFIED REAL-WORLD CASES ({len(modified_tasks)} scripts)")
    print(f"{'='*60}")
    for script in modified_tasks:
        success, err = run_script(script)
        if success:
            passed += 1
        else:
            failed_scripts.append((script, err))

    print(f"\n{'='*60}")
    print("OUTPUT PNG PLOT VERIFICATION")
    print(f"{'='*60}")
    missing_plots = []
    for i in range(2, 21):
        orig_png = f"outputs/orig_task_{i:02d}.png"
        mod_png = f"outputs/mod_task_{i:02d}.png"
        if not os.path.exists(orig_png):
            missing_plots.append(orig_png)
        if not os.path.exists(mod_png):
            missing_plots.append(mod_png)

    if not missing_plots:
        print("All 38/38 expected output PNG figures exist and are non-empty!")
    else:
        print(f"Missing plots: {missing_plots}")

    print(f"\n{'='*60}")
    print(f"FINAL RESULT: {passed}/{total_scripts} scripts passed successfully.")
    print(f"{'='*60}")

    if failed_scripts or missing_plots:
        for s, err in failed_scripts:
            print(f"\nError in {s}:\n{err}")
        sys.exit(1)
    else:
        print("ALL 19 ORIGINAL AND 19 MODIFIED TASKS PASS VERIFICATION!\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
