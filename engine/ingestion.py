import os
import subprocess

def clone_or_setup_repo(target_path):
    """
    If the target is a github URL, clones it into a temp directory within Scanner_v5.
    Otherwise, verifying it exists locally.
    """
    if target_path.startswith("http://") or target_path.startswith("https://"):
        print(f"[+] Ingestion targeting remote repository: {target_path}")
        repo_name = target_path.rstrip('/').split('/')[-1].replace('.git', '')
        clone_dir = os.path.join(os.getcwd(), f"_{repo_name}_ingested")
        
        if not os.path.exists(clone_dir):
            try:
                subprocess.run(["git", "clone", target_path, clone_dir], check=True, capture_output=True)
                print(f"[+] Successfully cloned to {clone_dir}")
            except Exception as e:
                print(f"[-] Failed to clone repository: {e}")
                return None
        return clone_dir
        
    elif os.path.exists(target_path):
        return target_path
    else:
        print(f"[-] Target {target_path} is neither a valid URL nor a local directory.")
        return None
