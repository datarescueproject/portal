# Architecture

The portal is a Jekyll static site with a small JavaScript layer for client-side searching, filtering, and pagination. GitHub Actions builds and deploys it to GitHub Pages.

## Data flow

```text
Baserow
  -> data/baserow/*.csv
  -> scripts/data_pipeline/generate_content.py
  -> content/_datasets, content/_organizations, content/_dataset_categories
  -> Jekyll
  -> _site
```

Baserow is the editable source of truth. CSV snapshots and generated Markdown are committed so each deployment is reproducible and records can be inspected on GitHub. Generated collection files should not be edited manually.

## Site structure

- `pages/` defines the homepage, listing pages, status page, the lightweight `/datasets.json` search index, and the complete `/datasets-full.json` export.
- `content/` contains the three Jekyll collections. The `collections_dir` setting groups them without changing their public URLs.
- `_layouts/` and `_includes/` render collection records and shared page chrome.
- `assets/js/src/` contains component-oriented JavaScript. Parcel writes the ignored production bundle to `assets/js/dist/`.
- `assets/css/` and `assets/images/` contain static presentation assets.

Public dataset, category, and office URLs are controlled in `_config.yml`. The browser-facing `/datasets.json` contains only the fields needed by the listing interface. `/datasets-full.json` exposes every generated dataset and resource field for external consumers, while full record details are also rendered into dataset pages during the Jekyll build.
