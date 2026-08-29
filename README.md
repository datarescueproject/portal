# Data Rescue Project Portal

![Homepage](https://github.com/datarescueproject/portal/blob/main/assets/images/DRP_Portal_homepage.png)

The portal is the public search and discovery interface for datasets archived by the [Data Rescue Project](https://www.datarescueproject.org/). Baserow is the canonical data source; this repository contains the site and the generated records used to build it.

This is very much a work-in-progress, and any help with improving this interface would be much appreciated. Feel free to create issues if you notice any bugs and PRs are welcome.

The protal was built using [JKAN](https://jkan.io), a lightweight, backend-free open data portal, powered by Jekyll developed by Tim Wisniewski.

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
