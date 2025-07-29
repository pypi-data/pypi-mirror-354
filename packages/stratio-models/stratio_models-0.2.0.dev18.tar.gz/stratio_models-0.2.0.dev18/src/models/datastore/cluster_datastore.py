# src/models/datastore/cluster_datastore.py
import re

from ..globals import ClusterActionEnum, InstallationActionEnum


class ClusterChange:
    def __init__(self, old_image, new_image):
        self.old_image = old_image
        self.new_image = new_image
        self.customer_identifier = self._get_value_from_image(new_image, "customerIdentifier")
        self.cluster_identifier = self._get_value_from_image(new_image, "clusterIdentifier")
        self.installation_region = self._get_value_from_image(new_image, "installationRegion")

        self.old_installation_action = self._get_value_from_image(old_image, "installationAction")
        self.old_cluster_action = self._get_value_from_image(old_image, "clusterAction")
        self.old_cluster_status = self._get_value_from_image(old_image, "clusterStatus")

        self.new_installation_action = self._get_value_from_image(new_image, "installationAction")
        self.new_cluster_action = self._get_value_from_image(new_image, "clusterAction")
        self.new_cluster_status = self._get_value_from_image(new_image, "clusterStatus")

    def __str__(self):
        return (
            f"ClusterChange(customer_id={self.customer_identifier}, "
            f"old_image={self.old_image}, "
            f"new_image={self.new_image})"
        )

    def __repr__(self):
        return self.__str__()

    def has_changed(self) -> bool:
        return self.old_image != self.new_image

    def old_contains(self, field_name: str) -> bool:
        return field_name in self.old_image

    def new_contains(self, field_name: str) -> bool:
        return field_name in self.new_image

    def installation_changed(self) -> bool:
        return self.old_installation_action != self.new_installation_action

    def cluster_changed(self) -> bool:
        return self.old_cluster_action != self.new_cluster_action

    def is_install_pending(self):
        return re.match(rf"{InstallationActionEnum.INSTALL_PENDING.value}", self.new_installation_action)

    def is_uninstall_pending(self):
        return re.match(rf"{InstallationActionEnum.UNINSTALL_PENDING.value}", self.new_installation_action)

    def is_account_pending(self):
        return InstallationActionEnum.ACCOUNT_PENDING.value in self.new_installation_action

    def is_start_stop_pending(self):
        return re.match(
            rf"{ClusterActionEnum.STOP_PENDING.value}|{ClusterActionEnum.START_PENDING.value}", self.new_cluster_action
        )

    def is_start_pending(self):
        return re.match(rf"{ClusterActionEnum.START_PENDING.value}", self.new_cluster_action)

    def is_stop_pending(self):
        return re.match(rf"{ClusterActionEnum.STOP_PENDING.value}", self.new_cluster_action)

    def is_start_applications_pending(self):
        return re.match(rf"{ClusterActionEnum.START_APPLICATIONS_PENDING.value}", self.new_cluster_action)

    @staticmethod
    def _get_value_from_image(image, field_name, default=""):
        return image.get(field_name, {}).get("S", default) if image else default
