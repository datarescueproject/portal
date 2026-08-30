import os

import numpy as np
import pandas as pd
import requests

VOLUNTEER_ACCESS_TOKEN = os.environ.get("VOLUNTEER_ACCESS_TOKEN")
BASEROW_ACCESS_TOKEN = os.environ.get("BASEROW_ACCESS_TOKEN")
CHUNK_SIZE = 200
tables_to_sync = [{'source':901,'destination':1124},{'source':640,'destination':1125}]


def get_results_json(url, api_key=BASEROW_ACCESS_TOKEN):
    table = requests.get(
        url,
        headers={
            "Authorization": f"Token {api_key}"
        },
        timeout=300,
    )

    res = table.json()['results']
    if table.json()['next'] is not None:
        res.extend(get_results_json(table.json()['next']))

    return res


def extract_link_values(value):
    if isinstance(value, dict):
        return value.get("value", value)

    if isinstance(value, list):
        return [
            item.get("value", item) if isinstance(item, dict) else item
            for item in value
        ]
        
    return value


def replace_linked_records_with_values(rows):
    """
    Convert:
        [{"id": 12, "value": "Alice"}]
    into:
        ["Alice"]
    """
    converted_rows = []
    fields = rows[0].keys()
    for row in rows:
        converted_row = row.copy()

        for field in fields:
            converted_row[field] = extract_link_values(converted_row.get(field))

        converted_rows.append(converted_row)

    return converted_rows


def arrays_to_strings(df):
    converted = df.copy()

    def convert(value):
        if isinstance(value, (list, tuple, np.ndarray)):
            return ",".join(
                str(item.get("value", item))
                if isinstance(item, dict)
                else str(item)
                for item in value
            )
        return value

    for column in converted.columns:
        converted[column] = converted[column].map(convert)

    return converted


for t in tables_to_sync:
    rows_on_tracker = get_results_json(f"https://baserow.datarescueproject.org/api/database/rows/table/{t['source']}/?user_field_names=true",BASEROW_ACCESS_TOKEN)
    rows_on_volunteer = get_results_json(f"https://baserow.datarescueproject.org/api/database/rows/table/{t['destination']}/?user_field_names=true",VOLUNTEER_ACCESS_TOKEN)

    rows_on_tracker = replace_linked_records_with_values(rows_on_tracker)
    rows_on_tracker = pd.DataFrame(rows_on_tracker)
    rows_on_tracker = rows_on_tracker.drop(columns=['order'])
    rows_on_tracker = arrays_to_strings(rows_on_tracker)
    if rows_on_volunteer:
        rows_on_volunteer = replace_linked_records_with_values(rows_on_volunteer)
        rows_on_volunteer = pd.DataFrame(rows_on_volunteer)
        rows_on_volunteer = rows_on_volunteer.drop(columns=['order'])
        rows_on_volunteer = arrays_to_strings(rows_on_volunteer)
    else:
        rows_on_volunteer = rows_on_tracker.iloc[0:0].copy()


    cols = list(set(rows_on_tracker.columns).intersection(rows_on_volunteer.columns))
    cols_wo_id = [c for c in cols if c!='id']
    merged = rows_on_tracker.merge(rows_on_volunteer,on=cols_wo_id,how="outer",indicator=True)
    ## if in both, don't have to do anything
    merged = merged[merged._merge!="both"]

    ## if in left, add to destination
    to_add = merged[merged._merge=="left_only"].id_x.to_list()
    to_add_rows = arrays_to_strings(rows_on_tracker[rows_on_tracker.id.isin(to_add)][cols].drop(columns=['id'])).to_dict(orient="records")

    for start in range(0, len(to_add_rows), CHUNK_SIZE):
        batch = to_add_rows[start:start + CHUNK_SIZE]

        response = requests.post(
            f"https://baserow.datarescueproject.org/api/database/rows/table/{t['destination']}/batch/?user_field_names=true",
            headers={
                "Authorization": f"Token {VOLUNTEER_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={"items": batch},
            timeout=300,
        )
        print(response.text)
        response.raise_for_status()
    
    ## if in right, delete from destination
    to_delete = merged[merged._merge=="right_only"].id_y.to_list()
    if len(to_delete) > 0:
        response = requests.post(
            f"https://baserow.datarescueproject.org/api/database/rows/table/{t['destination']}/batch-delete/",
            headers={
                "Authorization": f"Token {VOLUNTEER_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "items":to_delete
            },
            timeout=300
        )
        print(response.text)