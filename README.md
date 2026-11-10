# Your room-sensor project — completed reference solution

> **Git iteration:** start with [GIT_START_HERE.md](GIT_START_HERE.md).
> This copy adds Git settings and student-facing guides; the Python code is
> unchanged. No `.git` history or remote is bundled. For your own unfinished
> project, use the separate Git-files add-on instead of replacing your code.

This is the solved companion to **room_sensor_backbone_annotation_fix**. All tasks
from the finite-data assignment and Extension 1 are implemented. The small folder
layout, function names and data contract are retained, so you can compare one
function at a time with your own work.

This is still a folder of Python modules, **not an installable distribution**.
There is no `pyproject.toml`, manifest, setup command, pre-initialised Git history, web server,
browser application, database, asynchronous collector or metaprogramming framework.
You need only Python's standard library. No `pip install` command is needed.

**Keep your own attempt in a separate folder.** Extract this reference next to it;
do not overwrite your unfinished work just to try the solution.

## 1. Choose the stage you want to study

Open a terminal inside this extracted folder. Start with the completed finite
assignment, whose settings are ordinary Python variables:

```bash
python run_finite.py
```

Then try the completed configuration extension:

```bash
python run.py
```

The second command reads `config/example.json`. You can also choose a file explicitly:

```bash
python run.py config/example.json
```

On systems where your interpreter is called `python3`, use that name instead.
On Windows, `py -3 run.py` selects an installed Python 3 interpreter.
The `Optional` / `Union` annotation fix is retained. See `COMPATIBILITY.md` for
exactly which version was executed and which checks were syntax-only.

Both stages use the larger 36-record fixture, select six laboratory temperatures,
and apply scale 1.02 and offset -0.4. Their selected mean is approximately **21.02 C**.
Both print a `Calibrated summary:` line followed by a dictionary with count, mean,
minimum, maximum, median and sample standard deviation. Float display can include
extra digits; compare numerical values with a tolerance.

The raw laboratory-temperature mean remains **21.0 C**. The source files are not
changed. The tiny file is still available for hand calculations and small tests.

## 2. Find the results

| Command | New files, created when you run it |
|---|---|
| `python run_finite.py` | `output/finite/calibrated.csv`, `calibrated.jsonl`, `summary.json`, `run.log` |
| `python run.py` | `output/calibrated.csv`, `output/summary.json`, `output/run.log` |

`summary.json` contains the selected result, its identity/unit, the calibration
settings, the raw-data exploration report, and six **separate raw-series summaries**.
Those raw summaries have not been calibrated. Do not confuse them with the
selected calibrated summary near the top of the report.

The configured run always saves processed records as CSV, as specified in X4.
The JSON Lines writer is exercised by `run_finite.py` and by the tests; input
format selection does not change the configured output format.

Snapshots replace earlier snapshots. Logs append to earlier messages. A second
run does not duplicate measurement rows. Stop reading on the first invalid
measurement; do not quietly analyse only the valid prefix.

## 3. Use the two entry points as successive versions, not two applications

`run_finite.py` shows the first assignment in full:

```text
visible Python settings
    -> configure logging
    -> read and explore raw data
    -> select one series
    -> calibrate into new records
    -> calculate statistics
    -> save CSV, JSON Lines and summary JSON
```

`run.py` shows how that same work evolves in Extension 1:

```text
load/validate JSON settings once
    -> resolve paths and prevent collisions
    -> configure logging
    -> read and explore raw data
    -> call the pure process_readings function
    -> save CSV and summary JSON
```

There is deliberately some repetition in the entry points: compare the visible
steps directly rather than chase a new orchestration framework. Both use the
same readers, calibration, analysis and storage functions.

## 4. Read the code in this order

| File | What you should look for |
|---|---|
| `run_finite.py` | The first completed sequence, task I1 |
| `records.py` | The unchanged common parser and measurement contract |
| `readers.py` | R1/R2: JSON and JSON Lines alongside the original CSV example |
| `calibration.py` | C1: copy a record rather than change the raw dictionary |
| `analysis.py` | E1/S1/S2: exploration and separate physical-series statistics |
| `storage.py` | W1/W2: finite snapshot writers |
| `logging_service.py` | L1: console plus append-only file messages |
| `configuration.py` | X1/X2: exact schema, nested copies, path resolution and safety |
| `processing.py` | X3: calculations with explicit inputs and no external effects |
| `run.py` | X4: the configured entry point |

Each implemented task is labelled `SOLUTION` in its function/docstring.
`SOLUTIONS.md` walks you through every task and explains why the code is written
this way. It is addressed to you as the reader, not to a course administrator.

`STUDENT_GUIDE.md` and `EXTENSION_1.md` retain the original assignment wording for
comparison. Their first-run/stub descriptions refer to the student starter, not
to this solved copy. `NEXT_STEP.md` still describes a **future** streaming stage;
an infinite simulator is not a missing solution to this assignment.

## 5. Check the solution

Run every supplied and added check:

```bash
python -m unittest discover -s checks -p "*.py" -v
```

Expected result for the distributed solution: **76 tests, all passed, zero skipped**.
The individual groups are 12 original baseline checks, 20 original exercise checks,
and 44 extra regression/integration checks. The original exercise runner still
knows how to skip `NotImplementedError`, but the completed functions do not raise it.
A skip would mean you are no longer running the fully completed reference.

Tests use temporary directories and do not overwrite your `data/` or `output/`.
They include complete command-line runs with CSV, JSON and JSON Lines, disabled
calibration, an empty selection, wrong configuration, missing/corrupt files,
path collisions, input preservation, repeat logging and a different working directory.

## 6. Try three small changes

First, switch `input.format` to `json` and `input.path` to `../data/readings.json`
in a copy of the configuration. The selected calculations should stay the same.

Second, set `calibration.enabled` to `false`. The selected mean should become
21.0 and `calibration_applied` should be false. Coefficients remain required and
validated even when you do not use them.

Third, set `selection.room` to a name absent from the data. The command should
succeed with an empty CSV (header only), count 0, and `null` numerical statistics.
It must not silently fall back to another sensor.

A relative **command-line config path** starts at your terminal's working directory.
Relative **paths inside that config file** start at the config file's own directory.
The default config is located beside `run.py`, independently of your working directory.

## 7. Boundaries to keep in mind

Everything here processes finite data. A function accepting `Iterable` is not
automatically suitable for an infinite source. File readers and the pipeline
retain lists, whole-dataset summaries require an end, and snapshot writers replace
files. There is no sleeping, background acquisition or hidden live service.

Path collision checks resolve ordinary aliases and symbolic links. They are
teaching safeguards, not a security sandbox; hard links and filesystem races are
not addressed. Writes are not transactional: a failed second write can leave
one output updated and another old. Logging can also fail if its destination is
unwritable. These limitations are deliberate later engineering topics.

The input units are C, %, and hPa. There is no unit conversion, calibration fitting,
uncertainty propagation, outlier removal, duplicate rejection or timestamp sorting.
Calibration coefficients apply only to the selected series. Do not reuse a
laboratory-temperature correction for another station or physical quantity without
making that a justified, explicit choice.
