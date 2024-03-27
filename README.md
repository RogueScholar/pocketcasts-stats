<!--
SPDX-FileCopyrightText: © 2018-2020, Niklas Heer <me@nheer.io>
SPDX-FileCopyrightText: 🄯 2024, Peter J. Mello <admin@petermello.net>

SPDX-License-Identifier: MIT
-->
<h2 align="center">Pocket Casts statistics</h2>

<p align="center">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="https://codecov.io/gh/RogueScholar/pocketcasts-stats"><img src="https://codecov.io/gh/RogueScholar/pocketcasts-stats/branch/master/graph/badge.svg" /></a>
  <a href="https://pyup.io/repos/github/RogueScholar/pocketcasts-stats/"><img src="https://pyup.io/repos/github/RogueScholar/pocketcasts-stats/shield.svg" alt="Updates" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

Fetch your Pocket Casts statistics and put them into Airtable with
[about 80 lines](#lines-of-code) of code. :tada:

## Configuration

### Airtable

[![PocketCasts statistics](https://raw.github.com/RogueScholar/pocketcasts-stats/master/.github/img/screenshot_01.png "Airtable Dashboard")]()

For this tool to work you'll need a
[free Airtable account](https://airtable.com/invite/r/V2q23fXk). If you don't
have one - [make one](https://airtable.com/invite/r/V2q23fXk).

1. Go to this example base: <https://airtable.com/shryxs3YOERmBeHl1>
1. Click on `Copy base` in the upper-right corner of the page.
1. Once copied, delete all of the example records.
1. Click on your avatar in the upper-right corner of the page and select
   `Account`.
1. On the account page, click on `Generate API key` on the right side under API.
   - Save the key and for use later as the `AIRTABLE_API_KEY` variable value.
1. Go to this page and select your copied base: <https://airtable.com/api>
1. Select `AUTHENTICATION` on the left side of the page.
1. On the right side there should be a dark area with text that resembles this:
   - `$ curl https://api.airtable.com/v0/appr9hgXPZbBPqV4n/PocketCasts?api_key=YOUR_API_KEY`
   - Save the part after `v0/` until the following `/` for later use (here, it
	 would be `appr9hgXPZbBPqV4n`) as the `AIRTABLE_BASE_ID` value.
1. Proceed to the directions in the section directly below.

### Gitlab

For this to work, you'll need a free Gitlab.com account. If you don't have one -
make one.

1. Make a new project on [Gitlab.com](https://gitlab.com).
1. Import this repository as the base for your project.
1. Setup all environment variables in the project.
   - Go to `Settings` > `CI / CD` on the left side of the repository settings.
   - Insert variables under `Variables` (click expand, also see `Environment
	 variables`)
1. Setup the Pipeline Scheduler.
   - Go to `CI / CD` > `Schedules` on the left side of the page.
   - Click the green button on the right labelled `New schedule`.
   - Give it a description, such as "Get new stats every 2h".
   - Select `Custom ( Cron syntax )` where it asks for an `Interval Pattern`.
   - Insert the following into the field: `0 */2 * * *` (this is a Cron syntax
	 instruction to run every two hours, seven days a week).
   - Make sure that the `Target Branch` selected is your `master` branch.
   - Make sure the `Active` option is checked.
   - Click the `Save pipeline schedule` button.
1. Profit! :)

### Environment variables

- `POCKETCASTS_EMAIL` - the email address you login to Pocket Casts with
- `POCKETCASTS_PASSWORD` - your Pocket Casts password
- `AIRTABLE_BASE_ID` - the ID of the Airtable base which will store the data
- `AIRTABLE_API_KEY` - your Airtable account API key
- `AIRTABLE_POCKETCASTS_TABLE` - the table to store the Pocket Casts data

> [!IMPORTANT]
> You cannot use special characters like `.!$/\|` in environment variable names!

## Local testing

1. Copy the `.env_example` file and name it `pocketcasts-stats.env`.
1. Edit the `pocketcasts-stats.env` file and fill in your credentials as
   mentioned above in **[Environment variables](#environment-variables)**.
1. Test the project using Docker with the `make` command.
1. Profit! :)

## Contributing

Please make sure you run [`black`](https://github.com/ambv/black) on your code
before you commit it!

## Lines of code

This project uses about 80 lines of code according to
[`cloc`](https://github.com/AlDanial/cloc):

```console
➜ cloc app.py .gitlab-ci.yml
       2 text files.
       2 unique files.
       0 files ignored.

github.com/AlDanial/cloc v1.80  T=0.01s (157.1 file, 12570.7 lines)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           1             28             43             70
YAML                             1              4              0             15
-------------------------------------------------------------------------------
SUM:                             2             32             43             85
-------------------------------------------------------------------------------
```

## Attribution

- [Pocket Casts](https://www.pocketcasts.com/) for being an awesome podcast
  player!
- [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper),
  an awesome library to connect to Airtable.
- [furgoose/Pocket-Casts](https://github.com/furgoose/Pocket-Casts), a good
  reference for how to query the Pocket Casts API.
- [Airtable](https://airtable.com/invite/r/V2q23fXk), for being an awesome tool!
- [GitLab](https://gitlab.com) and `GitLabCI`, for being an all-in-one solution.
- Gitlab Scheduler for Pipelines, because without it you would need a server.
- [gitmoji](https://gitmoji.carloscuesta.me/), for better understandable commits
  through emojis. :tada:
- [pylama](https://github.com/klen/pylama), for checking code quality.
- [pytest](https://github.com/pytest-dev/pytest), for being an awesome testing
  framework.
- [pytest-cov](https://github.com/pytest-dev/pytest-cov), for generating
  coverage reports.
- [black](https://github.com/ambv/black), an awesome code formatter for Python.
- [codecov](https://codecov.io), for showing the code coverage and helping
  improve it.
- [PyUp.io](https://pyup.io/), for helping to keep this project secure.
- [codacy](https://app.codacy.com), for helping improve the code quality.
