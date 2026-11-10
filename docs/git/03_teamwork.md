# 03 — Share the project without exchanging ZIP files

Read this after creating a local history. Git is the version-control tool;
a hosting service such as GitHub or an institutional server is a place to share
repositories. You can use local commits and branches without an account. [R03]

## 1. Choose one shared starting history

For a team repository, one person creates the initial repository and shares it.
Everyone else clones that repository. Do not have every teammate initialise an
independent copy of the same ZIP and then try to combine unrelated histories.

Agree on access, who reviews changes, and whether your course uses GitHub or an
institutional host. Do not publish solved coursework, personal information, or
real sensor data unless sharing has been agreed. These files do not set any
account permissions or create a remote repository for you.

## 2. Connect an existing local history to an empty remote

On the chosen hosting service, create an **empty** repository. Because you already
have your local files and first commit, do not ask the service to generate another
README, ignore file, or licence in a separate initial commit. GitHub explicitly
recommends this when importing existing work. [R17]

Copy the remote URL supplied by your service. In the following command,
`REMOTE_URL` is a placeholder: replace it with that complete URL, keeping quotes.

```bash
git remote add origin "REMOTE_URL"
git remote -v
git push -u origin main
```

`origin` is a conventional local name for the remote. Adding it stores an
address; it does not upload files. `push` sends the committed history, and `-u`
sets the upstream relationship for this local branch. Uncommitted edits are not
included. [R14, R15]

Inspect the address before pushing. If `origin` already exists, inspect it rather
than adding a second one. Use `git remote set-url origin "REMOTE_URL"` only after
confirming that you intend to change that destination. [R14]

Authenticate using the method supported by your host. For GitHub, an account
password is not the credential for HTTPS Git operations: use an approved
credential-manager/token flow, or an SSH key. Never paste tokens into a remote
URL, Python file, configuration example, screenshot, or commit message. Your
`user.name`/`user.email` settings are not authentication credentials. [R18]

A private repository still requires careful data handling; it is not a reason to
commit passwords. No live push or login was performed while preparing this kit.

## 3. Your teammate clones; they do not initialise again

From the **parent directory** where a fresh project folder should be created:

```bash
git clone "REMOTE_URL" room-sensor-team
cd room-sensor-team
git config --local user.name "Your Name"
git config --local user.email "your-approved-commit-address@example.org"
python run.py
```

Again, replace the URL and identity placeholders. Clone creates a new local
working copy and repository; do not clone into your existing coursework folder
or run `git init` afterwards. [R13]

There should be shared data and example configuration, but no old output or
virtual environment. Running the example will create output locally. Test the
clone using the command appropriate to the starter or solved edition.

## 4. Use a short branch for one change

With no uncommitted work, prepare a new task:

```bash
git switch main
git pull --ff-only origin main
git switch -c docs/input-contract
```

`switch -c` creates and selects a branch. A branch is a movable name in the
history, not another copied directory. Your working files reflect the branch
you select. [R23]

`pull --ff-only` fetches and updates only when the branch can move forward
without creating a merge. If it refuses because histories diverged, inspect
them and ask your teammate; do not use force to conceal the disagreement. [R16]

Make one genuine improvement to `DATA_CONTRACT.md`, for example clarifying the
existing room/sensor/metric grouping rule. Do not change the actual contract
accidentally. Then:

```bash
git diff -- DATA_CONTRACT.md
git add DATA_CONTRACT.md
git diff --staged
git commit -m "Clarify the identity of a measurement series"
git push -u origin docs/input-contract
```

For a code task, replace the example path with the specific code and test files
that belong to it. Run the checks before requesting review.

## 5. Request a review, then merge

On GitHub, open a pull request from your branch into `main`. It is a proposal
for discussion and review before integration; a push alone does not create that
review request. [R24]

Describe the problem, the change, your test command/result, and any remaining
limits. Ask a teammate to inspect the actual diff. They should be able to explain
why the change belongs in the project. Correct feedback with small follow-up
commits on the same branch.

After approval, merge through the agreed host workflow. For this first lesson,
using a merge commit preserves the branch commits explicitly. The available
merge methods depend on repository settings; do not assume every button is
available or that an approval rule is automatically enforced.

Back in your local working copy:

```bash
git switch main
git pull --ff-only origin main
python -m unittest discover -s checks -p "*.py" -v
```

The final test command is for the completed edition; use the starter baseline
command when you are still doing the initial assignment.

When the branch's commits are integrated, delete the local branch with
`git branch -d docs/input-contract`. If this refuses after a squash-style merge,
do not immediately use `-D`: inspect the host and compare the resulting content
first. Deleting the local branch does not delete a remote branch. [R25]

## 6. Practise a local merge before learning the hosting interface

The practice sheet has a completely offline branch exercise. After a clean,
completed task branch with no competing edits, you can integrate it locally:

```bash
git switch main
git merge --ff-only docs/git-notes
```

A fast-forward merge moves `main` to the existing branch tip; it need not produce
a new merge commit. Diverging histories need a different integration step, which
the controlled conflict exercise explains. [R26]

Do not also merge locally if your team has agreed to review and merge on the
server first. These are two learning routes, not steps to perform twice.

## 7. What your team should be able to explain

A commit is a local checkpoint; a push shares committed history with a remote;
a clone starts a new working copy of a shared history; a branch isolates a line
of development; and a review request invites a decision about integration.
Read the command references for the exact behaviour of each operation.

For your first team task, keep `main` runnable, choose one reviewer, and avoid
complicated branch schemes. CI and protected-branch policies can be added in a
later iteration once the underlying operations make sense.

Sources and installation/authentication references: [REFERENCES.md](REFERENCES.md).
