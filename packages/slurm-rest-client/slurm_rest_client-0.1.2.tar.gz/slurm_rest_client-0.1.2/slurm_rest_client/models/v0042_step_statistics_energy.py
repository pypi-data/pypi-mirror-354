from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct


T = TypeVar("T", bound="V0042StepStatisticsEnergy")


@_attrs_define
class V0042StepStatisticsEnergy:
    """
    Attributes:
        consumed (Union[Unset, V0042Uint64NoValStruct]):
    """

    consumed: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        consumed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.consumed, Unset):
            consumed = self.consumed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if consumed is not UNSET:
            field_dict["consumed"] = consumed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct

        d = dict(src_dict)
        _consumed = d.pop("consumed", UNSET)
        consumed: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_consumed, Unset):
            consumed = UNSET
        else:
            consumed = V0042Uint64NoValStruct.from_dict(_consumed)

        v0042_step_statistics_energy = cls(
            consumed=consumed,
        )

        v0042_step_statistics_energy.additional_properties = d
        return v0042_step_statistics_energy

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
