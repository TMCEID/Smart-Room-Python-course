# Walk through your completed solution

Use this reference after you have tried a task, or when you need a small working
example to discuss. You do not need to read every file in one sitting. Run one
stage, inspect one function, change one input and predict the result before you
run it again.

The solution covers **R1, R2, E1, C1, S1, S2, W1, W2, L1, I1 and X1–X4**.
A useful reading order is `run_finite.py`, its component functions, then
`configuration.py`, `processing.py`, and finally `run.py`.

## 1. Recognise the objects moving through your program

A filename, a list of records, a list of numerical values and a summary are not
interchangeable. A reader receives a path and returns records. Calibration changes
one value in a new record. Analysis receives records or values, not filenames.
A writer receives an already calculated product and serialises it.

The shared record remains a simple dictionary:

```python
{
    "time": "2026-10-01T12:00:00+00:00",
    "room": "laboratory",
    "sensor_id": "station-01",
    "metric": "temperature",
    "value": 20.0,
    "unit": "C",
}
```

`records.py` is unchanged from the corrected starter. Its parser rejects missing
fields, invalid numerical values, missing timezones and unsupported metric/unit
pairs. Each reader calls this same function. That is why the rest of the program
does not need to remember whether a value originally came from CSV text or a JSON
number. Refer to `DATA_CONTRACT.md` for the exact rules.

## 2. R1 and R2 — Decode the format, then use the shared parser

In `read_json`, `json.load` decodes the entire finite document. The function then
checks that the result is a list. This matters: valid JSON can also describe a
number, a string or a dictionary, none of which is the agreed top-level reading
array. Only after that check do we call `parse_record` for each item.

A damaged record reports its **item number**. A JSON array item can span many
physical lines, so claiming that item 2 is necessarily line 2 would be misleading.
Malformed JSON syntax instead reports the line and column supplied by the decoder.

`read_jsonl` uses a different boundary: each non-blank line is a whole JSON object.
It skips blank lines, decodes one line and calls the same parser. A malformed or
invalid non-blank line stops the read and reports its physical line number.
Neither reader hides file-access errors by returning an empty dataset.

From a Python session opened in this folder, compare all three formats:

```python
from pathlib import Path
from readers import read_csv, read_json, read_jsonl

csv_records = read_csv(Path("data/readings.csv"))
json_records = read_json(Path("data/readings.json"))
jsonl_records = read_jsonl(Path("data/readings.jsonl"))
print(len(csv_records))  # 36
print(csv_records == json_records == jsonl_records)  # True
```

This line-oriented reader still builds a list. It is useful preparation for a
future generator, but it does not yet give you bounded memory for unending data.

## 3. E1 — Explore coverage before calculating a result

Open `explore_data` in `analysis.py`. It describes the input, rather than printing
or plotting it. You receive record counts, sorted identities, time bounds and a
sorted list of distinct measurement series.

The private helper `_group_by_series` makes the complete key
`(room, sensor_id, metric)` explicit. A leading underscore is a naming convention
for an internal helper, not a special access-control mechanism. Exploration and
per-series statistics reuse this small grouping step rather than grow two subtly
different versions of it.

The supplied larger file yields 36 records and six groups with six readings each.
The time bounds are found by parsing and comparing timestamps, not by trusting the
first and last rows. Reversing the list therefore does not reverse the reported
time interval. The original list is not sorted or modified.

The set comprehensions collect unique room, sensor and metric names. Sorting
those sets gives deterministic lists, which makes repeated outputs easier to
compare. The empty report has count 0, empty lists and `None` time bounds.

Do not add a mean across all input values. Such a mean would mix C, percent and
hPa. Explore the identities first; choose a physically meaningful series next.

## 4. C1 — Calibration returns a new record

The solution is deliberately short:

```python
def calibrate_reading(reading, scale, offset):
    corrected = reading.copy()
    corrected["value"] = calibrate_value(reading["value"], scale, offset)
    return corrected
```

The dictionary copy separates the processed record from the raw one. A shallow
copy is enough for this contract because each field is a string or a number;
there are no nested mutable lists that must be copied as well.

The scalar function applies scale first and then offset. With scale 1.02 and
offset -0.4, the tiny values 20, 21 and 22 become approximately 20.00, 21.02 and
22.04. The time, identity and unit are unchanged. Even an identity correction
(scale 1, offset 0) returns a new dictionary.

Calling calibration twice on the **same raw input** should produce the same
answer. Applying calibration to its previous output is a different operation and
would generally apply the correction twice. Keep raw and processed names distinct.
The file format itself does not tell you whether a correction was already applied;
the accompanying summary records that decision.

## 5. S1 and S2 — Reuse statistics, but keep physical series separate

`extended_summary` starts with `basic_summary` and adds only the two new fields.
For the median, an empty list has no answer. For sample standard deviation, fewer
than two observations give no answer. The result is `None`, not zero. Your JSON
writer later represents this as `null`.

Sample standard deviation uses the n-1 denominator in its variance. This is why
we call `statistics.stdev`, not `pstdev`. For [20, 21, 22], the sample standard
deviation is 1. You can inspect this small case by hand before trusting a larger
result. Sorting for median does not modify your original list.

`summarise_by_series` groups records and calls `extended_summary` once per group.
The output includes the full identity and unit beside each nested summary.
The supplied laboratory-temperature mean is 21.0 C, while the office-temperature
mean is 23.5 C. Neither is a mean across both rooms or across all quantities.

This function reports the values supplied to it. In the entry points, the
`raw_series_summaries` field is deliberately calculated from raw records. The
selected calibrated summary is a separate product. Analysis never guesses which
calibration it ought to apply.

## 6. W1 and W2 — Store snapshots, not operational messages

`save_csv` creates the parent directory, opens the target in replacement mode,
writes the standard header, and writes the records. `newline=""` leaves CSV
newline handling to the CSV machinery. The field order comes from `records.FIELDS`,
so input and output agree about the format. With no records, you still get a header.

`save_jsonl` writes one complete JSON object followed by a newline for each record.
There is no outer array and no comma separating two lines. Empty input writes an
empty file, replacing any previous contents. `allow_nan=False` rejects numerical
values that are not part of standard JSON.

Both JSON writers prepare their text before opening the destination in replacement
mode. A serialisation error therefore does not first erase an old valid file.
This is a small safeguard, not a transactional write protocol. Disk errors can
still interrupt writes; the CSV writer also assumes already validated records.

Try a round trip after `python run_finite.py`:

```python
from pathlib import Path
from readers import read_csv, read_jsonl

csv_rows = read_csv(Path("output/finite/calibrated.csv"))
jsonl_rows = read_jsonl(Path("output/finite/calibrated.jsonl"))
print(csv_rows == jsonl_rows)  # True
print(len(csv_rows))          # 6, also after running the script again
```

Keep raw inputs in `data/` and processed products in `output/`. The writers do not
know which files you used as inputs; path protection belongs to the calling code.

## 7. L1 — Configure logging once and keep numerical functions quiet

`configure_logging` constructs a console handler and, when a path is supplied,
a UTF-8 file handler opened in append mode. The old messages survive the next
run. `force=True` replaces the entry point's previous root handlers, so configuring
this small application twice does not duplicate each message.

`logging.getLogger(__name__)` obtains the logger used by an entry-point module.
It does not read data or start logging a run merely because you import that module.
Messages are emitted around actions in `main`: input format/path, counts, selection,
calibration decision and output locations. Pure functions do not log.

Inspect `run.log` after two runs. Each action should appear once per run, not twice
because two handlers accidentally accumulated. The log explains what happened;
it is not a substitute for the measurements stored in CSV or JSON Lines.

## 8. I1 — Follow the complete finite assignment

Read `run_finite.py` from top to bottom. Its choices are ordinary variables near
the top: input path and format, selected series, scale, offset and output folder.
Then read the visible sequence in `main` without jumping into the helpers.

The code explores all raw records, selects one physical series, creates corrected
records, extracts their values and calculates a summary. It writes both CSV and
JSON Lines so that you can compare the two representations. One JSON report records
the selected result and the separate raw exploration products.

The default now uses `readings.csv`, not `tiny.csv`, so that selection actually has
other rooms and quantities to leave behind. It still selects only six readings.
Nothing is hidden in a background service; the program finishes when those finite
outputs have been written.

## 9. X1 — Check the requested run before doing output work

`validate_config` accepts a dictionary and either returns `None` or raises a
`ValueError`. It does not read files, create directories or configure logging.
The required sections and leaf keys are fixed by the original exercise.

A small `SECTION_KEYS` dictionary describes the allowed names. `_check_keys`
reports missing and unknown keys. A typo should not be ignored just because a
programmer guessed what you intended. This is ordinary dictionary validation,
not a schema framework or plugin mechanism.

Pay particular attention to booleans. Python treats `bool` as a subtype of `int`,
so checking only `isinstance(value, (int, float))` would also accept `True` as a
scale. The solution rejects booleans before accepting numerical coefficients.
Conversely, `calibration.enabled` accepts actual booleans, not 0, 1 or the text
`"false"`. JSON `false` and JSON `"false"` are different values.

Whitespace-only paths/names are invalid. Accepted non-empty strings are preserved;
a validator should not silently remove spaces from a filename. Format, metric and
log-level choices require an exact match. Coefficients remain finite numerical
values even when calibration is disabled.

## 10. X2 — Separate the two meanings of a relative path

There are two different starting points:

```text
python run.py project/config/example.json
              ^ relative to the terminal's current working directory

"input": {"path": "../data/readings.csv", ...}
                   ^ relative to the directory containing that config file
```

The default configuration path instead starts beside `run.py`, using
`ROOT = Path(__file__).resolve().parent`. `ROOT` is a `Path` object. Its `/`
operator joins path components; it is not division and it is not a property of
uppercase variable names. The class name is `Path`, not `PATH`.

`resolve_paths` copies the nested settings before replacing text paths with
absolute `Path` objects. A shallow top-level copy would still share dictionaries
such as `config["input"]`; assigning into one would unexpectedly change the original.
`deepcopy` makes this distinction explicit in a small amount of code.

Paths are resolved before comparing destinations. For example, `data/x.csv` and
`output/../data/x.csv` should not evade a collision check. No two of input,
processed output, summary output and log may point to the same resolved path.
`load_config` additionally protects the configuration file itself. A null log path
stays `None` and means console-only logging.

Path resolution may inspect the filesystem to follow symbolic links, but it does
not create the requested directories or files. The checks are not a filesystem
security model: hard-link aliases and changes between checking and writing are
outside this exercise.

## 11. X3 — A pure processing function with explicit arguments

Now inspect `process_readings` in `processing.py`. It receives records, selection
settings and calibration settings. It does not receive an input filename, a config
path or a logger. The steps remain recognisable:

```text
select one series -> optionally calibrate -> extract values -> summarise
```

Selecting first prevents a temperature correction from being applied to the same
station's humidity or pressure records. The result contains new record dictionaries
even when calibration is disabled. You can therefore edit the returned record
without changing a raw dictionary through a shared reference.

Pass `iter(raw_records)` and the source is consumed once, during selection. The
selected finite list can then be used for both output and statistics. The regression
suite includes an iterable that deliberately raises an error if anyone tries to
start it twice.

This is the functional-programming part: explicit inputs, transformations that
return new values, no hidden I/O, and reusable small functions. There is no need
for nested lambdas or a general `compose` engine. List comprehensions keep the
transformation order visible.

The field `calibration_applied` follows the exercise contract and mirrors the
requested `enabled` setting. For an empty selection it can still be true, but
count 0 and empty readings show that there were no values to correct. It is not
an independent claim that a non-empty calibration took place.

This function still requires finite input. Selecting every matching record from
an infinite iterable would never finish. The `Iterable` annotation broadens the
accepted interface; it does not change that algorithmic fact.

## 12. X4 — Let run.py own the external actions

The final entry point loads configuration once and configures logging once. It
reads raw data, obtains raw exploration products, and calls the pure processing
function with explicit settings. Finally, it saves processed records and report
metadata. The optional positional config argument is handled with `argparse`.

Do not write the entire resolved settings dictionary directly as JSON: it now
contains `Path` objects. The report selects the fields that describe the analysis
and converts the recorded input path to text. The CSV contains the very same
processed readings whose values produced the selected summary.

The outer script catches expected file and validation errors, logs the failure
and exits with a nonzero status. An invalid configuration is checked before a log
or snapshot is opened. A bad data file may leave operational messages in the log,
but it must not generate a new successful analysis product.

There is no rollback spanning the CSV and JSON writes. If the first write succeeds
and the second fails, the program reports failure, but the first file remains.
Do not confuse this teaching pipeline with a transactional database update.

## 13. What is complete, and what remains a different assignment?

Every function that was an exercise stub now has an implementation, and both I1
and X4 have runnable entry points. The original 20 exercise checks execute instead
of skipping. The added integration checks exercise both entry points, not just
individual functions in isolation.

The generator section remains a preparation note. You can run its finite generator
expression to observe one-use consumption. A simulated infinite sensor source,
rolling windows, storage retention, installation metadata, Git workflow,
metaprogramming and a browser are intentionally later steps. Leaving those out is
not leaving a current task unfinished.

## Standard-library references

These are references for the API behaviour used in the code; the sensor fixtures,
exercise design and numerical expected results belong to this project.

- JSON decoding/encoding: https://docs.python.org/3.9/library/json.html
- Sample standard deviation and median: https://docs.python.org/3.9/library/statistics.html
- Paths and path joining: https://docs.python.org/3.9/library/pathlib.html
- Logger configuration: https://docs.python.org/3.9/library/logging.html

The 3.9 pages are useful when comparing older-interpreter APIs. They do not imply
that this solution was executed under 3.9; see `VALIDATION.md`.
