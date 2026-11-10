# Completed reference: task map

Use this table to compare your attempt with the reference. Every current task is
implemented; there are no live exercise stubs in the Python modules.

| Task | Implementation | Evidence |
|---|---|---|
| R1: JSON reader | `readers.read_json` | Same 36 parsed records as CSV; invalid containers rejected |
| R2: JSON Lines reader | `readers.read_jsonl` | Same records; blank lines skipped; bad line identified |
| E1: Exploration | `analysis.explore_data` | 36 records, six distinct series; empty/reversed input checked |
| C1: Calibration | `calibration.calibrate_reading` | Corrected values in new dictionaries; raw values unchanged |
| S1: Extended summary | `analysis.extended_summary` | Median and sample SD; empty/singleton cases |
| S2: Per-series statistics | `analysis.summarise_by_series` | Lab temperature mean 21; office temperature mean 23.5 |
| W1: CSV storage | `storage.save_csv` | Header, snapshot replacement, empty and round-trip checks |
| W2: JSON Lines storage | `storage.save_jsonl` | Round trip, replacement, empty and non-finite checks |
| L1: File logging | `logging_service.configure_logging` | Append without duplicate handlers; UTF-8 checked |
| I1: Finite assembly | `run_finite.py` | Complete subprocess run, CSV/JSONL and report produced |
| X1: Validation | `configuration.validate_config` | Missing/unknown names, types and choices rejected |
| X2: Path handling | `configuration.resolve_paths`, `load_config` | Nested copies, relative paths, collision protection |
| X3: Functional core | `processing.process_readings` | Single source consumption, no mutation, enabled/disabled paths |
| X4: Configured assembly | `run.py` | All input formats, optional config path and failure exits |

The command `python -m unittest discover -s checks -p "*.py" -v` runs all 76 checks.
The extra checks are not a claim of exhaustive correctness for all possible input.
Use `SOLUTIONS.md` for the reasoning and `VALIDATION.md` for environment limits.

## Decisions you can explain from the code

An empty dataset is valid: count 0 and undefined numerical statistics represented
by None/null. An invalid record is not valid empty data: the read stops visibly.
Calibration returns new records. Logs append and describe actions; snapshots
replace files and contain measurements/results. The current whole-data analysis
would not finish on an infinite source. All settings are loaded once, outside the
pure calculation.
