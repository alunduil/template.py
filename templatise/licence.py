"""Licence interactions."""
import datetime
import logging

import requests
import retry

_LOGGER = logging.getLogger(__name__)


class InvalidError(RuntimeError):
    """Indicates an invalid licence was specified."""


class UnavailableError(RuntimeError):
    """Indicates licence information is not available."""


def text(licence_id: str) -> str:
    """Full text for Licence with name."""
    licence_text = _download(licence_id)
    if licence_text is None:
        raise RuntimeError(f"Could not find licence text for {licence_id}.")
    return licence_text


@retry.retry(UnavailableError, tries=2, logger=_LOGGER)
def _download(licence_id: str) -> str:
    response = requests.get(
        url=f"https://spdx.org/licenses/{licence_id}.json",
        timeout=datetime.timedelta(minutes=1).total_seconds(),  # nosec
    )

    if response.status_code in range(400, 500):
        raise InvalidError(f"Requested {licence_id}, but recieved {response}.")

    if response.status_code in range(500, 600):
        raise UnavailableError(f"Requested {licence_id}, but received {response}.")

    return str(response.json()["licenseText"])
