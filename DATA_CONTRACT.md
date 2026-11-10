# Agree on one reading before you write several readers

You will have several ways to read data, but the rest of your program should not
need to know which file format was used. Your readers therefore return the same
kind of Python object: a finite list of dictionaries. Each dictionary describes
one measurement of one physical quantity.

## One standard record

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

| Field | Meaning and rule |
|---|---|
| `time` | ISO 8601 text with an explicit timezone; the parser normalises it to UTC. |
| `room` | Non-empty room name. |
| `sensor_id` | Non-empty station identifier. |
| `metric` | One of `temperature`, `humidity`, `pressure`. |
| `value` | Finite float after parsing; a numeric string may arrive from a file. |
| `unit` | `C` for temperature, `%` for relative humidity, `hPa` for pressure. |

A measurement series has the identity **(room, sensor_id, metric)**. Do not group
by room alone, or by sensor alone. One sensor station supplies three quantities,
and their numerical values are not interchangeable.

The fixtures already use the agreed units. You are not asked to build unit
conversion in this iteration. Fahrenheit is rejected, not quietly interpreted as
Celsius. Calibration is a correction within a unit; it is not a replacement for
an explicit unit conversion.

## Your parser is a common boundary

`records.parse_record` is supplied. Call it for each row/object from every reader.
It checks required fields, finite numeric values, non-empty text, recognised
metric/unit pairs, and timezone-aware timestamps. It returns a new dictionary.
A boolean is not accepted as a measurement, even though Python can convert it to
a number. Extra named fields are ignored in this first record contract.

The parser does not reject statistical outliers, perform calibration, remove
repeated timestamps, or sort data. Keep those decisions visible rather than
hiding them inside one reader. For now, stop at the first invalid record; never
silently return only the valid prefix or replace bad readings with zero.

## The supplied files

All measurements are synthetic classroom fixtures, not observations from real
sensors. You may inspect or copy them freely within your project.

| File | Contents |
|---|---|
| `tiny.csv` | Three laboratory temperatures: 20, 21, 22 C. Start here. |
| `readings.csv` | 36 records: two rooms, one station per room, three metrics, six times. |
| `readings.json` | The same 36 records, in the same order, as one JSON array. |
| `readings.jsonl` | The same 36 records, in the same order, one JSON object per line. |
| `broken.csv` | One valid row followed by a non-numeric value, missing timezone, wrong unit. |

The larger files cover 12:00 through 12:05 UTC on 1 October 2026. Every individual
series has six records. Their order is interleaved: a temperature may be followed
by humidity from the same station. You cannot assume consecutive rows belong to
one series. In `broken.csv`, the first failure is physical line 3, including the
header. Repair it to reveal the next intentional failure.

## Input, processing and output are different responsibilities

Your reader produces records in original row order. Your calibration returns new
records with a changed `value`, keeping identity, timestamp and unit. Your analysis
uses either one series or explicit groups. Your writer serialises a result; it
does not calculate it.

The original file and original in-memory records remain unchanged. Keep both raw
and processed lists under distinct names while you work. Apply calibration once
to raw readings, not repeatedly to previously calibrated output. The CSV record
format alone does not tell you whether calibration has already been applied;
record that information in the accompanying summary JSON.

All finite snapshot writers use replacement mode. JSON and CSV snapshots are not
transactional database updates: a disk error can still leave a partial write.
Your log file, by contrast, will use append mode. Never use an input filename as
an output filename. Extension 1 adds explicit path-collision checks.
