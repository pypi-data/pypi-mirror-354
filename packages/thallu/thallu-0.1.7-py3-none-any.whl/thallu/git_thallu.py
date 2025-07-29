import subprocess
from pathlib import Path
import argparse
import inquirer
import questionary


def git_init():
    if Path(".git").exists():
        return "✅ Git repo already initialized."
    res = subprocess.run(["git", "init"], capture_output=True, text=True, check=True)
    return res.stdout


def git_remote(config_file="plan.txt"):
    config_path = Path.cwd() / config_file
    if not config_path.exists():
        raise FileNotFoundError(f"Missing '{config_file}' in project directory.")

    config = {}
    with open(config_path, "r") as f:
        exec(f.read(), {}, config)

    username = config.get("username", "").strip()
    repo = config.get("repo", "").strip()
    if not username or not repo:
        raise ValueError(f"Invalid or missing 'username' or 'repo' in {config_file}")

    url = f"https://github.com/{username}/{repo}.git"

    remotes = subprocess.run(
        ["git", "remote"], capture_output=True, text=True, check=True
    ).stdout.split()

    if "origin" in remotes:
        return "✅ Remote 'origin' already exists."
    else:
        res = subprocess.run(
            ["git", "remote", "add", "origin", url], capture_output=True, text=True, check=True
        )
        return f"🔗 Added remote: {url}"


def git_add():
    res = subprocess.run(["git", "add", "."], capture_output=True, text=True, check=True)
    return "➕ Staged all files."


def git_commit():
    message = input("💬 Enter commit message: ").strip()
    if not message:
        message = "Update commit"
    res = subprocess.run(
        ["git", "commit", "-m", message], capture_output=True, text=True
    )
    if res.returncode != 0:
        # Usually no changes to commit
        return "⚠️ No changes to commit."
    return f"📦 Commit done: {message}"

def git_branch():
    res = subprocess.run(
        ["git", "branch", "-M", "main"], capture_output=True, text=True
    )
    if res.returncode == 0:
        return "🌿 Renamed branch to 'main'."
    else:
        return f"⚠️ Failed to rename branch. Reason: {res.stderr}"



#get the name of the current branch
def current_branch():
    res = subprocess.run(['git','rev-parse','--abbrev-ref','HEAD'] , capture_output=True , text=True)
    return res.stdout.strip()

def git_push():
    branch = current_branch()
    if branch == "HEAD_DETACHED_OR_NO_REPO":
        return "❌ Cannot push: Not in a valid Git repository or detached HEAD state."

    # CAUTION: --force is used here. Consider replacing with safer alternatives or a warning.
    # For now, keeping it as per original script.
    try:
        # Using branch variable directly in command
        res = subprocess.run(
            ["git", "push", "-u", "origin", branch, "--force"],
            capture_output=True, text=True, check=True # Use check=True to raise CalledProcessError
        )
        return f"🚀 Code pushed to GitHub (branch: {branch}).\n{res.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        # Capture the specific error from Git
        error_message = e.stderr.strip()
        return f"❌ Git push failed: {error_message}"


#to list all branches:
def list_branches():
    res = subprocess.run(['git', 'branch'], capture_output=True, text=True)
    # Each line looks like: "* 2.0" or "  main"
    branches = [line.strip().lstrip('* ').strip() for line in res.stdout.splitlines() if line.strip()]
    return branches


#to create a new brance andd checkout to that branch:
def new_branch():
    name = input("🌱 Enter the new branch name: ").strip()
    branches = list_branches()
    if name in branches:
        return f"⚠️ Branch '{name}' already exists."
    else:
        subprocess.run(['git', 'checkout', '-b', name], capture_output=True, text=True)
        # Push the new branch to origin
        push_res = subprocess.run(['git', 'push', '-u', 'origin', name], capture_output=True, text=True)
        if push_res.returncode == 0:
            return f"✅ Created and switched to branch '{name}'. Branch pushed to remote."
        else:
            return f"⚠️ Created and switched to branch '{name}', but failed to push:\n{push_res.stderr}"




#switch teh branches

def switch_branches(branch_name):
    res = subprocess.run(['git','switch',branch_name] , capture_output=True , text = True)
    if res.returncode ==0:
        return f'🔄 Switched to the branch : {branch_name}.'
    else:
        return f"❌ Failed to switch to branch '{branch_name}':\n{res.stderr}"
    
#switch using interactive inquirer
def switch_interactive():
    branches = list_branches()
    question =[ inquirer.List('branch',
                             message = 'Select the brach you need to switch ',
                             choices = branches)
    ]
    answer = inquirer.prompt(question)
    if answer:
        return switch_branches(answer['branch'])
    else:
        return '❌ No branch selected.'


#merge branches
def merge_branches(branches):
    target_branch = current_branch()
    print(f"🧬 Merging into current branch: {target_branch}")
    
    for b in branches:
        print(f"\n🔀 Merging {b} into {target_branch}...")
        result = subprocess.run(["git", "merge", b ,'--no-edit'])
        if result.returncode != 0:
            print(f"❌ Merge conflict or error with {b}. Resolve and continue manually.")
            break
        else:
            print(f"✅ Successfully merged {b}")

#merge interactive
def merge_interactive():
    current = current_branch()
    options = [b for b in list_branches() if b != current]

    selected = questionary.checkbox(
        "🧩 Select branches to merge into current branch:",
        choices=options
    ).ask()

    if not selected:
        print("❗ No branches selected.")
        return
    merge_branches(selected)



#delete branch

def delete_branch(branch_name):
    current = current_branch()
    if branch_name == current:
        return "❌ Cannot delete the branch you are currently on."
    #to delete the local branch:
    res_local = subprocess.run(['git','branch','-d',branch_name],capture_output=True , text = True)
    if res_local.returncode !=0:
        res_force = subprocess.run(['git','branch','-D',branch_name] , capture_output=True , text=True)
        if res_force.returncode !=0:
            return f"❌ Failed to delete local branch '{branch_name}':\n{res_force.stderr}"
        else:
            local_msg = f"⚠️ Force deleted local branch '{branch_name}'."
    else:
        local_msg = f"✅ Deleted local branch '{branch_name}'."

    # Delete remote branch
    res_remote = subprocess.run(
        ["git", "push", "origin", "--delete", branch_name], capture_output=True, text=True)
    if res_remote.returncode != 0:
        return f"{local_msg}\n⚠️ Failed to delete remote branch '{branch_name}':\n{res_remote.stderr}"
    else:
        remote_msg = f"✅ Deleted remote branch '{branch_name}'."

    return f"{local_msg}\n{remote_msg}"


#delete interactively
def delete_branch_interactive():
    branches = list_branches()
    current = current_branch()

    # Exclude current branch from choices to prevent accidental deletion
    choices = [b for b in branches if b != current]

    if not choices:
        print("❗ No branches available for deletion (except current branch).")
        return

    selected = questionary.checkbox(
        "🗑️ Select branch(es) to delete (current branch excluded):",
        choices=choices
    ).ask()

    if not selected:
        print("❗ No branch selected.")
        return

    for branch in selected:
        print(delete_branch(branch))



def thallu_main(update_only=False):
    if not update_only:
        print(git_init())
        print(git_remote())
        print(git_add())
        print(git_commit())
        current = current_branch()
        if current =='master':
            print(git_branch())

    else:
        print(git_add())
        print(git_commit())
    
    print(git_push())

def main():
    parser = argparse.ArgumentParser(description="Git automation tool: thallu")
    parser.add_argument("-u", "--update", action="store_true", help="Run update (add, commit, push) only")
    parser.add_argument("-b", "--branches", action="store_true", help="List all local branches")
    parser.add_argument("-nb", "--new-branch", action="store_true", help="Create and checkout to a new branch")
    parser.add_argument("-cb", "--current-branch", action="store_true", help="Return the current branch name")
    parser.add_argument("-sb", "--switch-branch", nargs='?', const=True,help="Switch branch: specify branch name or omit for interactive selection")
    parser.add_argument("-m", "--merge", nargs='*', help="Merge branches into the current branch")
    parser.add_argument("-d", "--delete",nargs='?',  # optional argument 
    const=True, # if no value passed, set to True to trigger interactive mode
    help="Delete a branch locally and remotely. Use without argument for interactive selection."
)


    args = parser.parse_args()

    # Priority-based handling
    if args.branches:
        print("🌿 Available branches:")
        for b in list_branches():
            print(f"- {b}")
    elif args.new_branch:
        print(new_branch())
    elif args.current_branch:
        print(f"🔎 Current branch: {current_branch()}")
    elif args.switch_branch is True:
        print(switch_interactive())
    elif isinstance(args.switch_branch, str):
        print(switch_branches(args.switch_branch))
    elif args.merge == []:
        merge_interactive()
    elif isinstance(args.merge, list):
        merge_branches(args.merge)
    
    elif args.delete:
        if args.delete is True:
            delete_branch_interactive()
        else:
            print(delete_branch(args.delete))
        return


    else:
        thallu_main(update_only=args.update)
