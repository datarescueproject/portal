"""Generate tracked Jekyll collections from the committed Baserow snapshots."""

import argparse
import ast
import os
import re
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "baserow"
CONTENT_DIR = ROOT / "content"
COLLECTION_DIRS = {
    "datasets": CONTENT_DIR / "_datasets",
    "organizations": CONTENT_DIR / "_organizations",
    "categories": CONTENT_DIR / "_dataset_categories",
}


def clean_text(value):
    """Match the text cleanup used by the existing generated records."""
    string = str(value)
    string = string.replace("\n", "").replace("\r", "").replace("\t", "")
    string = re.sub(r"\s+", " ", string)
    string = re.sub(r"^[^a-zA-Z0-9]+", "", string)
    string = re.sub(r"^-", "", string)
    string = string.rstrip(":")
    return re.sub(r"(?<!http)(?<!https):", "", string)


def slugify(value):
    string = clean_text(value)
    string = re.sub(r"[^\w\s-]", "", string)
    string = re.sub(r"\s+", "-", string)
    return string.lower()


def get_metadata_availability(dataset_id, data_backups):
    matches = data_backups[data_backups.dataset_id == dataset_id]
    availability = matches.metadata_available.astype(str).str.lower().tolist()
    if "yes" in availability:
        metadata_url = matches.loc[
            matches.metadata_available.astype(str).str.lower() == "yes", "metadata_url"
        ].iloc[0]
        return "Yes", metadata_url
    if "needs review" in availability:
        return "Under Review", ""
    return "No", ""


def get_dataset_categories(row, organizations):
    overrides = ast.literal_eval(row["categories"])
    if overrides:
        categories = [category["value"] for category in overrides]
    elif row["organization"] == "Unknown":
        categories = ["Uncategorized"]
    else:
        organization_names = [name.strip() for name in row["organization"].split(",")]
        values = organizations[
            organizations["Organizations"].isin(organization_names)
        ]["Categories"].values
        categories = [category for value in values for category in value.split(";")]
        categories = [category for category in categories if category]
        if not categories:
            categories = ["Uncategorized"]
    return sorted(set(categories))


def render_category(row):
    category_slug = slugify(row["Name"])
    return (
        "---\n"
        f"name: {row['Name']} \n"
        f"logo: /assets/images/categories/{category_slug}.svg \n"
        f"featured: {row['Active']} \n"
        "---\n"
    )


def render_organization(name):
    return f"---\ntitle: {clean_text(name)} \ndescription: \n---\n"


def render_dataset(row, backups, organizations):
    organization = row["organization"] or "Unknown"
    data_backups = backups[backups.dataset == row["dataset"]]
    metadata_available, metadata_url = get_metadata_availability(
        row["dataset_id"], data_backups
    )

    lines = [
        "---",
        f"title: {clean_text(row['dataset'])}",
        f"organization: {clean_text(organization)}",
        f"agency: {clean_text(row['agency'])}",
        f"websites: {clean_text(row['websites'])}",
        f"data_source: {clean_text(row['url'])}",
        f"description: {clean_text(row['notes'])}",
        f"last_modified: {row['last_modified']}",
        f"dataset_source_status: {clean_text(row['dataset_source_status'])}",
        f"metadata_available: {metadata_available}",
        f"metadata_url: {clean_text(metadata_url)}",
        "category:",
    ]
    lines.extend(
        f"  - {category} "
        for category in get_dataset_categories(
            {**row.to_dict(), "organization": organization}, organizations
        )
    )
    lines.append("resources:")
    for index, backup in data_backups.iterrows():
        lines.extend(
            [
                f"  - id: {index}",
                f"    url: {clean_text(backup['download_location'])}",
                f"    format: {clean_text(backup['file_type'])}",
                f"    status: {clean_text(backup['status'])}",
                f"    size: {backup['size']}",
                f"    download_date: {backup['download_date']}",
                f"    maintainer: {clean_text(backup['maintainer'])}",
                f"    notes: {clean_text(backup['notes'])}",
            ]
        )
    lines.append("---")
    return "\n".join(lines) + "\n"


def load_snapshots():
    backups = pd.read_csv(DATA_DIR / "backups.csv").fillna("")
    datasets = pd.read_csv(DATA_DIR / "datasets.csv").fillna("")
    organizations = pd.read_csv(DATA_DIR / "organizations.csv").fillna("")
    categories = pd.read_csv(DATA_DIR / "categories.csv").fillna("")

    backups.columns = backups.columns.str.lower()
    datasets.columns = datasets.columns.str.lower()
    categories["Active"] = categories["Active"].astype(str).str.lower()
    return backups, datasets, organizations, categories


def build_expected_files():
    backups, datasets, organizations, categories = load_snapshots()
    expected = {name: {} for name in COLLECTION_DIRS}

    for _, row in categories.iterrows():
        expected["categories"][f"{slugify(row['Name'])}.md"] = render_category(row)

    organization_names = set()
    for _, row in datasets.iterrows():
        organization = row["organization"] or "Unknown"
        organization_names.add(organization)
        expected["datasets"][f"{slugify(row['dataset'])}.md"] = render_dataset(
            row, backups, organizations
        )

    for organization in organization_names:
        filename = f"{slugify(organization)}.md"
        if len(filename) < 253:
            expected["organizations"][filename] = render_organization(organization)

    return expected


def find_differences(expected):
    differences = []
    for collection, directory in COLLECTION_DIRS.items():
        actual_names = {path.name for path in directory.glob("*.md")}
        expected_names = set(expected[collection])
        differences.extend(f"missing: {directory / name}" for name in expected_names - actual_names)
        differences.extend(f"stale: {directory / name}" for name in actual_names - expected_names)
        for name in actual_names & expected_names:
            if (directory / name).read_text(encoding="utf-8") != expected[collection][name]:
                differences.append(f"changed: {directory / name}")
    return sorted(differences)


def write_atomically(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary_file:
        temporary_file.write(content)
        temporary_path = Path(temporary_file.name)
    os.replace(temporary_path, path)


def generate(expected):
    for collection, directory in COLLECTION_DIRS.items():
        directory.mkdir(parents=True, exist_ok=True)
        expected_names = set(expected[collection])
        for stale_path in directory.glob("*.md"):
            if stale_path.name not in expected_names:
                stale_path.unlink()
        for name in sorted(expected_names):
            write_atomically(directory / name, expected[collection][name])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail when tracked content is out of date"
    )
    args = parser.parse_args()
    expected = build_expected_files()

    if args.check:
        differences = find_differences(expected)
        if differences:
            print("Generated content is out of date:")
            print("\n".join(differences[:50]))
            if len(differences) > 50:
                print(f"...and {len(differences) - 50} more differences")
            raise SystemExit(1)
        print("Generated content matches the committed Baserow snapshots.")
        return

    generate(expected)
    counts = ", ".join(
        f"{len(files)} {collection}" for collection, files in expected.items()
    )
    print(f"Generated {counts}.")


if __name__ == "__main__":
    main()
