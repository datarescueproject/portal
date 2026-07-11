import requests
import pandas as pd
from datetime import date, timedelta
import json

BASEROW_ACCESS_TOKEN = os.environ.get("BASEROW_ACCESS_TOKEN")

def get_URLs_from_dist(arr):
    urls = []
    if arr:
        for a in arr:
            try: 
                urls.append(a['accessURL'])
            except:
                pass
            try: 
                urls.append(a['downloadURL'])
            except:
                pass
    
    urls = list(set(urls))
    if len(urls) > 0:
        url_out = ", ".join(urls)
    else:
        url_out = ""
    return url_out


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

## Fetching the datasets not on data.gov any longer
try:
    resp = requests.get(url="https://findgovdata.org/files/last_seen.json")

    data_gov_missing = pd.DataFrame(resp.json()['documents'])
    metadata = pd.json_normalize(data_gov_missing['metadata'])
    df_expanded = data_gov_missing.drop(columns=['metadata']).join(metadata)
    df_expanded = df_expanded[['id', 'name', 'description',
    'organization_type', 'organization_name', 'publisher', 
    'last_seen', 'dcat.landingPage','distribution_count',
    'dcat.distribution']]

    df_expanded['dcat.distribution'] = df_expanded['dcat.distribution'].fillna("")
    df_expanded['dcat.landingPage'] = df_expanded['dcat.landingPage'].fillna("")
    df_expanded['download_urls'] = df_expanded['dcat.distribution'].apply(get_URLs_from_dist)

    df_expanded['last_seen'] = pd.to_datetime(df_expanded['last_seen'], format='ISO8601')
    df_expanded['last_seen'] = df_expanded['last_seen'].dt.date

    df_expanded = df_expanded.drop(columns=['dcat.distribution','distribution_count']).rename(columns={'dcat.landingPage':'source_url','id':'hashed_id'})
    df_expanded.last_seen = df_expanded.last_seen.astype('str')

    ## Fetching the datasets already added to baserow
    rows_on_baserow = get_results_json("https://baserow.datarescueproject.org/api/database/rows/table/1054/?user_field_names=true")
    rows_on_baserow = pd.DataFrame(rows_on_baserow)
    rows_on_baserow = rows_on_baserow.drop(columns=['order'])
    rows_to_add = df_expanded[~df_expanded.hashed_id.isin(rows_on_baserow.hashed_id)]
    rows_to_add_json = rows_to_add.to_dict(orient='records')
    
    ## Posting rows to baserow table
    for r in rows_to_add_json:
        requests.post(
        "https://baserow.datarescueproject.org/api/database/rows/table/1054/?user_field_names=true",
        headers={
            "Authorization": "Token {BASEROW_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        },
        json=r
        )

    print(f"{len(rows_to_add_json)} rows added to Baserow table")
    
    ## Check if any datasets previously marked as missing from data.gov are back
    rows_to_toggle_status = rows_on_baserow[~rows_on_baserow.hashed_id.isin(df_expanded.hashed_id)]
    rows_to_toggle_status = rows_to_toggle_status[rows_to_toggle_status.status == "Missing from data.gov"]

    if(len(rows_to_toggle_status)) > 0:
        for i in rows_to_toggle_status.id:
            requests.patch(
                "https://baserow.datarescueproject.org/api/database/rows/table/1054/{i}/?user_field_names=true",
                headers={
                    "Authorization": "Token {BASEROW_ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "status":"Returned to data.gov",
                    "last_seen": str(date.today())
                }
            )
        print(f"{len(rows_to_toggle_status)} rows marked as returned in Baserow table")

    ## Check if any datasets previously marked as returned are missing again
    status_returned = rows_on_baserow[rows_on_baserow.status == "Returned to data.gov"]
    status_returned_to_toggle = status_returned[~status_returned.hashed_id.isin(df_expanded.hashed_id)]
    
    if(len(status_returned_to_toggle)) > 0:
        for i in status_returned_to_toggle.id:
            requests.patch(
                "https://baserow.datarescueproject.org/api/database/rows/table/1054/{i}/?user_field_names=true",
                headers={
                    "Authorization": "Token {BASEROW_ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "status":"Missing from data.gov",
                    "last_seen": str(date.today()-timedelta(days=1))
                }
            )
        print(f"{len(status_returned_to_toggle)} rows marked once again as missing in Baserow table")
    

except Exception as e:
    print(e)
    