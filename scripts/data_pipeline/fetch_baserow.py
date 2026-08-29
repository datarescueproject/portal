"""Fetch the portal's canonical Baserow tables into committed CSV snapshots."""

import os
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "data" / "baserow"
API_ROOT = "https://baserow.datarescueproject.org/api/database/rows/table"


def get_results_json(table_id, access_token):
    url = f"{API_ROOT}/{table_id}/?user_field_names=true"
    results = []
    while url:
        response = requests.get(
            url,
            headers={"Authorization": f"Token {access_token}"},
            timeout=300,
        )
        response.raise_for_status()
        payload = response.json()
        results.extend(payload["results"])
        url = payload["next"]
    return results


def get_array_values(values, column):
    return ", ".join(str(value[column]) for value in values)


def get_optional_array_values(values, column="value"):
    return get_array_values(values, column) if values else ""


def normalize_line_endings(value):
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n")
    return value


def write_csv_snapshot(frame, filename):
    normalized = frame.apply(lambda column: column.map(normalize_line_endings))
    normalized.to_csv(OUTPUT_DIR / filename, index=False, lineterminator="\n")


def process_dataset_row(row):
    return {
        "dataset": row["Name"],
        "notes": row["Notes"],
        "dataset_id": row["id"],
        "url": row["URL"],
        "websites": get_array_values(row["Websites"], "value"),
        "organization": get_array_values(row["Organization"], "value"),
        "agency": get_array_values(row["Agency"], "value"),
        "categories": row["Categories"],
        "last_modified": row["Last modified"],
        "dataset_source_status": get_array_values(row["Dataset Status"], "value"),
    }


def process_backup_row(row):
    if not row["Dataset"]:
        return None
    metadata = row["Metadata Available"]
    status = row["Status"]
    return {
        "dataset": get_optional_array_values(row["Dataset"]),
        "dataset_id": get_optional_array_values(row["Dataset"], "id"),
        "status": status["value"] if status else "In Progress",
        "url": get_optional_array_values(row["Dataset URL"]),
        "source_website": get_optional_array_values(row["Website"]),
        "organization": get_optional_array_values(row["Organization"]),
        "agency": get_optional_array_values(row["Agency"]),
        "download_date": row["Backup date"],
        "size": row["Backup size"],
        "maintainer": get_array_values(row["Maintainer"], "value"),
        "download_location": row["Backup location"],
        "file_type": get_array_values(row["File type"], "value"),
        "notes": row["Notes"],
        "metadata_available": metadata["value"] if metadata else "",
        "metadata_url": row["Metadata URL"],
    }


def main():
    access_token = os.environ.get("BASEROW_ACCESS_TOKEN")
    if not access_token:
        raise SystemExit("BASEROW_ACCESS_TOKEN is required")

    dataset_rows = get_results_json(639, access_token)
    backup_rows = get_results_json(640, access_token)
    categories = pd.DataFrame(get_results_json(732, access_token))[
        ["Name", "Active"]
    ]
    organizations = pd.DataFrame(get_results_json(638, access_token))[
        ["Organizations", "Categories"]
    ]
    organizations["Categories"] = organizations["Categories"].apply(
        lambda values: ";".join(value["value"] for value in values)
    )

    backups = pd.DataFrame(
        processed
        for row in backup_rows
        if (processed := process_backup_row(row)) is not None
    )
    backups = backups[backups["status"] == "Finished"]
    datasets = pd.DataFrame(process_dataset_row(row) for row in dataset_rows)
    datasets = datasets[datasets["dataset"].isin(backups["dataset"])]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv_snapshot(datasets, "datasets.csv")
    write_csv_snapshot(backups, "backups.csv")
    write_csv_snapshot(categories, "categories.csv")
    write_csv_snapshot(organizations, "organizations.csv")
    print(
        f"Saved {len(datasets)} datasets, {len(backups)} backups, "
        f"{len(categories)} categories, and {len(organizations)} organizations."
    )


if __name__ == "__main__":
    main()
