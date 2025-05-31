# analyze-activities

activity data from different hobbies/source are converted into a common json format:
key: date, value=list(title)

```json
{
  "2025-01-01": [
    "00:00 New Year",
    "09:47 Wake up",
    "09:34 Jogging in the Snow (65 min)",
    "Some text without a time."
  ]
}
```

## Calender appointments

1. export calendar in ics format
2. run [cal.py](src/cal.py) to convert into `data/cal.json`

format: `HH:MM TITLE`

## Git commits

1. run [git_1_export_history.sh](src/git_1_export_history.sh) to extract commit data from all repos to `data/git/*.log`
2. run [git_2_analyze.py](src/git_2_analyze.py) to convert into  `data/git.json`

format: `HH:MM Coding at REPO: COMMIT_TITLE`

## Oura ring sleep times

1. download [sleep.csv](https://cloud.ouraring.com/account/export/sleep/csv) to `data/oura/sleep.csv`
2. run [oura.py](src/oura.py) to convert into `data/oura.json`

format: `HH:MM Start sleep` and `HH:MM Wake up`

## Strava activities

1. export ics list of activities via <https://entorb.net/strava-streamlit/> -> "Cal Export" to `data/strava/Strava_Activity_Calendar.ics`
2. run [strava.py](src/strava.py) to convert into `data/strava.json`

format: `HH:MM TYPE: TITLE (MINUTES)`

## TODO: Diary/Journal

## Tools

### Pytest unit tests

```sh
pytest tests/ --cov --cov-report=html:coverage_report
```

### Ruff formatter and linter

```sh
ruff check
ruff format
```

### Pre-commit code checker

(also runs Ruff and CSpell)

```sh
pre-commit run --all-files
```

### GitHub Action Workflow

[check.yml](.github/workflows/check.yml) runs pytest, pre-commit, sonarqube

### SonarQube Code Analysis

See report at [sonarcloud.io](https://sonarcloud.io/summary/overall?id=entorb_analyze-activities&branch=main)
