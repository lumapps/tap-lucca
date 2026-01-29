"""REST client handling, including LuccaStream base class."""

from __future__ import annotations

import decimal
import sys
import typing as t
from importlib import resources


from tap_lucca.auth import LuccaAuthenticator

from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BaseHATEOASPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

import logging

from urllib.parse import parse_qsl

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class LuccaPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        data = response.json()
        return data.get("links", {}).get("next", {}).get("href")
    
    def get_previous_url(self, response):
        data = response.json()
        return data.get("links", {}).get("prev", {}).get("href")
    
    def has_more(self, response: requests.Response):
        data = response.json()
        next = data.get("links", {}).get("next")
        return next is not None

class LuccaStream(RESTStream):
    """Lucca stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$.items[*]"

    stream_params :dict = {}

    page_size = 100

    @override
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return self.config["api_url"]

    @override
    @property
    def authenticator(self) -> OAuthAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return LuccaAuthenticator(
            self,
            auth_endpoint=f"{self.url_base}/connect/token",
            oauth_scopes=self.config["scopes"],
            default_expiration=1200,
            oauth_headers={
                "Host": "accounts.world.luccasoftware.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "Api-Version": "2024-11-01",
                },
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
        )


    @property
    @override
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return {
            "Api-Version": "2024-11-01"
        }

    @override
    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        return LuccaPaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = self.stream_params
        params["include"] = "totalCount,links"
        params["limit"] = self.page_size

        # Next page token is a URL, so we can to parse it to extract the query string

        if next_page_token:
            return dict(parse_qsl(next_page_token.query))
    
        # if self.replication_key:
        #     params["sort"] = "asc"
        #     params["order_by"] = self.replication_key

        return params

    @override
    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    @override
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    @override
    def post_process(
        self,
        row: dict,
        context: Context | None = None,
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Note: As of SDK v0.47.0, this method is automatically executed for all stream types.
        You should not need to call this method directly in custom `get_records` implementations.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
