# Validation of the completed reference solution

This file describes the **solved folder**, not the earlier exercise scaffold.
Checks were executed using Python **3.13.5 on Linux**. No external Python packages
are needed by the implementation or its unittest suite.

## Executed checks

```bash
python -m unittest discover -s checks -p "*.py" -v
```

**76 tests passed; zero failures, zero errors, zero skips.** These comprise:

- 12 original baseline checks, retained unchanged;
- 20 original exercise checks, retained unchanged and now actually executed;
- 44 additional solution checks, including complete subprocess executions.

The final ZIP was also extracted into a fresh directory and this complete command
was rerun against that copy, followed by both entry points. The clean extraction
was initially free of runtime output and Python bytecode.

The checks cover agreement among the three input formats; malformed documents and
records; input-location errors; empty data; identity calibration; new dictionaries;
finite calibration results; actual timestamp comparison; correct sample SD and
median; grouping by all three identity components; retained units; source iteration
once; disabled calibration; snapshot replacement; CSV and JSON Lines round trips;
UTF-8 text; log appending and duplicate-handler prevention; strict configuration
keys/types/values; nested copy independence; all six pairwise input/output/log
collisions; protection of the configuration file; and visible nonzero failure exits.

The original module-import check remains green. An added check covers both entry
points: importing them does not start processing or create output files.

## End-to-end behaviour observed

Both `python run_finite.py` and `python run.py` completed. The default larger input
contains 36 records across six series. The selected laboratory-temperature series
contains six records. With scale 1.02 and offset -0.4, the selected summary was:

```text
count:      6
mean:       21.02
minimum:    20.0
maximum:    22.040000000000003
median:     21.020000000000003
sample_sd:  0.7632981069018853
```

These are floating-point results, not manually rounded expected-output strings.
With calibration disabled, the selected mean was 21.0 and the recorded calibration
flag was false. Missing selections produced count 0, null numerical statistics and
a header-only CSV. No fallback to another series occurred.

The integration suite launched the scripts **outside the project directory**.
It also exercised a relative command-line config argument, all three configured
input formats, console-only logging, two consecutive runs, invalid configuration,
a missing input and the deliberately broken CSV. It compared source-file bytes
before and after successful runs and checked the saved CSV against its summary.

The standard record parser, five data fixtures, example configuration, data
contract, generator-preparation note and two original check files are byte-for-byte
unchanged from `room_sensor_backbone_annotation_fix.zip` (11 retained files).
The original assignment guides have only a reference-edition notice prepended.
The previous starter README, progress, compatibility and validation pages were
replaced with accurate reference-solution versions. No unfinished function remains
in the implementation modules.

## Compatibility checks and limits

All **13 Python files** parsed under the Python 3.9 grammar setting. Type hints for
all **25 module-defined functions** resolved under the available Python 3.13.5
runtime. These are syntax/annotation checks, not execution under Python 3.9.

A Python 3.9 runtime was unavailable, and an attempted download failed at DNS
resolution. No runtime test on 3.9, Windows or macOS is claimed. The earlier
Optional/Union fix remains in place; see `COMPATIBILITY.md` for timestamp-format
cautions on older interpreters.

This is a finite teaching pipeline. Tests are not a proof of every possible input,
filesystem state or numeric extreme. No real sensor hardware, unbounded stream,
long-running retention policy, transactional writes, malicious-input sandboxing,
network access or live browser is implemented or tested. There is deliberately no
package manifest, Git setup or third-party dependency installation.

Path safeguards cover resolved path equality, not hard-link aliases or filesystem
races. Disk errors can interrupt a snapshot write or leave only one of the two
configured outputs updated. The analysis functions assume the documented parsed
record contract; they do not silently normalise arbitrary units or missing fields.
