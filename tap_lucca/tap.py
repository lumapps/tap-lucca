"""Lucca tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_lucca import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapLucca(Tap):
    """Lucca tap class."""

    name = "tap-lucca"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Client ID",
            description="The client ID",
        ),
        th.Property(
            "client_secret",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Client secret",
            description="The client secret",
        ),
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            required=True,
            title="API URL",
            description="The API base URL",
        ),
        th.Property(
            "scopes",
            th.StringType(nullable=False),
            required=True,
            title="OAuth2 scopes",
            description="The OAuth2 scopes to use",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.LuccaStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.JobPositionsStream(self),
            streams.DepartmentsStream(self),
            streams.LegalEntitiesStream(self),
        ]


if __name__ == "__main__":
    TapLucca.cli()
