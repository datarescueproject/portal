# Docker development

Docker is the supported local development environment. It supplies the pinned Ruby runtime plus Node.js and Python dependencies.

## Start the site

```sh
docker compose up --build
```

The `site` service builds JavaScript and serves Jekyll at <http://localhost:4000>. The `assets` service watches JavaScript source files and rebuilds the bundle.

## Checks

Run the same focused checks used by CI:

```sh
docker compose run --rm site npm run lint
docker compose run --rm site python scripts/data_pipeline/generate_content.py --check
docker compose run --rm site bundle exec jekyll build
```

Build products and local dependency directories are ignored by Git. Stop the services with `docker compose down`; add `--volumes` only when the Node dependency volume needs to be recreated.
