# Data Rescue Project Portal

The portal is the public search and discovery interface for datasets archived by the [Data Rescue Project](https://www.datarescueproject.org/). Baserow is the canonical data source; this repository contains the site and the generated records used to build it.

## Repository map

| Path | Purpose |
| --- | --- |
| `content/` | Generated, tracked Jekyll collections for datasets, offices, and categories |
| `pages/` | Public page and JSON entry points |
| `_layouts/`, `_includes/` | Shared Jekyll presentation |
| `assets/` | CSS, images, and JavaScript source |
| `data/baserow/` | Committed CSV snapshots from Baserow |
| `scripts/data_pipeline/` | Snapshot fetching and content generation |
| `.github/workflows/` | Data synchronization, validation, and deployment |
| `docs/` | Architecture, development, and data-pipeline details |

## Development

Local development is Docker-only:

```sh
docker compose up --build
```

Open <http://localhost:4000>. See [development](docs/development.md), [architecture](docs/architecture.md), and [data pipeline](docs/data-pipeline.md) for details.
