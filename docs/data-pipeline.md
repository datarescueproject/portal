# Data pipeline

Baserow is the canonical source for portal records. The committed CSV snapshots and Markdown collections are derived data.

## Synchronize content

The scheduled **Sync Baserow content** workflow:

1. fetches the four Baserow tables into `data/baserow/`;
2. regenerates datasets, organizations, and categories under `content/`;
3. commits both layers together in one commit; and
4. triggers a GitHub Pages deployment after a successful run.

To perform the same operation locally:

```sh
docker compose run --rm -e BASEROW_ACCESS_TOKEN site \
  python scripts/data_pipeline/fetch_baserow.py
docker compose run --rm site \
  python scripts/data_pipeline/generate_content.py
```

Review the resulting CSV and Markdown diff together before committing.

## Generated-content rules

- Do not manually edit files below `content/_datasets/`, `content/_organizations/`, or `content/_dataset_categories/`.
- Generation uses only the local committed snapshots; it does not download CSV files from GitHub.
- Output filenames and category ordering are deterministic.
- Generation removes records no longer present in the snapshots.
- Writes are atomic per file, so an interrupted write cannot leave a partial record.
- CI runs `generate_content.py --check` and fails when generated content is missing, stale, or modified.

The separate **Sync missing government data** workflow updates the operational missing-data table in Baserow. It does not create portal files.
