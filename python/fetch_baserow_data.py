import pandas as pd
import requests
# import json
# import numpy as np
import os
from create_markdowns import create_markdowns


BASEROW_ACCESS_TOKEN = os.environ.get("BASEROW_ACCESS_TOKEN")


def get_results_json(url):
    table = requests.get(
        url,
        headers={
            "Authorization": f"Token {BASEROW_ACCESS_TOKEN}"
        }
    )

    res = table.json()['results']
    if table.json()['next'] is not None:
        res.extend(get_results_json(table.json()['next']))

    return res


def get_arr_vals(arr, col):
    return ", ".join([str(x[col]) for x in arr])


def check_missing_vals(field, col="value"):
    if len(field) > 0:
        val = get_arr_vals(field, col=col)
    else:
        val = ""
    
    return val


def process_dataset_row(d):
    return {
        "dataset": d["Name"],
        "notes": d["Notes"],
        "dataset_id": d["id"],
        "url": d["URL"],
        "websites": get_arr_vals(d["Websites"], col="value"),
        "organization": get_arr_vals(d["Organization"], col="value"),
        "agency": get_arr_vals(d["Agency"], col="value"),
        "last_modified": d["Last modified"]
    }


def process_backup_row(d):
    if len(d["Dataset"]) > 0:
        if d["Metadata Available"]:
            metadata_avl = d["Metadata Available"]["value"]
        else:
            metadata_avl = ""
        return {
            "dataset": check_missing_vals(d["Dataset"], col="value"),
            "dataset_id": check_missing_vals(d["Dataset"], col="id"),
            "status": d["Status"]["value"],
            "url": check_missing_vals(d["Dataset URL"], col="value"),
            "source_website": check_missing_vals(d["Website"], col="value"),
            "organization": check_missing_vals(d["Organization"], col="value"),
            "agency": check_missing_vals(d["Agency"], col="value"),
            "download_date": d["Backup date"],
            "size": d["Backup size"],
            "maintainer": get_arr_vals(d["Maintainer"], col="value"),
            "download_location": d["Backup location"],
            "file_type": get_arr_vals(d["File type"], col="value"),
            "notes": d["Notes"],
            "metadata_available": metadata_avl,
            "metadata_url": d["Metadata URL"]
        }
    else:
        return


dataset_table = get_results_json("https://baserow.datarescueproject.org/api/database/rows/table/639/?user_field_names=true")
backups_table = get_results_json("https://baserow.datarescueproject.org/api/database/rows/table/640/?user_field_names=true")

rows = []
for row in backups_table:
    rows.append(process_backup_row(row))

rows = [row for row in rows if row is not None]
backups = pd.DataFrame(rows)

rows = []
for row in dataset_table:
    rows.append(process_dataset_row(row))

rows = [row for row in rows if row is not None]
datasets = pd.DataFrame(rows)

datasets.to_csv("baserow_exports/datarescue_datasets.csv", index=False)
backups.to_csv("baserow_exports/datarescue_backups.csv", index=False)

create_markdowns()
