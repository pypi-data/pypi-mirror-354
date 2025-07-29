from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_wckey_tag_flags_item import V0042WckeyTagFlagsItem

T = TypeVar("T", bound="V0042WckeyTagStruct")


@_attrs_define
class V0042WckeyTagStruct:
    """
    Attributes:
        wckey (str): WCKey name
        flags (list[V0042WckeyTagFlagsItem]):
    """

    wckey: str
    flags: list[V0042WckeyTagFlagsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        wckey = self.wckey

        flags = []
        for componentsschemasv0_0_42_wckey_tag_flags_item_data in self.flags:
            componentsschemasv0_0_42_wckey_tag_flags_item = componentsschemasv0_0_42_wckey_tag_flags_item_data.value
            flags.append(componentsschemasv0_0_42_wckey_tag_flags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "wckey": wckey,
                "flags": flags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        wckey = d.pop("wckey")

        flags = []
        _flags = d.pop("flags")
        for componentsschemasv0_0_42_wckey_tag_flags_item_data in _flags:
            componentsschemasv0_0_42_wckey_tag_flags_item = V0042WckeyTagFlagsItem(
                componentsschemasv0_0_42_wckey_tag_flags_item_data
            )

            flags.append(componentsschemasv0_0_42_wckey_tag_flags_item)

        v0042_wckey_tag_struct = cls(
            wckey=wckey,
            flags=flags,
        )

        v0042_wckey_tag_struct.additional_properties = d
        return v0042_wckey_tag_struct

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
