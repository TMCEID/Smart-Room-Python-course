# Validation of the Git teaching iteration

Checked on **4 November 2026** using **Python 3.13.5**, **Git 2.47.3**, and Linux.
This is a report of executed checks, not a promise of compatibility with every
Git configuration, operating system, host, or future project modification.

## Application behaviour remains unchanged

All **27 original files other than the README** were compared byte-for-byte with
`room_sensor_solved.zip` and were unchanged. This includes every Python module,
check, data fixture, and the default JSON configuration. Only the original README
received a short Git entry point and a corresponding wording adjustment.

The existing **76 application tests passed with no skips** from a fresh Git clone
through a temporary local bare remote. Both `python run.py` and
`python run_finite.py` ran in that clone. Their generated outputs and bytecode did
not dirty the tracked working tree.

```bash
python -m unittest discover -s checks -p "*.py" -v
```

The extra calibration test was extracted directly from the practice guide and
executed separately: **1 test passed**. Its sample record was also accepted by
the real record parser. It is an exercise in the guide, not an additional file
already inserted into your 76-test reference suite.

## Git workflow checks

**22 release scenarios passed.** They were performed in disposable folders, with
repository-local test identities and without modifying global Git settings:

1. 27 original files retained byte-for-byte; only original README amended.
2. Add-on contains no Python solutions/README replacement; no manifests or bundled .git.
3. New-repository detection, main initialisation and repository-local identity.
4. Both unmodified entry points run before staging.
5. Ignore rules exclude 10 generated/private paths but preserve all fixtures and shared settings.
6. Explicit personal configuration works without being staged.
7. Text attributes and actual CRLF-to-LF index normalisation.
8. Initial dry run and staging select exactly the delivered project, without local artifacts.
9. Before-first-commit unstage recipe preserves the working file.
10. Reviewed first commit has a clean working tree.
11. Both entry points keep Git status clean after running.
12. Staging exercise demonstrates independently staged and unstaged file versions.
13. Branch exercise, visible file changes, fast-forward merge and safe branch deletion.
14. Code example extracted from the guide runs and its sample record passes the real parser.
15. Controlled conflict reproduces as documented; abort returns to the clean pre-merge state.
16. Manual conflict resolution creates the intended two-parent merge commit.
17. Unstage, discard and revert exercises preserve the distinctions described in the guide.
18. Already-tracked output is removed from future snapshots, not deleted locally or from history.
19. Push/upstream/clone workflow works against a temporary local bare remote; personal files stay absent.
20. Fresh clone runs both entry points and all 76 existing tests with zero skips.
21. Fresh-clone application/test runs leave tracked files unchanged.
22. Two-clone branch sharing and fast-forward update work; host review UI is not simulated.

These release scenarios are separate from the 76 application tests. Your normal
unittest command does not secretly initialise a repository or make commits.
The temporary `.git` histories, fake private files, and artificial exercise
commits are not included in either download.

## Add-on tested against the student starter

The add-on was copied onto a clean extraction of
`room_sensor_backbone_annotation_fix.zip`. All **25 existing starter files**
remained byte-for-byte unchanged. The starter ran successfully, **12 baseline
checks passed**, and full discovery reported **20 intentionally skipped unfinished
exercise checks** in addition to those 12 passes. Those skips remain unfinished
student work, not completed solutions.

After initialisation and staging, the starter's source, sample data, configuration
and guides were included. Outputs and bytecode were excluded. The staged
whitespace/conflict-marker check passed.

## Archive and documentation checks

Both final ZIP files were extracted and checked. Dotfiles are present. Neither
archive contains `.git`, runtime output, Python caches, a virtual environment,
a package manifest, a credential, or a configured remote. Relative Markdown
links in the new materials resolve within their intended layout. The complete
archive was staged cleanly, and its 76 tests and both entry points were rerun
from the final extracted copy.

## Important limits

Remote operations used a real **local bare repository**, not GitHub or an
institutional server. Push, upstream configuration, clone, branch sharing,
fetching and fast-forward updates were exercised. No account was created, no
online upload occurred, and authentication, permissions, branch-protection rules
and the host's review interface were **not** exercised.

Command execution was on Linux. CRLF input normalisation was tested with an
explicit fixture, but Windows/PowerShell and macOS were not run. Git 2.28 is the
documented minimum for these examples, not a separately executed runtime here.
The Python compatibility limits remain those of the prior reference solution.

Root-level `VALIDATION.md` is retained as the earlier application-validation
record. Its description of the pre-Git stage is historical; this document covers
the new Git materials. No CI, automatic hooks, packaging, browser, or live sensor
processing was added in this iteration.
