from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_cluster_rec_flags_item import V0042ClusterRecFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_cluster_rec_associations import V0042ClusterRecAssociations
    from ..models.v0042_cluster_rec_controller import V0042ClusterRecController
    from ..models.v0042_tres import V0042Tres


T = TypeVar("T", bound="V0042ClusterRec")


@_attrs_define
class V0042ClusterRec:
    """
    Attributes:
        controller (Union[Unset, V0042ClusterRecController]):
        flags (Union[Unset, list[V0042ClusterRecFlagsItem]]):
        name (Union[Unset, str]): ClusterName
        nodes (Union[Unset, str]): Node names
        select_plugin (Union[Unset, str]):
        associations (Union[Unset, V0042ClusterRecAssociations]):
        rpc_version (Union[Unset, int]): RPC version used in the cluster
        tres (Union[Unset, list['V0042Tres']]):
    """

    controller: Union[Unset, "V0042ClusterRecController"] = UNSET
    flags: Union[Unset, list[V0042ClusterRecFlagsItem]] = UNSET
    name: Union[Unset, str] = UNSET
    nodes: Union[Unset, str] = UNSET
    select_plugin: Union[Unset, str] = UNSET
    associations: Union[Unset, "V0042ClusterRecAssociations"] = UNSET
    rpc_version: Union[Unset, int] = UNSET
    tres: Union[Unset, list["V0042Tres"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        controller: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.controller, Unset):
            controller = self.controller.to_dict()

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for componentsschemasv0_0_42_cluster_rec_flags_item_data in self.flags:
                componentsschemasv0_0_42_cluster_rec_flags_item = (
                    componentsschemasv0_0_42_cluster_rec_flags_item_data.value
                )
                flags.append(componentsschemasv0_0_42_cluster_rec_flags_item)

        name = self.name

        nodes = self.nodes

        select_plugin = self.select_plugin

        associations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = self.associations.to_dict()

        rpc_version = self.rpc_version

        tres: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = []
            for componentsschemasv0_0_42_tres_list_item_data in self.tres:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                tres.append(componentsschemasv0_0_42_tres_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if controller is not UNSET:
            field_dict["controller"] = controller
        if flags is not UNSET:
            field_dict["flags"] = flags
        if name is not UNSET:
            field_dict["name"] = name
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if select_plugin is not UNSET:
            field_dict["select_plugin"] = select_plugin
        if associations is not UNSET:
            field_dict["associations"] = associations
        if rpc_version is not UNSET:
            field_dict["rpc_version"] = rpc_version
        if tres is not UNSET:
            field_dict["tres"] = tres

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_cluster_rec_associations import V0042ClusterRecAssociations
        from ..models.v0042_cluster_rec_controller import V0042ClusterRecController
        from ..models.v0042_tres import V0042Tres

        d = dict(src_dict)
        _controller = d.pop("controller", UNSET)
        controller: Union[Unset, V0042ClusterRecController]
        if isinstance(_controller, Unset):
            controller = UNSET
        else:
            controller = V0042ClusterRecController.from_dict(_controller)

        flags = []
        _flags = d.pop("flags", UNSET)
        for componentsschemasv0_0_42_cluster_rec_flags_item_data in _flags or []:
            componentsschemasv0_0_42_cluster_rec_flags_item = V0042ClusterRecFlagsItem(
                componentsschemasv0_0_42_cluster_rec_flags_item_data
            )

            flags.append(componentsschemasv0_0_42_cluster_rec_flags_item)

        name = d.pop("name", UNSET)

        nodes = d.pop("nodes", UNSET)

        select_plugin = d.pop("select_plugin", UNSET)

        _associations = d.pop("associations", UNSET)
        associations: Union[Unset, V0042ClusterRecAssociations]
        if isinstance(_associations, Unset):
            associations = UNSET
        else:
            associations = V0042ClusterRecAssociations.from_dict(_associations)

        rpc_version = d.pop("rpc_version", UNSET)

        tres = []
        _tres = d.pop("tres", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _tres or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            tres.append(componentsschemasv0_0_42_tres_list_item)

        v0042_cluster_rec = cls(
            controller=controller,
            flags=flags,
            name=name,
            nodes=nodes,
            select_plugin=select_plugin,
            associations=associations,
            rpc_version=rpc_version,
            tres=tres,
        )

        v0042_cluster_rec.additional_properties = d
        return v0042_cluster_rec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
