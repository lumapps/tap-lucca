"""Stream type classes for tap-lucca."""

from __future__ import annotations

from typing import ClassVar

import typing as t
from importlib import resources

from singer_sdk import typing as th, SchemaDirectory, StreamSchema

from tap_lucca import schemas
from tap_lucca.client import LuccaStream

SCHEMAS_DIR = SchemaDirectory(schemas)



class EmployeesStream(LuccaStream):
    name = "employees"
    path = "/lucca-api/employees"
    records_jsonpath = "$.items[*]"
    stream_params = {}

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)


class JobPositionsStream(LuccaStream):
    name = "job_positions"
    path = "/lucca-api/job-positions"
    records_jsonpath = "$.items[*]"
    stream_params = {}

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)


class DepartmentsStream(LuccaStream):
    name = "departments"
    path = "/lucca-api/departments"
    records_jsonpath = "$.items[*]"
    stream_params = {}

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)


class LegalEntitiesStream(LuccaStream):
    name = "legal_entities"
    path = "/lucca-api/legal-entities"
    records_jsonpath = "$.items[*]"
    stream_params = {}

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema: ClassVar[StreamSchema] = StreamSchema(SCHEMAS_DIR)