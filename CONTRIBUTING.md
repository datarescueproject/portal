# Contributing

To run the site locally, see the [JKAN instructions](https://github.com/timwis/jkan/blob/main/docs/running-locally.md).

## Linting

Install the frontend dependencies and run the JavaScript and CSS checks:

```sh
npm ci
npm run lint
```

Use `npm run lint:fix` to apply safe automatic fixes. The pull-request workflow runs these checks before the repository-wide MegaLinter job.
