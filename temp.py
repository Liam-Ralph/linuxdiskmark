import subprocess
import os
user = os.environ.get("SUDO_USER") # or os.environ.get("USER")

result = subprocess.run(["sudo", "-u", user, "firefox", "--new-tab", "https://google.com"], capture_output = True, text = True)
if result.returncode != 0:
    print("Failed")
    subprocess.run(["sudo", "-u", user, "xdg-open", "https://google.com"])

print("HI")
exit(0)

# works but doesn't exit if
#  - firefox is not open
#  - firefox was previously opened by this program
# will not exit or print HI

# does not work if
# - firefox was opened by user