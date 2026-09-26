# Running the validator in CI

The validator needs Python 3.9 or newer and nothing else. Run it from the repository root on every pull request.

## GitHub Actions

```yaml
  mirage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python3 .mirage/check.py check
```

Add this as a job in the existing workflow, or as `.github/workflows/mirage.yml` with `on: [pull_request]`.

## GitLab CI

```yaml
mirage:
  image: python:3.12-slim
  script:
    - python3 .mirage/check.py check
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

## Any other CI

Run `python3 .mirage/check.py check` in a job with Python 3.9 or newer. A non-zero exit fails the job.
