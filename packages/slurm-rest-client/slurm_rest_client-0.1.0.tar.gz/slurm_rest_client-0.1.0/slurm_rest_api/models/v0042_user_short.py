from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_admin_lvl_item import V0042AdminLvlItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="V0042UserShort")


@_attrs_define
class V0042UserShort:
    """
    Attributes:
        adminlevel (Union[Unset, list[V0042AdminLvlItem]]):
        defaultaccount (Union[Unset, str]): Default account
        defaultwckey (Union[Unset, str]): Default WCKey
    """

    adminlevel: Union[Unset, list[V0042AdminLvlItem]] = UNSET
    defaultaccount: Union[Unset, str] = UNSET
    defaultwckey: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        adminlevel: Union[Unset, list[str]] = UNSET
        if not isinstance(self.adminlevel, Unset):
            adminlevel = []
            for componentsschemasv0_0_42_admin_lvl_item_data in self.adminlevel:
                componentsschemasv0_0_42_admin_lvl_item = componentsschemasv0_0_42_admin_lvl_item_data.value
                adminlevel.append(componentsschemasv0_0_42_admin_lvl_item)

        defaultaccount = self.defaultaccount

        defaultwckey = self.defaultwckey

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if adminlevel is not UNSET:
            field_dict["adminlevel"] = adminlevel
        if defaultaccount is not UNSET:
            field_dict["defaultaccount"] = defaultaccount
        if defaultwckey is not UNSET:
            field_dict["defaultwckey"] = defaultwckey

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        adminlevel = []
        _adminlevel = d.pop("adminlevel", UNSET)
        for componentsschemasv0_0_42_admin_lvl_item_data in _adminlevel or []:
            componentsschemasv0_0_42_admin_lvl_item = V0042AdminLvlItem(componentsschemasv0_0_42_admin_lvl_item_data)

            adminlevel.append(componentsschemasv0_0_42_admin_lvl_item)

        defaultaccount = d.pop("defaultaccount", UNSET)

        defaultwckey = d.pop("defaultwckey", UNSET)

        v0042_user_short = cls(
            adminlevel=adminlevel,
            defaultaccount=defaultaccount,
            defaultwckey=defaultwckey,
        )

        v0042_user_short.additional_properties = d
        return v0042_user_short

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
