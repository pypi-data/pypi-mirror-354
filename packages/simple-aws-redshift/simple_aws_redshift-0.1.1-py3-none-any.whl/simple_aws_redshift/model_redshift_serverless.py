# -*- coding: utf-8 -*-

"""
Redshift Serverless Data Models.
"""

import typing as T
import dataclasses
import datetime

from func_args.api import T_KWARGS, REQ
from iterproxy import IterProxy

from .model import Base

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_redshift_serverless.type_defs import (
        NamespaceTypeDef,
        NamespaceStatusType,
    )


@dataclasses.dataclass
class RedshiftServerlessNamespace(Base):
    """
    Redshift Serverless Namespace object.

    Ref:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_namespace.html
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/list_namespaces.html

    :param _data: The raw data from the API response, stored as a dictionary.
    """

    raw_data: "NamespaceTypeDef" = dataclasses.field(default=REQ)

    @property
    def admin_password_secret_arn(self) -> T.Union[str]:
        return self.raw_data.get("adminPasswordSecretArn")

    @property
    def admin_password_secret_kms_key_id(self) -> T.Optional[str]:
        return self.raw_data.get("adminPasswordSecretKmsKeyId")

    @property
    def admin_username(self) -> T.Optional[str]:
        return self.raw_data.get("adminUsername")

    @property
    def creation_date(self) -> T.Optional[datetime.datetime]:
        return self.raw_data.get("creationDate")

    @property
    def db_name(self) -> T.Optional[str]:
        return self.raw_data.get("dbName")

    @property
    def default_iam_role_arn(self) -> T.Optional[str]:
        return self.raw_data.get("defaultIamRoleArn")

    @property
    def iam_roles(self) -> T.Optional[T.List[str]]:
        return self.raw_data.get("iamRoles")

    @property
    def kms_key_id(self) -> T.Optional[str]:
        return self.raw_data.get("kmsKeyId")

    @property
    def log_exports(self) -> T.Optional[T.List[str]]:
        return self.raw_data.get("logExports")

    @property
    def namespace_arn(self) -> T.Optional[str]:
        return self.raw_data.get("namespaceArn")

    @property
    def namespace_id(self) -> T.Optional[str]:
        return self.raw_data.get("namespaceId")

    @property
    def namespace_name(self) -> T.Optional[str]:
        return self.raw_data.get("namespaceName")

    @property
    def status(self) -> "NamespaceStatusType":
        return self.raw_data["status"]

    @property
    def core_data(self) -> T_KWARGS:
        return {
            "namespace_name": self.namespace_name,
            "namespace_id": self.namespace_id,
            "namespace_arn": self.namespace_arn,
            "status": self.status,
            "creation_date": self.creation_date,
        }

    @property
    def is_available(self) -> bool:
        return self.status == "AVAILABLE"

    @property
    def is_modifying(self) -> bool:
        return self.status == "MODIFYING"

    @property
    def is_deleting(self) -> bool:
        return self.status == "DELETING"


class RedshiftServerlessNamespaceIterProxy(IterProxy[RedshiftServerlessNamespace]):
    pass
