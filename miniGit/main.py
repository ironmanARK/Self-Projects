import os
import sys
from blob import Blob
from tree import Tree
from commit import Commit

MINIGIT_DIR = ".minigit"
OBJECTS_DIR = os.path.join(MINIGIT_DIR, "objects")
INDEX_FILE = os.path.join(MINIGIT_DIR, "index")
HEAD_FILE = os.path.join(MINIGIT_DIR, "HEAD")
def init():
    if not os.path.exists(MINIGIT_DIR):
        os.makedirs(MINIGIT_DIR)
    if not os.path.exists(OBJECTS_DIR):
        os.makedirs(OBJECTS_DIR)
    open(INDEX_FILE, "w").close()
    with open(HEAD_FILE, "w") as f:
        f.write("")
    print("Initialized empty miniGit repository.")

def add(filenames):
    entries = {}
    for filename in filenames:
        if not os.path.exists(filename):
            print(f"Error: {filename} does not exist")
            continue
        blob = Blob(filename)
        blob_hash = blob.store()
        entries[filename] = blob_hash
        print(f"Added {filename} as blob {blob_hash}")

    with open(INDEX_FILE, "w") as idx:
        for fname, h in entries.items():
            idx.write(f"{fname} {h}\n")

def commit(message):
    entries = {}
    if not os.path.exists(INDEX_FILE):
        print("Nothing to commit.")
        return

    with open(INDEX_FILE, "r") as idx:
        for line in idx:
            fname, h = line.strip().split()
            entries[fname] = h

    if not entries:
        print("Nothing to commit.")
        return

    tree = Tree(entries)
    tree_hash = tree.store()

    parent = None
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "r") as f:
            head = f.read().strip()
            if head:
                parent = head

    new_commit = Commit(tree_hash, message, parent)
    commit_hash = new_commit.store()

    with open(HEAD_FILE, "w") as f:
        f.write(commit_hash)

    print(f"Commit created: {commit_hash}")

def log():
    if not os.path.exists(HEAD_FILE):
        print("No commits yet.")
        return
    with open(HEAD_FILE, "r") as f:
        commit_hash = f.read().strip()

    while commit_hash:
        commit_path = os.path.join(OBJECTS_DIR, commit_hash)
        if not os.path.exists(commit_path):
            break
        with open(commit_path, "rb") as f:
            data = f.read().decode(errors="ignore")
        print(f"Commit {commit_hash}:\n{data}\n{'-'*40}")
        parent = None
        for line in data.splitlines():
            if line.startswith("parent "):
                parent = line.split(" ")[1]
                break
        commit_hash = parent


def checkout(commit_hash):
    commit_path = os.path.join(OBJECTS_DIR, commit_hash)
    if not os.path.exists(commit_path):
        print(f"Error: commit {commit_hash} does not exist")
        return

    with open(commit_path, "rb") as f:
        data = f.read().split(b"\x00", 1)[1].decode(errors="ignore")

    tree_hash = None
    for line in data.splitlines():
        if line.startswith("tree "):
            tree_hash = line.split(" ")[1]
            break

    if not tree_hash:
        print("Invalid commit: no tree found.")
        return

    tree_path = os.path.join(OBJECTS_DIR, tree_hash)
    with open(tree_path, "rb") as f:
        tree_data = f.read().split(b"\x00", 1)[1].decode(errors="ignore")

    for entry in tree_data.splitlines():
        blob_hash, filename = entry.split(" ", 1)
        blob_path = os.path.join(OBJECTS_DIR, blob_hash)
        with open(blob_path, "rb") as bf:
            content = bf.read().split(b"\x00", 1)[1]
        with open(filename, "wb") as wf:
            wf.write(content)

    with open(HEAD_FILE, "w") as f:
        f.write(commit_hash)

    print(f"Checked out commit {commit_hash}")
def status():
    print("On branch master")

    # Show HEAD commit
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, "r") as f:
            head_commit = f.read().strip()
        if head_commit:
            print(f"HEAD commit: {head_commit}")
        else:
            print("No commits yet.")
    else:
        print("No commits yet.")

    # Show staged files
    print("\nChanges to be committed:")
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as idx:
            lines = idx.readlines()
        if lines:
            for line in lines:
                fname, h = line.strip().split()
                print(f"    {fname}")
        else:
            print("    (none)")
    else:
        print("    (none)")

    # Show unstaged changes
    print("\nChanges not staged for commit:")
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as idx:
            staged_files = [line.strip().split()[0] for line in idx.readlines()]
        unstaged = []
        for fname in staged_files:
            if os.path.exists(fname):
                with open(fname, "rb") as f:
                    content = f.read()
                blob_hash = Blob(fname).store()
                with open(os.path.join(OBJECTS_DIR, blob_hash), "rb") as b:
                    blob_content = b.read().split(b"\x00", 1)[1]
                if content != blob_content:
                    unstaged.append(fname)
        if unstaged:
            for file in unstaged:
                print(f"    {file}")
        else:
            print("    (none)")
    else:
        print("    (none)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args]")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        init()
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python main.py add <file1> [file2 ...]")
        else:
            add(sys.argv[2:])
    elif cmd == "commit":
        if len(sys.argv) < 3:
            print("Usage: python main.py commit <message>")
        else:
            message = " ".join(sys.argv[2:])
            commit(message)
    elif cmd == "log":
        log()
    elif cmd == "checkout":
        if len(sys.argv) < 3:
            print("Usage: python main.py checkout <commit_hash>")
        else:
            checkout(sys.argv[2])
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
