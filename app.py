# SPDX-FileCopyrightText: © 2018-2019, Niklas Heer <me@nheer.io>
# SPDX-FileCopyrightText: 🄯 2024, Peter J. Mello <admin@petermello.net>
#
# SPDX-License-Identifier: MIT
"""Retrieve listening statistics from the Pocket Casts API and print as JSON."""
import json

from airtable import Airtable
from environs import Env
from requests import RequestException, request


def get_statistics(username: str, password: str) -> dict:
    """Gets the user statistics from the Pocket Casts API.

    Parameters
    ----------
    username : str
        Your login email address for PocketCasts.
    password : str
        Your login password for PocketCasts.

    Returns
    -------
    A dict of all the statistics about the user's profile.
    """

    # Login and get a token from Pocket Casts.
    login_url = "https://api.pocketcasts.com/user/login"
    data = f'{{"email":"{username}","password":"{password}","scope":"webplayer"}}'
    headers = {"Origin": "https://play.pocketcasts.com"}
    response = request(
        method="POST", url=login_url, data=data, headers=headers, timeout=30
    ).json()

    if "message" in response:
        raise RequestException("Login failed.")
    else:
        token = response["token"]

    # Get the statistics through the Pocket Casts API.
    req = request(
        method="POST",
        url="https://api.pocketcasts.com/user/stats/summary",
        timeout=30,
        data=("{}"),
        headers={
            "Authorization": f"Bearer {token}",
            "Origin": "https://play.pocketcasts.com",
            "Accept": "*/*",
        },
    )

    if not req.ok:
        raise RequestException("Invalid request.")

    return req.json()


def enrich_with_delta(record: dict, previous_record: dict) -> dict:
    """Enriches a record with delta time fields.

    Parameters
    ----------
    record : dict
        The statistics record from Pocket Casts as a dict.
    previous_record : dict
        The most current record in Airtable.

    Returns
    -------
    An dict with the calculated time deltas using the previous record.
    """
    enriched_record = dict(record)

    # Calculate time deltas for all keys in stats.
    for key, _ in record.items():
        enriched_record[f"Delta ({key})"] = record[key] - previous_record[key]

    return enriched_record


# Handle environment variables.
env = Env()
env.read_env()

# Read logging overrides from environment variables for local development.
DEBUG = env.bool("DEBUG", default=False)
INFO = env.bool("INFO", default=False)

##############################
# PocketCasts
##############################

# Get the statistics from Pocket Casts.
record = get_statistics(env("POCKETCASTS_EMAIL"), env("POCKETCASTS_PASSWORD"))

# Delete the start date because we don't need it.
del record["timesStartedAt"]

# Convert everything to integers.
record = dict((k, int(v)) for k, v in record.items())

##############################
# Airtable
##############################

# The API key for Airtable is provided by the  AIRTABLE_API_KEY variable.
airtable = Airtable(env("AIRTABLE_BASE_ID"), env("AIRTABLE_POCKETCASTS_TABLE"))

# Get previous record to calculate delta(s)
previous_record = airtable.get_all(
    view="data",
    maxRecords=1,
    sort=[("#No", "desc")],
    fields=[
        "Delta (timeSilenceRemoval)",
        "Delta (timeSkipping)",
        "Delta (timeIntroSkipping)",
        "Delta (timeVariableSpeed)",
        "Delta (timeListened)",
        "timeSilenceRemoval",
        "timeSkipping",
        "timeIntroSkipping",
        "timeVariableSpeed",
        "timeListened",
    ],
)

# Check if this is the first time we are running.
if previous_record:
    # Enrich record with delta data.
    record = enrich_with_delta(record, previous_record[0]["fields"])

    # Allow an environment variable to omit the step of writing to the database.
    if not DEBUG:
        # Insert new record into Airtable, but we need to be sure we want it.
        if (
            previous_record[0]["fields"] != record
            and record["Delta (timeListened)"] != 0
        ):
            airtable.insert(record)
            if INFO:
                print("[INFO] Written new entry to Airtable.")
        else:
            if INFO:
                print("[INFO] Skip writing empty entry.")
else:
    # This is the first run.
    record = enrich_with_delta(record, record)

    if not DEBUG:
        airtable.insert(record)
        if INFO:
            print("[INFO] Written the first entry to Airtable.")

# Print the data
print(json.dumps(record, sort_keys=True, indent=4))
