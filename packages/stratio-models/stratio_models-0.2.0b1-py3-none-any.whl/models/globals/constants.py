from enum import Enum


class ClusterSizeEnum(str, Enum):
    L = "L"
    M = "M"
    S = "S"


class InstallationActionEnum(str, Enum):
    # installation states for the product lifecycle
    ACCOUNT_PENDING = "account-pending"
    ACCOUNT_IN_PROGRESS = "account-in-progress"
    ACCOUNT_CHECK = "check-account"
    INSTALL_IN_PROGRESS = "installation-in-progress"
    INSTALL_PENDING = "installation-pending"
    INSTALL_CHECK = "check-installation"
    UNINSTALL_PENDING = "uninstall-pending"
    UNINSTALL_IN_PROGRESS = "uninstall-in-progress"


class InstallationPhaseEnum(str, Enum):
    PROVISION_CLUSTER = "provision-cluster"
    INSTALL_KEOS = "install-keos"
    INSTALL_MONITORING = "install-monitoring"
    INSTALL_STRATIO = "install-stratio"


class ClusterStatusEnum(str, Enum):
    STARTED = "started"
    STOPPED = "stopped"


class ClusterActionEnum(str, Enum):
    START_PENDING = "start-pending"
    STOP_PENDING = "stop-pending"
    START_APPLICATIONS_PENDING = "start-applications-pending"
    START_CLUSTER_IN_PROGRESS = "start-cluster-in-progress"
    START_APPLICATIONS_IN_PROGRESS = "start-applications-in-progress"
    STOP_IN_PROGRESS = "stop-in-progress"
    START_CHECK = "check-start"
    STOP_CHECK = "check-stop"


class SubscriptionActionEnum(str, Enum):
    SUBSCRIBE_SUCCESS = "subscribe-success"
    UNSUBSCRIBE_PENDING = "unsubscribe-pending"
    SUBSCRIBE_FAIL = "subscribe-fail"
    UNSUBSCRIBE_SUCCESS = "unsubscribe-success"
