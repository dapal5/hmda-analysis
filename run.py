import subprocess
import sys

def main():
    subprocess.run([sys.executable, "extract.py"], check=True)
    subprocess.run([sys.executable, "load.py"], check=True)
    subprocess.run(["dbt", "run"], cwd="hmda", check=True)
    print("pipeline complete")

if __name__ == "__main__":
    main()