from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_tres import V0042Tres


T = TypeVar("T", bound="V0042QosLimitsMaxTresPer")


@_attrs_define
class V0042QosLimitsMaxTresPer:
    """
    Attributes:
        account (Union[Unset, list['V0042Tres']]):
        job (Union[Unset, list['V0042Tres']]):
        node (Union[Unset, list['V0042Tres']]):
        user (Union[Unset, list['V0042Tres']]):
    """

    account: Union[Unset, list["V0042Tres"]] = UNSET
    job: Union[Unset, list["V0042Tres"]] = UNSET
    node: Union[Unset, list["V0042Tres"]] = UNSET
    user: Union[Unset, list["V0042Tres"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.account, Unset):
            account = []
            for componentsschemasv0_0_42_tres_list_item_data in self.account:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                account.append(componentsschemasv0_0_42_tres_list_item)

        job: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.job, Unset):
            job = []
            for componentsschemasv0_0_42_tres_list_item_data in self.job:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                job.append(componentsschemasv0_0_42_tres_list_item)

        node: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.node, Unset):
            node = []
            for componentsschemasv0_0_42_tres_list_item_data in self.node:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                node.append(componentsschemasv0_0_42_tres_list_item)

        user: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.user, Unset):
            user = []
            for componentsschemasv0_0_42_tres_list_item_data in self.user:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                user.append(componentsschemasv0_0_42_tres_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if job is not UNSET:
            field_dict["job"] = job
        if node is not UNSET:
            field_dict["node"] = node
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_tres import V0042Tres

        d = dict(src_dict)
        account = []
        _account = d.pop("account", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _account or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            account.append(componentsschemasv0_0_42_tres_list_item)

        job = []
        _job = d.pop("job", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _job or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            job.append(componentsschemasv0_0_42_tres_list_item)

        node = []
        _node = d.pop("node", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _node or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            node.append(componentsschemasv0_0_42_tres_list_item)

        user = []
        _user = d.pop("user", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _user or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            user.append(componentsschemasv0_0_42_tres_list_item)

        v0042_qos_limits_max_tres_per = cls(
            account=account,
            job=job,
            node=node,
            user=user,
        )

        v0042_qos_limits_max_tres_per.additional_properties = d
        return v0042_qos_limits_max_tres_per

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
