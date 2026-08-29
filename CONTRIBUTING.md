# Contributing

Use the Docker workflow described in [docs/development.md](docs/development.md). Site content is generated from Baserow, so changes to dataset, office, or category records must be made at the source and synchronized through the data pipeline.

Before opening a pull request, run:

```sh
docker compose run --rm site npm run lint
docker compose run --rm site python scripts/data_pipeline/generate_content.py --check
docker compose run --rm site bundle exec jekyll build
```

Pull requests run these checks again in CI.
