"""Tests for Licence interactions."""
import unittest.mock

import hypothesis
import hypothesis.strategies
import pytest
import requests

import templatise.licence as sut


def licence_responses(
    status_code: hypothesis.strategies.SearchStrategy[
        int
    ] = hypothesis.strategies.integers(min_value=100, max_value=599)
) -> hypothesis.strategies.SearchStrategy[requests.Response]:
    """Hypothesis strategy for requests.Response."""

    def construct_response(status_code: int) -> requests.Response:
        result = requests.Response()
        result.status_code = status_code
        return result

    return hypothesis.strategies.builds(construct_response, status_code=status_code)


class TestLicenceText:
    """Tests for licence downloading."""

    @pytest.mark.skip()  # type: ignore[misc]
    @hypothesis.given(  # type: ignore[misc]
        response=licence_responses(
            status_code=hypothesis.strategies.integers(min_value=300, max_value=399)
        )
    )
    def test_3xx_responses(self, response: requests.Response) -> None:
        """Test 3xx classes of HTTP responses."""

    @hypothesis.given(  # type: ignore[misc]
        response=licence_responses(
            status_code=hypothesis.strategies.integers(min_value=400, max_value=499)
        )
    )
    def test_4xx_responses(self, response: requests.Response) -> None:
        """Test 4xx classes of HTTP responses."""
        with unittest.mock.patch.object(
            sut.requests, "get", return_value=response  # type: ignore[attr-defined]
        ) as mock_requests_get:
            with pytest.raises(sut.InvalidError):
                sut.text(name="ignored")  # pylint: disable=W0212
            mock_requests_get.assert_called_once()

    @hypothesis.given(  # type: ignore[misc]
        response=licence_responses(
            status_code=hypothesis.strategies.integers(min_value=500, max_value=599)
        )
    )
    def test_5xx_responses(self, response: requests.Response) -> None:
        """Test 5xx classes of HTTP responses."""
        with unittest.mock.patch.object(
            sut.requests, "get", return_value=response  # type: ignore[attr-defined]
        ) as mock_requests_get:
            with pytest.raises(sut.UnavailableError):
                sut.text(name="ignoed")  # pylint: disable=W0212
            assert mock_requests_get.call_count == 2  # nosec
