# study-quiz-cli
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/DavidTJGriffin/study-quiz-game)
[![PyPI version](https://badge.fury.io/py/study-quiz-cli.svg)](https://pypi.org/project/study-quiz-cli/)

A Python CLI tool that lets you create and play your own multiple-choice study quizzes in the terminal. Designed for students who want to test themselves with custom questions.

---

## Installation

```bash
pipx install study-quiz-cli
```

> ⚠️ If `quizcli` isn’t recognized after install, run:

```bash
pipx ensurepath
exec $SHELL  # or restart your terminal
```

---

## Usage

```bash
quizcli
```

When you run it, you'll:

1. Create your own quiz questions in this format:  
   ```
   What is the capital of Japan?|A. Beijing| B. Seoul|C. Tokyo|D. Bangkok|C
   ```

2. Answer the questions interactively  
3. Get a final score (5 points per correct answer)  
4. Choose to replay with the same or new questions

---

## Tech Stack

- Python 3.12+
- Poetry
- CLI entrypoint via `pyproject.toml`
- File I/O with `quiz-questions.txt` (saved locally)

---

## License

This project is licensed under the MIT License.
