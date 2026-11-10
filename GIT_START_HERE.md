# Your next step: give your project a history

You already have a folder containing a sensor-data program. In this iteration,
keep that program as it is. Your new job is to record understandable changes and
learn how to share them without copying whole folders between people.

**Start locally. You do not need a GitHub account for your first lesson.**

## Choose the correct download

**`room_sensor_git_files.zip` is the add-on for your own work.** Copy its contents
into your existing project, beside `run.py`. Include the two dotfiles,
`.gitignore` and `.gitattributes`. Merge the `docs` folder; do not replace an
existing one wholesale. Compare files first if you already have names in common.
This archive contains no Python solutions and does not replace your README.

**`room_sensor_git_ready.zip` is a complete reference copy.** It contains the
previously solved project plus these Git materials. Keep it beside your own
attempt: it includes completed Python exercises. The Python implementation,
fixtures, tests, and default configuration have not been changed for this step.

Neither archive contains a `.git` directory or a pre-made commit history.
You create your own history under your own identity. Nothing is uploaded for you.

## Your first sitting

Open a terminal in the folder containing `run.py`. Read
[the local-history walkthrough](docs/git/02_local_history.md) and follow it in
order. It explains the commands rather than asking you to run an opaque setup
script. Begin by checking that Git is installed:

```bash
git --version
python --version
```

The command examples use Git 2.28 or newer. Use the Python interpreter that
already runs your project; substitute `python3` or `py -3` where needed.
There are no new Python dependencies to install.

Your first milestone is a reviewed local commit, a second small change, and a
clean working directory. Do not start with remote accounts or merge conflicts.

## Follow the material in small stages

| Read | What you will do |
|---|---|
| [01 — Files and boundaries](docs/git/01_files.md) | Decide what belongs in history and understand each added file. |
| [02 — Local history](docs/git/02_local_history.md) | Initialise, inspect, stage, commit, compare, and correct mistakes. |
| [03 — Sharing and teamwork](docs/git/03_teamwork.md) | Add a remote only when ready; use short branches and review. |
| [04 — Practice](docs/git/04_practice.md) | Complete project-specific exercises, including a controlled conflict. |
| [Command reference](docs/git/COMMANDS.md) | Find a command after you understand the operation. |
| [Contributing](CONTRIBUTING.md) | Agree on how your team works. |

You can finish the local-history lesson without reading the later sections.
The practice sheet explicitly separates the starter from the solved edition.

## Keep this step small

There is still no package manifest, installation command, CI workflow, automatic
Git hook, browser, or live sensor service. The existing tests run manually.
We have not selected a licence, repository owner, remote address, or public
visibility on your behalf. Confirm those choices with your course team before
publishing. Use private sharing for the classroom until publication is agreed.

To add an entry to your own README, use this sentence:

> Start the Git iteration with [GIT_START_HERE.md](GIT_START_HERE.md).

The complete reference already contains this link. Technical references are in
[REFERENCES.md](docs/git/REFERENCES.md); validation and its limits are in
[VALIDATION.md](docs/git/VALIDATION.md).
