from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_accounting_allocated import V0042AccountingAllocated
    from ..models.v0042_tres import V0042Tres


T = TypeVar("T", bound="V0042Accounting")


@_attrs_define
class V0042Accounting:
    """
    Attributes:
        allocated (Union[Unset, V0042AccountingAllocated]):
        id (Union[Unset, int]): Association ID or Workload characterization key ID
        id_alt (Union[Unset, int]): Alternate ID (not currently used)
        start (Union[Unset, int]): When the record was started (UNIX timestamp)
        tres (Union[Unset, V0042Tres]):
    """

    allocated: Union[Unset, "V0042AccountingAllocated"] = UNSET
    id: Union[Unset, int] = UNSET
    id_alt: Union[Unset, int] = UNSET
    start: Union[Unset, int] = UNSET
    tres: Union[Unset, "V0042Tres"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allocated: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.allocated, Unset):
            allocated = self.allocated.to_dict()

        id = self.id

        id_alt = self.id_alt

        start = self.start

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allocated is not UNSET:
            field_dict["allocated"] = allocated
        if id is not UNSET:
            field_dict["id"] = id
        if id_alt is not UNSET:
            field_dict["id_alt"] = id_alt
        if start is not UNSET:
            field_dict["start"] = start
        if tres is not UNSET:
            field_dict["TRES"] = tres

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_accounting_allocated import V0042AccountingAllocated
        from ..models.v0042_tres import V0042Tres

        d = dict(src_dict)
        _allocated = d.pop("allocated", UNSET)
        allocated: Union[Unset, V0042AccountingAllocated]
        if isinstance(_allocated, Unset):
            allocated = UNSET
        else:
            allocated = V0042AccountingAllocated.from_dict(_allocated)

        id = d.pop("id", UNSET)

        id_alt = d.pop("id_alt", UNSET)

        start = d.pop("start", UNSET)

        _tres = d.pop("TRES", UNSET)
        tres: Union[Unset, V0042Tres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0042Tres.from_dict(_tres)

        v0042_accounting = cls(
            allocated=allocated,
            id=id,
            id_alt=id_alt,
            start=start,
            tres=tres,
        )

        v0042_accounting.additional_properties = d
        return v0042_accounting

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
