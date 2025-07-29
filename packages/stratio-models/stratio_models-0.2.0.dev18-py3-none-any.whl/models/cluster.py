# src/stratio/api/models/cluster.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.dynamodb import DynamoModel
from models.globals import (
    ClusterActionEnum,
    ClusterSizeEnum,
    ClusterStatusEnum,
    InstallationActionEnum,
    InstallationPhaseEnum,
)


class EC2Item(BaseModel):
    # mandatory attributes
    ImageId: str
    InstanceId: str
    InstanceType: str
    State: dict

    # optional attributes
    VpcId: Optional[str] = None
    SubnetId: Optional[str] = None
    LaunchTime: Optional[datetime] = None
    Placement: Optional[dict] = None
    Tags: Optional[list[dict]] = None


class EKSItem(BaseModel):
    # mandatory attributes
    name: str
    arn: str
    createdAt: datetime
    version: str
    roleArn: str
    status: str
    # optional attributes
    endpoint: Optional[str] = None
    health: Optional[dict] = None
    platformVersion: Optional[str] = None


class ClusterBase(BaseModel):
    """
    Base representation of a cluster.
    """

    # mandatory attributes
    customerIdentifier: str
    clusterIdentifier: str

    # optional attributes
    provisionedAccountId: Optional[str] = None
    adminEmail: Optional[str] = None
    installationAction: Optional[InstallationActionEnum] = None
    installationRegion: Optional[str] = None
    installationPhase: Optional[InstallationPhaseEnum] = None
    clusterStatus: Optional[ClusterStatusEnum] = None
    clusterAction: Optional[ClusterActionEnum] = None
    created: Optional[str] = None
    k8sVersion: Optional[str] = None
    keosVersion: Optional[str] = None
    universeVersion: Optional[str] = None
    successfullyInstalled: Optional[bool] = None
    bucketSecretArn: Optional[str] = None


class Cluster(ClusterBase, DynamoModel):
    """
    Cluster-hub representation of a cluster.
    """

    # Required fields
    adminEmail: str
    adminUsername: str
    productCode: str
    # Optional fields
    clusterName: Optional[str] = None
    clusterUrl: Optional[str] = None
    description: Optional[str] = None
    installationClusterSize: Optional[ClusterSizeEnum] = None
    bucketAccessKey: Optional[str] = None


class ClusterMetadata(ClusterBase):
    """
    Metadata representation of a cluster, used alog with AWS stacks.
    """

    tableName: Optional[str] = None


class Infrastructure(BaseModel):
    """
    Infrastructure representation of a cluster, used to store items for a particular stack.
    """

    metadata: ClusterMetadata
    eks: Optional[EKSItem] = None
    ec2: list[EC2Item]


class InfrastructureList(BaseModel):
    """
    List representation of infrastructures, used to store multiple clusters' metadata.
    """

    source: str
    items: list[ClusterMetadata]
    error: Optional[str] = None
