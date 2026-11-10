# 04 — Practise Git using your sensor project

Do the exercises in order. Use a disposable copy for the conflict and recovery
exercises. Your goal is to understand what you are saving, not to accumulate
commands or a large number of meaningless commits.

## A. Prove that generated results stay local

Start after your first commit, with `git status --short` empty. Run `python run.py`
twice. Inspect the files it creates and run:

```bash
git status --short
git status --ignored --short
git check-ignore -v output/summary.json
git ls-files data config checks
```

Expected: ordinary status stays empty; ignored output/caches may be shown by the
second command; the ignore diagnostic identifies `/output/`; the final command
lists tracked fixtures, the example configuration, and checks. [R07, R08, R27]

Explain why `data/tiny.csv` belongs in history but `output/summary.json` normally
does not. Do not describe an ignore rule as a backup or security policy.

## B. See that staging records a version, not a promise

Open `PROGRESS.md` and append a heading `## Staging experiment` and the sentence:

```text
First observation: I ran the example successfully.
```

Stage it, then open the file again and append:

```text
Second observation: generated output stayed outside Git.
```

Do not stage again yet. Compare:

```bash
git status --short
git diff -- PROGRESS.md
git diff --staged -- PROGRESS.md
```

You should see a staged addition and an unstaged addition. The second sentence
exists in your editor's file but is not in the selected next snapshot. Decide
that both observations belong together, stage the file again, and commit with a
message describing the experiment. [R05, R09]

Before your next exercise, get back to a clean tree. Write a two-sentence answer
explaining why saving, staging, and committing are different actions.

## C. Make one branch and a simple local merge

Start on clean `main` after your earlier commits:

```bash
git switch -c docs/git-notes
```

Create `docs/git_notes.md` with three short explanations in your own words:
what a measurement series is, where the configuration's relative paths start,
and why output is not shared. The filename is deliberately separate from these
supplied lesson files. Stage and commit it:

```bash
git add docs/git_notes.md
git diff --staged
git commit -m "Explain the project data and path conventions"
git switch main
```

Before merging, confirm that the new file is absent from `main`'s working copy.
Then:

```bash
git merge --ff-only docs/git-notes
git log --oneline --graph --all -6
git branch -d docs/git-notes
```

The note returns when its commit becomes part of `main`. You did not copy a
folder or paste the file manually. Explain why this merge needed no conflict
resolution. [R23, R25, R26]

## D. Make one real change with its check

Choose a task suited to your edition. In the student scaffold, finish one reader
or calibration task and its check. In the solved reference, **do not re-implement
an already completed task**: add a useful explanatory test or improve a specific
error message with a regression check.

For a small test-only example, inspect `calibration.calibrate_reading`. Create
`checks/test_calibration_example.py` containing:

```python
"""A numerical example that also checks that raw data is preserved."""
import unittest
from calibration import calibrate_reading


class CalibrationExample(unittest.TestCase):
    def test_scale_then_offset_without_changing_input(self):
        # This dictionary follows the common record contract.
        raw = {
            "time": "2026-10-24T12:00:00+00:00",
            "room": "laboratory",
            "sensor_id": "station-01",
            "metric": "temperature",
            "value": 20.0,
            "unit": "C",
        }
        # Keep a copy so the test can detect accidental input mutation.
        before = raw.copy()
        corrected = calibrate_reading(raw, scale=1.1, offset=-1.0)
        # Calibration is value * scale + offset: 20 * 1.1 - 1 = 21.
        self.assertAlmostEqual(corrected["value"], 21.0)
        self.assertEqual(raw, before)
        self.assertIsNot(corrected, raw)
```

Run it explicitly from the project root:

```bash
python -m unittest discover -s checks -p "test_calibration_example.py" -v
```

On the solved edition it should pass; on an unfinished starter it requires the
calibration task. Notice that this is an explanatory regression example, not a
newly discovered bug. Choose a short branch name, commit the file intentionally,
and explain its purpose to a partner. Do not add it twice just to increase a
count. A full suite with this extra check has one more test than the baseline.

## E. Resolve a controlled conflict without touching Python

Use a **disposable copy** with its own history. Begin on clean `main`; do not run
this exercise while merging another task. Keep this step local and do not push
its artificial commits into a team's real project.

Create `docs/merge_practice.txt` in your editor with this one line, ending with a
newline:

```text
Dashboard refresh interval: undecided.
```

Record the common starting point:

```bash
git add docs/merge_practice.txt
git commit -m "Add a harmless line for merge practice"
git switch -c practice/fast-refresh
```

On this branch replace the whole line with:

```text
Dashboard refresh interval: 1 second.
```

Then:

```bash
git add docs/merge_practice.txt
git commit -m "Propose a one-second refresh"
git switch main
```

On `main`, replace the original undecided line with:

```text
Dashboard refresh interval: 5 seconds.
```

Commit this competing decision, then merge:

```bash
git add docs/merge_practice.txt
git commit -m "Propose a five-second refresh"
git merge practice/fast-refresh
```

A content conflict is expected: two branches changed the same line differently.
Git stops for a decision. The program is not broken; this is a text exercise.
Inspect `git status` and the file. In the usual conflict display you will see
markers like:

```text
    <<<<<<< HEAD
    Dashboard refresh interval: 5 seconds.
    =======
    Dashboard refresh interval: 1 second.
    >>>>>>> practice/fast-refresh
```

The block is indented here only for display, so this guide itself is not mistaken
for an unresolved conflict by `git diff --check`. Real markers may start in the
first column of the conflicted file.

Your exact labels or extra base lines can differ with Git's conflict-display
settings. Here `HEAD` is your current `main`, not a universal synonym for the
correct answer. Read both proposals. Choose and explain a compromise:

```text
Dashboard refresh interval: 2 seconds, pending measurement.
```

Replace the marked block with that sentence, remove **all** conflict markers,
and finish the resolution:

```bash
git add docs/merge_practice.txt
git diff --staged --check
git commit -m "Resolve the refresh-interval discussion for the exercise"
git log --oneline --graph --all -8
```

This time the branches diverged; the result is a merge commit with two parents.
If instead you want to abandon the attempt **while the conflict is still in
progress**, `git merge --abort` cancels that merge. Start clean so that aborting
is not entangled with earlier uncommitted work. [R26]

Nothing here implements a dashboard or changes a configuration key: the sentence
is only a safe conflict example. Never insert unsupported keys into the strict
sensor configuration just to manufacture a conflict.

## F. Practise recovery on a disposable file

Still in the disposable repository, add another harmless sentence to
`docs/merge_practice.txt`, stage it, then use
`git restore --staged docs/merge_practice.txt`. Confirm that your edit remains in
the file. Inspect it and make a backup if you want to retain it. Finally use
`git restore -- docs/merge_practice.txt` to discard that deliberately unwanted
unstaged sentence. Verify a clean tree. Do not use your real coursework as the
first experiment with a discard operation. [R11]

As a separate exercise, add and commit a temporary sentence. With a clean tree
and that ordinary one-parent commit as your current `HEAD`, run
`git revert --no-edit HEAD`. Verify that the sentence is removed by a **new**
commit, while the earlier commit still appears in the log. Do not substitute a
merge commit for this exercise. [R22]

## G. Optional teamwork check

After the local exercises, use the shared-repository workflow. One person makes
a small improvement on a branch; another reviews it and runs the checks from a
fresh clone. Demonstrate that the clone has the small fixtures and example
configuration, can run the program, and does not contain anyone's previous
outputs, private configuration, or virtual environment.

## Record your evidence

In your own `PROGRESS.md`, record the actual commands/results, a short commit
history, and a paragraph explaining one mistake you corrected. Do not submit
passwords, tokens, private paths, or artificial screenshots of tests you did not
run. Your explanation matters more than having the same commit identifiers as
somebody else.

References for the command behaviour: [REFERENCES.md](REFERENCES.md).
