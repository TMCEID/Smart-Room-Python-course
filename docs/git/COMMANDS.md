# Command reference — use after the walkthrough

Run commands from the project root. Replace all uppercase placeholders and
identity examples. `REMOTE_URL` is your host's repository address; `COMMIT_ID`
is an inspected commit identifier. These are not working values.

| Intention | Command | Check first |
|---|---|---|
| Check Git | `git --version` | Git must be installed. |
| Check repository root | `git rev-parse --show-toplevel` | A failure is normal before initialisation. |
| Start local history | `git init -b main` | New folder, not inside another project repository. |
| Set your name here | `git config --local user.name "Your Name"` | Repository exists; replace the name. |
| Set your commit email here | `git config --local user.email "you@example.org"` | Use an approved address, not a password. |
| Inspect changes | `git status --short` | Include `--ignored` to see ignored paths. |
| Read unstaged tracked edits | `git diff` | Untracked files' contents are not shown. |
| Stage one file | `git add PROGRESS.md` | Save and review that file first. |
| Read the next snapshot's changes | `git diff --staged` | Review before every commit. |
| Check staged whitespace | `git diff --staged --check` | This does not run Python tests. |
| Record the snapshot | `git commit -m "Describe the change"` | Appropriate checks have run. |
| View short history | `git log --oneline --graph --all -8` | Press `q` if a pager opens. |
| Explain an ignore match | `git check-ignore -v output/summary.json` | No match gives exit code 1. |
| Inspect text attributes | `git check-attr text eol -- run.py` | Expected here: set, lf. |
| Unstage an edit, keep the file | `git restore --staged PROGRESS.md` | At least one commit exists. |
| Create/select a branch | `git switch -c docs/git-notes` | Start clean, from the intended base. |
| Return to main | `git switch main` | Finish current work first. |
| Simple local integration | `git merge --ff-only docs/git-notes` | Current branch is main; no divergence. |
| Delete an integrated local branch | `git branch -d docs/git-notes` | Switch away; integration confirmed. |
| Inspect remotes | `git remote -v` | Do not share output containing credentials. |
| Add a sharing destination | `git remote add origin "REMOTE_URL"` | Remote exists; destination checked. |
| Share committed main | `git push -u origin main` | Authentication and sharing approval. |
| Start a teammate's working copy | `git clone "REMOTE_URL" room-sensor-team` | Run from the parent of a new folder. |
| Update local main simply | `git pull --ff-only origin main` | On clean main; remote configured. |
| Cancel an unresolved merge | `git merge --abort` | A merge is actually in progress. |
| Reverse an ordinary commit | `git revert --no-edit COMMIT_ID` | Clean tree; inspect the commit first. |

## Destructive or surprising operations are not shortcuts

`git restore -- FILE` overwrites working-copy content with its staged version.
Do not confuse it with `git restore --staged FILE`, which keeps your edits.
Read the recovery lesson and practise on a disposable file first. Do not use
force push, `reset --hard`, or `clean -fd` to make an unexplained status disappear.

## The Python checks remain separate

```bash
# Starter baseline:
python -m unittest discover -s checks -p "test_*.py" -v

# Completed solution, including exercise checks:
python -m unittest discover -s checks -p "*.py" -v
```

Commands and cautions are explained in [02_local_history.md](02_local_history.md)
and [03_teamwork.md](03_teamwork.md). Sources: [REFERENCES.md](REFERENCES.md).
