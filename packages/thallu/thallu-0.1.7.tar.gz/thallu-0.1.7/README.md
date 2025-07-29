# `thallu` ⚔️

`thallu` is a **lightweight yet powerful Command Line Interface (CLI) tool** designed to automate and streamline your Git workflow, allowing you to focus on development rather than repetitive Git commands.

---

## 🚀 Features

`thallu` simplifies common Git operations, offering a comprehensive set of features:

* **Repository Initialization**: Automatically initializes a Git repository if one doesn't exist.
* **Remote Management**: Adds and validates the `origin` Git remote using configurations from `plan.txt`.
* **Staging**: Stages all modified files with a single command.
* **Interactive Commits**: Prompts for commit messages, ensuring clear and descriptive commits.
* **Branch Renaming**: Automatically renames the `master` branch to `main` for modern Git workflows.
* **Effortless Pushing**: Pushes changes to the `origin` remote.
* **Branch Creation**: Quickly create and checkout new branches.
* **Flexible Branch Switching**: Switch between branches interactively or directly by providing the branch name.
* **Streamlined Merging**: Merge multiple branches into your current branch, either interactively or by specifying branch names.
* **Efficient Branch Deletion**: Delete branches interactively or by specifying the branch name.
* **Configuration Validation**: Validates the `plan.txt` configuration file to ensure correct setup.

---

## 📦 Installation

To install `thallu`, simply use pip:

```bash
pip install thallu
```

---

## ⚙️ Usage

`thallu` provides various commands to manage your Git workflow:

### Initial Setup and Workflow (Init, Commit, Push)

This command is safe for both fresh and existing repositories, handling initialization, staging, committing, and pushing.

```bash
thallu
```

### Update Only (Stage, Commit, Push)

Use this command to quickly stage, commit, and push changes without re-initializing the repository.

```bash
thallu -u
```

### Branch Management

`thallu` offers robust branch management capabilities:

* **List all branches**:
    ```bash
    thallu -b
    ```
* **Create a new branch**:
    ```bash
    thallu -nb
    ```
* **Switch branches (interactive)**:
    ```bash
    thallu -sb
    ```
* **Switch to a specific branch**:
    ```bash
    thallu -sb branch_name
    ```
* **Merge branches interactively**:
    ```bash
    thallu -m
    ```
* **Merge specific branches**:
    ```bash
    thallu -m feature1 feature2
    ```
* **Delete branches (interactive)**:
    ```bash
    thallu -d
    ```
* **Delete a specific branch**:
    ```bash
    thallu -d branch_name
    ```

---

## 📁 Requirements

To use `thallu`, ensure you meet the following requirements:

* **Python**: Version **3.7** or higher.
* **Git**: Version **2.23** or higher.
    * *Note*: Git version 2.23+ is required for `git switch` and `git restore` commands, which `thallu` leverages. You can check your Git version using:
        ```bash
        git --version
        ```
* **`plan.txt` configuration file**: A file named `plan.txt` must be present in your project's root directory with the following structure:

    ```python
    username = "your-github-username"
    repo = "your-repo-name"
    ```

---

## 🧪 Example Output

Here's an example of the output you might see when running `thallu`:

```bash
✅ Git repo already initialized.
🔗 Remote 'origin' already exists.
➕ Staged all files.
💬 Enter commit message: initial setup
📦 Commit done: initial setup
🌿 Renamed branch to 'main'.
🚀 Pushed to origin/main.
```

---


## Current Commands
![thallu Command Reference](https://github.com/Naveensivam03/thallu/blob/main/command.png?raw=true)

## 🛣️ Roadmap

We have exciting plans for future enhancements to `thallu`:

* **Project Type Auto-detection**: Automatically detect project types (e.g., Python, Node.js) for tailored workflows.
* **GPG Signing Support**: Integrate GPG signing for enhanced commit security.
* **GitHub Releases Integration**: Streamline the creation and management of GitHub releases.
* **Commit Message Presets**: Provide pre-defined commit message templates for common scenarios.
* **CI Hooks and Test Coverage**: Add support for Continuous Integration (CI) hooks and improve test coverage.
* **Public/Private Repo Detection**: Intelligent detection of public and private repositories.

---

## 🤝 Contributing

Contributions are highly welcome! If you'd like to contribute, please follow these steps:

1.  Fork the `thallu` repository.
2.  Create a new feature branch for your changes.
3.  Submit a Pull Request (PR) with a clear and concise description of your enhancements.

---

## 📜 License

© Naveensivam03

`thallu` was built for developers seeking to eliminate repetitive Git tasks and enhance their productivity.