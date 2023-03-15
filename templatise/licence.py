"""Licence interactions."""
import datetime
import logging
import typing

import bs4
import requests
import retry

_LOGGER = logging.getLogger(__name__)


class InvalidError(RuntimeError):
    """Indicates an invalid licence was specified."""


class UnavailableError(RuntimeError):
    """Indicates licence information is not available."""


def text(name: str) -> str:
    """Full text for Licence with name."""
    response = _download(name)
    maybe_text = _extract(response.text)
    if maybe_text is None:
        raise RuntimeError(f"Could not find licence text in {response.url}.")
    return maybe_text


@retry.retry(UnavailableError, tries=2, logger=_LOGGER)
def _download(name: str) -> requests.Response:
    url = f"https://opensource.org/licenses/{name}"
    response = requests.get(
        url, timeout=datetime.timedelta(minutes=1).total_seconds()  # nosec
    )
    if response.status_code in range(400, 500):
        raise InvalidError(f"Requested {name}, but recieved {response}.")
    if response.status_code in range(500, 600):
        raise UnavailableError(f"Requested {name}, but received {response}.")

    return response


def _extract(html: str) -> typing.Optional[str]:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    result = soup.find(name="div", id="LicenseText")
    if not result:
        result = soup.find(name="article")
    return result.text.strip() if result is not None else None
