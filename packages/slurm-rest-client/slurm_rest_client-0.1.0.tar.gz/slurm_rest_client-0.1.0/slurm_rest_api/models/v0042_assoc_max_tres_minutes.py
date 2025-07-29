from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_assoc_max_tres_minutes_per import V0042AssocMaxTresMinutesPer
    from ..models.v0042_tres import V0042Tres


T = TypeVar("T", bound="V0042AssocMaxTresMinutes")


@_attrs_define
class V0042AssocMaxTresMinutes:
    """
    Attributes:
        total (Union[Unset, list['V0042Tres']]):
        per (Union[Unset, V0042AssocMaxTresMinutesPer]):
    """

    total: Union[Unset, list["V0042Tres"]] = UNSET
    per: Union[Unset, "V0042AssocMaxTresMinutesPer"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.total, Unset):
            total = []
            for componentsschemasv0_0_42_tres_list_item_data in self.total:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                total.append(componentsschemasv0_0_42_tres_list_item)

        per: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.per, Unset):
            per = self.per.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if per is not UNSET:
            field_dict["per"] = per

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_assoc_max_tres_minutes_per import V0042AssocMaxTresMinutesPer
        from ..models.v0042_tres import V0042Tres

        d = dict(src_dict)
        total = []
        _total = d.pop("total", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _total or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            total.append(componentsschemasv0_0_42_tres_list_item)

        _per = d.pop("per", UNSET)
        per: Union[Unset, V0042AssocMaxTresMinutesPer]
        if isinstance(_per, Unset):
            per = UNSET
        else:
            per = V0042AssocMaxTresMinutesPer.from_dict(_per)

        v0042_assoc_max_tres_minutes = cls(
            total=total,
            per=per,
        )

        v0042_assoc_max_tres_minutes.additional_properties = d
        return v0042_assoc_max_tres_minutes

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
