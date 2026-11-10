# 01 — Which files belong in your repository?

Your repository should let a teammate understand your program, run the small
example, and reproduce the checks. It is not a copy of every file your computer
happens to create while you work.

## The two files Git actually reads

### `.gitignore`: keep generated and personal files out of routine staging

Open the supplied file. Each group of patterns has a comment explaining its
purpose. A trailing slash denotes a directory; a leading slash anchors a pattern
to this project's root. Patterns such as `*.log` can match at multiple depths.
Ignored **untracked** files are normally omitted by `git add .`. Previously
tracked files are not removed from history by an ignore rule. [R01]

For our project, the important decision is not to ignore an entire file format:

| Path | Track it? | Why in this project? |
|---|---|---|
| `readers.py`, `analysis.py`, other Python modules | Yes | They define the behaviour you are developing. |
| `checks/` | Yes | A teammate should be able to run the same checks. |
| `data/tiny.csv` | Yes | A deliberately small, shared hand-checking example. |
| `data/readings.csv`, `.json`, `.jsonl` | Yes | Equivalent fixtures for testing the readers. |
| `data/broken.csv` | Yes | A deliberate error fixture, not accidental rubbish. |
| `config/example.json` | Yes | Shared settings that work after a fresh clone. |
| `output/` | No | Reproducible results and operational logs. |
| `__pycache__/`, `.venv/` | No | Computer-generated or machine-specific files. |
| `config/local.json`, `config/*.local.json` | No | Optional personal settings, often containing local paths. |
| `data/private/`, `.env`, `.env.*` | No | Reserved local locations; not a permission system. |
| Markdown guides | Yes | Instructions and design decisions are part of your work. |

Do not add `*.csv` or `*.json` to the ignore file: those rules would also hide our
shared fixtures or configuration. If you intentionally need a new reference
result, store a small reviewed fixture outside `output/`, not a full run dump.

**Ignoring is not security.** It is still possible to stage ignored files
explicitly, and a secret inside a tracked Python file is not protected. Review
what you stage. A secret already committed needs a separate response; see the
recovery section of the local-history guide. [R01, R19]

### `.gitattributes`: agree on how text is stored and checked out

Windows and Unix-like systems can use different newline encodings. For the
project's Python, Markdown, CSV and JSON text, the supplied rules select LF.
Other file types use automatic text detection. The purpose is to avoid changes
that appear to replace every line merely because a tool changed newlines. [R02]

The file does not decide which files to track, run a formatter, or convert a
file's character encoding. Keep using UTF-8 when saving the supplied text files.
Git processes attributes during operations such as staging and checkout; adding
the file does not instantly rewrite every open file in your editor. [R02]

Inspect the settings after initialising the repository:

```bash
git check-attr text eol -- run.py config/example.json data/tiny.csv
```

For these paths, expect `text: set` and `eol: lf`. [R28] For a **new** repository, stage
normally. For an **existing** repository with inconsistent newlines, first finish
unrelated changes, make a backup, and agree a separate normalisation commit.
Only then consider `git add --renormalize .`, inspect the staged diff, and commit
that change on its own. Do not run it blindly in a mixed working tree. [R02]

## The other new files are for you

| File | Its role |
|---|---|
| `GIT_START_HERE.md` | Entry point and reading order; works with either edition. |
| `CONTRIBUTING.md` | Team agreement on small changes, tests, and review. |
| `docs/git/01_files.md` | This explanation of project boundaries. |
| `docs/git/02_local_history.md` | Your first local history and safe recovery practice. |
| `docs/git/03_teamwork.md` | Remotes, branches, and a lightweight team workflow. |
| `docs/git/04_practice.md` | Exercises that use the sensor project, not unrelated toys. |
| `docs/git/COMMANDS.md` | A compact command lookup with preconditions. |
| `docs/git/REFERENCES.md` | Official sources for Git and GitHub behaviour. |
| `docs/git/VALIDATION.md` | What was actually executed while preparing these materials. |

The full reference also adds a short Git pointer to the existing `README.md`.
The add-on deliberately does not replace that file or any of your Python code.

## What is deliberately not supplied

A `.git` directory is created by `git init` or `git clone`; it holds the local
repository machinery. Do not make one manually, paste one from a teammate, or
place one inside `data/`. [R03, R13]

There is no `.gitkeep` in `output/`: our program already creates its output
directories. A fresh clone does not need runtime results. There is no personal
`.gitconfig` either: set your identity with Git commands on your own machine.

No `pyproject.toml`, `setup.py`, `requirements.txt`, CI YAML, or Git hook is
required for this step. The program uses the standard library. No licence is
selected for you; agree redistribution terms before a public release. No remote
URL or credentials have been embedded in the files.

## Your private configuration is explicit, not automatic

In the **completed configuration extension**, copy `config/example.json` to
`config/local.json` using your editor or file manager. Keep it in the same folder
so the relative-path convention remains correct. Change only your local copy,
then run:

```bash
python run.py config/local.json
```

This is a full configuration file, not an overlay. The program does not
implicitly search for `local.json`, load `.env`, or merge settings. In the
original starter, configuration loading is still a student task; do not expect
this command to activate functionality you have not implemented.

Use [REFERENCES.md](REFERENCES.md) for the numbered sources.
