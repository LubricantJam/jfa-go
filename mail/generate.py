import subprocess
import shutil
import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output directory for .html and .txt files")

args = parser.parse_args()

def runcmd(cmd):
    if os.name == "nt":
        return subprocess.check_output(cmd, shell=True)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return proc.communicate()


local_path = Path(__file__).resolve().parent

for mjml in [f for f in local_path.iterdir() if f.is_file() and "mjml" in f.suffix]:
    print(f"Compiling {mjml.name}")
    fname = mjml.with_suffix(".html")
    runcmd(f"npx mjml {str(mjml)} -o {str(fname)}")
    if fname.is_file():
        print("Done.")

html = [f for f in local_path.iterdir() if f.is_file() and "html" in f.suffix]

output = Path(args.output)  # local_path.parent / "build" / "data"
output.mkdir(parents=True, exist_ok=True)

for f in html:
    shutil.copy(str(f), str(output / f.name))
    print(f"Copied {f.name} to {str(output / f.name)}")
    txtfile = f.with_suffix(".txt")
    if txtfile.is_file():
        shutil.copy(str(txtfile), str(output / txtfile.name))
        print(f"Copied {txtfile.name} to {str(output / txtfile.name)}")
    else:
        print(
            f"Warning: {txtfile.name} does not exist. Text versions of emails should be supplied."
        )
