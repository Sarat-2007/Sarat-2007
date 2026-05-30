import os
import datetime
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}\nStdout: {result.stdout}\nStderr: {result.stderr}")
    return result.returncode == 0

def update_readme():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found.")
        return False
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_marker = "<!-- daily-update -->"
    update_text = f"{update_marker}\n<p align=\"right\"><sub><i>Last updated: {current_time} (Auto-update)</i></sub></p>"
    
    if update_marker in content:
        # Split and replace the old marker section
        parts = content.split(update_marker)
        # We assume the old marker is at the end. We'll reconstruct.
        content = parts[0] + update_text
    else:
        content += f"\n\n{update_text}"
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"README updated successfully at {current_time}.")
    return True

def git_push():
    if not run_cmd("git add README.md"):
        return False
    if not run_cmd('git commit -m "chore: daily profile pulse update"'):
        print("Nothing to commit or commit failed.")
        # If there are no changes, we still return True so it doesn't error out
    if not run_cmd("git push origin main"):
        return False
    print("Successfully pushed daily update to GitHub!")
    return True

if __name__ == "__main__":
    if update_readme():
        git_push()
