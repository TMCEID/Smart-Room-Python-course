# 02 — Build a history on your own computer

Your goal is to answer three questions: what changed, why did it change, and
which version did you test? Keep this first lesson local. Publishing is a
separate action that comes later.

## 1. Locate your project and check your tools

Open a terminal inside the folder containing `run.py`, `data`, and `checks`.
Use your file manager's “open terminal here” action or `cd` into that folder.
Run:

```bash
git --version
python --version
```

These notes use Git 2.28 or newer, including `git init -b main`. If Git is
missing, install the distribution for your platform from the official Git
installation page, then reopen your terminal. [R03, R20]

Use `python3` or `py -3` instead of `python` when that is the interpreter you
already use. Git does not solve Python-version mismatches. Refer to the project's
compatibility notes before blaming a failed import on version control.

Run `python run.py` once. In the solved edition also try `python run_finite.py`.
You should recognise the program's output before adding a new tool around it.

## 2. Check whether you already have a repository

```bash
git rev-parse --show-toplevel
```

For a new extracted folder, “not a git repository” is expected. If Git prints a
path, inspect it: is that the intended project root, or a parent folder already
tracked by another project? Do not create a nested repository by accident.
If your project already has its own repository, skip initialisation and the
first-commit recipe; add these files as an ordinary later change. [R21]

For a new project folder only:

```bash
# Create local history machinery; do not contact a server.
git init -b main
```

The branch is explicitly called `main`, so the lesson does not depend on a
machine's default branch-name setting. [R03]

## 3. Set the identity that will appear in your commits

Replace both placeholder values before running:

```bash
git config --local user.name "Your Name"
git config --local user.email "your-approved-commit-address@example.org"
```

The local scope affects this repository, not every other project on your
computer. This identity is commit authorship information, not a login to GitHub
or your institution's Git server. Use an address you are comfortable recording
in shared history; a hosting provider's privacy address is an option when
configured for your account. [R04, R18]

Check the values:

```bash
git config --local --get user.name
git config --local --get user.email
```

Do not use your teammate's identity or the placeholders above unchanged.

## 4. Understand the three places you will inspect

```text
working files              staging area                  local history
what your editor changes   next snapshot you selected    committed snapshots
          -- git add -->                   -- git commit -->
```

When you save a file, you change the working copy. `git add` selects the file's
current contents for the next commit. Editing it again does not update that
selection automatically: you would need to stage the new contents too. [R05]

A commit records the staged snapshot with a message and history information.
It does not upload your project. [R06]

Before staging, look at:

```bash
git status --short
git status --ignored --short
git add --dry-run .
```

Here `--dry-run` previews what would be added without staging it. New files
usually appear with `??`; ignored paths appear with `!!` when requested.
Tracked changes use two status columns for the index and working copy. [R05, R07]

Confirm that the Python files, guides, fixture data, and `config/example.json`
will be included. `output/` and Python caches should be ignored. When in doubt:

```bash
git check-ignore -v output/summary.json
git check-ignore -v config/local.json
git check-ignore -v data/tiny.csv
```

The first two should identify an ignore rule, even if the paths do not yet
exist. The fixture should produce no matching rule. No-match exit status 1 is
normal for `check-ignore`; it does not mean your data is broken. [R08]

## 5. Make your first reviewed commit

After inspecting the preview:

```bash
git add .
git diff --staged --stat
git diff --staged
git diff --staged --check
```

The broad `git add .` is deliberate for the **initial, reviewed import only**.
Later, use explicit filenames for one logical change. `--staged` compares your
selected snapshot with the preceding commit (or the empty starting state).
A plain `git diff` compares unstaged tracked changes with the staging area;
it does not show the contents of untracked files. [R05, R09]

Large output may open in a pager. Press `q` to leave the pager; you are not
closing Git or deleting the output.

Run the checks appropriate to your edition:

```bash
# Original student starter: supplied working behaviour.
python -m unittest discover -s checks -p "test_*.py" -v

# Completed reference: all checks, including exercise checks.
python -m unittest discover -s checks -p "*.py" -v
```

The complete reference has 76 passing checks with no skips. The original starter
has 12 baseline checks; optional unfinished-task checks may skip. Never describe
a skipped exercise as implemented. If you changed the project, your test totals
may differ: record your actual result.

Now commit and inspect:

```bash
git commit -m "Start the room-sensor project with sample data and checks"
git status
git log --oneline -3
```

You should see the new commit and a clean working tree. Your commit identifier
will differ from everyone else's. `git log --oneline` is a compact view, not a
substitute for meaningful messages. [R06, R10]

**Checkpoint:** run the program and checks again. `git status --short` should
stay empty because the generated outputs and caches are ignored. If it is not
empty, inspect the listed files rather than committing them automatically.

## 6. Make a small second commit

Open `PROGRESS.md` and add a short `## Git practice` section. Write which program
and checks you ran. Do not claim an exercise is completed unless it really is.

```bash
git diff -- PROGRESS.md
git add PROGRESS.md
git diff --staged -- PROGRESS.md
git commit -m "Record the initial test commands and results"
git log --oneline -3
```

Now you have a beginning and an understandable next step, rather than one
unexplained upload. Try stating in one sentence why the second commit exists.

## 7. Correct mistakes without guessing

### You staged a file but want to keep editing it

After you have at least one commit:

```bash
git restore --staged PROGRESS.md
```

This removes that file's changes from the next-commit selection while keeping
your edited working file. **Before the very first commit**, `HEAD` does not yet
exist: for a newly added file, `git rm --cached -- PROGRESS.md` removes it from
the index but keeps the local file. Re-stage it when ready. [R11, R12]

### You want to discard an uncommitted edit

First inspect `git diff -- PROGRESS.md` and `git diff --staged -- PROGRESS.md`.
Copy anything you need to keep outside the project. When the staged comparison
is empty and you genuinely want to lose the unstaged edit:

```bash
git restore -- PROGRESS.md
```

**This overwrites the working file with its staged version.** It is not the same
as unstaging. Git may not be able to recover text that was never committed.
Practise only on the disposable exercise file described in the practice sheet.
[R11]

### You want to undo an already committed change

With a clean tree, inspect the history and identify the specific ordinary,
non-merge commit. The following is a template; replace `COMMIT_ID`:

```bash
git revert --no-edit COMMIT_ID
```

This creates a new reversing commit; it does not erase the old one. Conflicts
are possible if later work overlaps. Stop and inspect `git status` rather than
running unrelated commands. For an unresolved revert, `git revert --abort`
cancels that in-progress operation. [R22]

Do not learn recovery by trying `reset --hard`, force pushes, or mass deletion on
your real coursework. Those are not needed for this lesson.

### A generated file is already tracked

Adding an ignore rule alone does not untrack it. For a non-sensitive generated
file whose local version you want to keep, first finish other staged work, then:

```bash
git rm --cached -- output/summary.json
git add .gitignore
git diff --staged
git commit -m "Stop tracking generated summary output"
```

This example assumes that exact path is tracked. It leaves your local copy in
place but stages its removal from future snapshots. Existing commits still
contain it. Teammates updating to the removal commit may lose their tracked
copy, so agree the change first and let them back it up if needed. [R01, R12]

For a committed password or token, stop and revoke/rotate it first. Merely
removing the current file does not remove the secret from history or copies.
Tell your team and follow the hosting provider's documented clean-up procedure;
do not improvise a history rewrite. [R19]

## 8. Know when to stop

You have completed this lesson when you can show two purposeful commits,
explain working files versus staging versus history, and run the program without
creating new tracked results. Keep remote hosting for the next session.

Official command references: [REFERENCES.md](REFERENCES.md).
