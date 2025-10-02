# miniGit
miniGit is a simplified version control system implemented in Python, designed to mimic the core functionality of Git.  
It allows you to initialize a repository, add files, commit changes, view commit history, checkout old commits, and check the status of your repository.
This project is a self-made implementation for educational purposes demonstrating how version control systems work under the hood.
## Project Structure
## Features

- Initialize a repository (`init`)
- Add files to staging area (`add <filename>`)
- Commit changes with a message (`commit "message"`)
- View commit history (`log`)
- Checkout previous commits (`checkout <commit_hash>`)
- Check repository status (`status`)

## How to Run miniGit

1. **Clone or download this repository**
    ```bash
    git clone https://github.com/yourusername/miniGit.git
    cd miniGit
    ```

2. **Initialize your repository**
    ```bash
    python main.py init
    ```

3. **Add files to staging area**
    ```bash
    python main.py add <filename>
    ```
    Example:
    ```bash
    python main.py add hello.txt
    ```

4. **Commit your changes**
    ```bash
    python main.py commit "Your commit message"
    ```

5. **View commit history**
    ```bash
    python main.py log
    ```

6. **Checkout a previous commit**
    ```bash
    python main.py checkout <commit_hash>
    ```

7. **Check repository status**
    ```bash
    python main.py status
    ```

---

## 📌 Example Workflow

```bash
python main.py init
echo "Hello miniGit" > hello.txt
python main.py add hello.txt
python main.py commit "First commit"
echo "Hello again" >> hello.txt
python main.py add hello.txt
python main.py commit "Second commit"
python main.py log
python main.py status
python main.py checkout <first_commit_hash>