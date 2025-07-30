# -*- coding: utf-8 -*-

"""
Improve the original redshift-serverless boto3 client.
"""

import typing as T

import botocore.exceptions
from func_args.api import REQ, OPT, remove_optional

from .model_redshift_serverless import (
    RedshiftServerlessNamespace,
    RedshiftServerlessNamespaceIterProxy,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_redshift_serverless.client import RedshiftServerlessClient


def list_namespaces(
    redshift_serverless_client: "RedshiftServerlessClient",
    page_size: int = 100,
    max_items: int = 9999,
) -> RedshiftServerlessNamespaceIterProxy:
    """
    Ref:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListNamespaces.html
    """

    # inner generator function to yield objects
    def func():
        paginator = redshift_serverless_client.get_paginator("list_namespaces")
        response_iterator = paginator.paginate(
            PaginationConfig={
                "MaxItems": max_items,
                "PageSize": page_size,
            }
        )
        for response in response_iterator:
            for dct in response.get("namespaces", []):
                yield RedshiftServerlessNamespace(raw_data=dct)

    # return an iterproxy object that wraps the generator
    return RedshiftServerlessNamespaceIterProxy(func())


def get_namespace(
    redshift_serverless_client: "RedshiftServerlessClient",
    namespace_name: str,
) -> T.Optional[RedshiftServerlessNamespace]:
    """
    Ref:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_namespace.html
    """
    try:
        response = redshift_serverless_client.get_namespace(
            namespaceName=namespace_name,
        )
        return RedshiftServerlessNamespace(raw_data=response["namespace"])
    except botocore.exceptions.ClientError as e:
        # return None if the namespace does not exist
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            return None
        else:  # pragma: no cover
            raise


def delete_namespace(
    redshift_serverless_client: "RedshiftServerlessClient",
    namespace_name: str,
    final_snapshot_name: T.Optional[str] = None,
    final_snapshot_retention_period: T.Optional[int] = None,
) -> T.Optional[RedshiftServerlessNamespace]:
    """
    Ref:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/delete_namespace.html
    """
    try:
        response = redshift_serverless_client.delete_namespace(
            **remove_optional(
                namespaceName=namespace_name,
                finalSnapshotName=final_snapshot_name,
                finalSnapshotRetentionPeriod=final_snapshot_retention_period,
            ),
        )
        return RedshiftServerlessNamespace(raw_data=response["namespace"])
    except botocore.exceptions.ClientError as e:
        # return None if the namespace does not exist
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            return None
        else:  # pragma: no cover
            raise
