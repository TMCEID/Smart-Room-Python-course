"""SOLUTION X4: run the configured, finite sensor-data pipeline.

Run: python run.py [config/example.json]
For the earlier, explicit-settings solution, first read/run run_finite.py.
"""
import argparse
import logging
from pathlib import Path

from analysis import explore_data, summarise_by_series
from configuration import load_config
from logging_service import configure_logging
from processing import process_readings
from readers import read_data
from records import UNITS
from storage import save_csv, save_json

# This default is anchored to the script. An explicit CLI path is relative to cwd.
ROOT = Path(__file__).resolve().parent
LOGGER = logging.getLogger(__name__)


def main(config_path: Path = ROOT / "config" / "example.json") -> None:
    """Load settings once; keep I/O effects around, not inside, the pure calculation."""
    # Validate/collision-check BEFORE opening a log or any output snapshot.
    config = load_config(config_path)
    configure_logging(config["logging"]["level"], config["logging"]["path"])
    LOGGER.info("Loaded configuration: %s", Path(config_path).resolve())

    LOGGER.info("Reading %s input: %s", config["input"]["format"], config["input"]["path"])
    raw_readings = read_data(config["input"]["path"], config["input"]["format"])
    exploration = explore_data(raw_readings)
    raw_summaries = summarise_by_series(raw_readings)
    LOGGER.info("Read %d raw records in %d distinct series", len(raw_readings),
                len(exploration["series"]))

    # Pure processing receives values/settings, not filenames or loggers.
    result = process_readings(raw_readings, config["selection"], config["calibration"])
    LOGGER.info("Selected %d records for %s", len(result["readings"]), config["selection"])
    if result["calibration_applied"]:
        LOGGER.info("Calibration enabled: scale=%s, offset=%s",
                    config["calibration"]["scale"], config["calibration"]["offset"])
    else:
        LOGGER.info("Calibration disabled; selected values remain raw.")
    if not result["readings"]:
        LOGGER.warning("Selection is empty; saving no readings and undefined statistics.")

    # Keep raw exploration separate from the selected, possibly calibrated summary.
    # Paths become strings only where they are deliberately included as JSON metadata.
    report = {
        "source": {"path": str(config["input"]["path"]), "format": config["input"]["format"]},
        "series": {**config["selection"], "unit": UNITS[config["selection"]["metric"]]},
        "calibration_applied": result["calibration_applied"],
        "calibration": config["calibration"].copy(),
        "summary": result["summary"],
        "raw_exploration": exploration,
        "raw_series_summaries": raw_summaries,
    }
    save_csv(config["output"]["readings_path"], result["readings"])
    save_json(config["output"]["summary_path"], report)
    LOGGER.info("Saved processed readings: %s", config["output"]["readings_path"])
    LOGGER.info("Saved summary and raw exploration: %s", config["output"]["summary_path"])
    label = "Calibrated" if result["calibration_applied"] else "Uncalibrated"
    print(f"{label} summary:", result["summary"])


if __name__ == "__main__":
    # Imports remain quiet; parsing command-line options belongs to script execution.
    parser = argparse.ArgumentParser(description="Process one finite sensor dataset.")
    parser.add_argument("config", nargs="?", type=Path,
                        default=ROOT / "config" / "example.json",
                        help="JSON settings file (default: config/example.json beside this script)")
    args = parser.parse_args()
    try:
        main(args.config)
    except (OSError, ValueError) as error:
        # Fail visibly and return a nonzero exit code; do not invent a success result.
        LOGGER.error("Run stopped: %s", error)
        raise SystemExit(1) from error
