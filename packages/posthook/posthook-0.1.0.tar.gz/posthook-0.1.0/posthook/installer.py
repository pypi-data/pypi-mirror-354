import os
import shutil
import subprocess

def install_hooks(repo_path):
    hooks_dir = os.path.join(os.path.dirname(__file__), 'hooks')
    git_hooks_dir = os.path.join(repo_path, '.git', 'hooks')
    root_env_path = os.path.join(repo_path, '.env')
    template_env_path = os.path.join(os.path.dirname(__file__), '..', '.env.example')

    if not os.path.isdir(git_hooks_dir):
        print("❌ Error: Target directory is not a valid Git repository.")
        return

    print("🔧 Installing Git hooks...")

    # Install all hooks
    for filename in os.listdir(hooks_dir):
        source = os.path.join(hooks_dir, filename)
        target = os.path.join(git_hooks_dir, filename)

        try:
            shutil.copyfile(source, target)
            os.chmod(target, 0o775)
            print(f"✅ Hook installed: {filename}")
        except Exception as e:
            print(f"❌ Failed to install {filename}: {e}")

    # Copy .env if missing
    if not os.path.exists(root_env_path):
        try:
            shutil.copyfile(template_env_path, root_env_path)
            print("✅ .env file created from template.")
            print("📌 Please fill in your Jira email, password/API token, and GPT key.")

            # Open in Notepad (Windows-only)
            try:
                subprocess.run(["notepad.exe", root_env_path], check=True)
            except Exception as e:
                print(f"⚠️  Could not open .env in Notepad: {e}")

        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
    else:
        print("⚠️  .env file already exists. No changes made.")

    print("🎉 Installation complete. You're ready to commit!")
