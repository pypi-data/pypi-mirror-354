from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_assoc_max_jobs import V0042AssocMaxJobs
    from ..models.v0042_assoc_max_per import V0042AssocMaxPer
    from ..models.v0042_assoc_max_tres import V0042AssocMaxTres


T = TypeVar("T", bound="V0042AssocMax")


@_attrs_define
class V0042AssocMax:
    """
    Attributes:
        jobs (Union[Unset, V0042AssocMaxJobs]):
        tres (Union[Unset, V0042AssocMaxTres]):
        per (Union[Unset, V0042AssocMaxPer]):
    """

    jobs: Union[Unset, "V0042AssocMaxJobs"] = UNSET
    tres: Union[Unset, "V0042AssocMaxTres"] = UNSET
    per: Union[Unset, "V0042AssocMaxPer"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        jobs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.jobs, Unset):
            jobs = self.jobs.to_dict()

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        per: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.per, Unset):
            per = self.per.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if jobs is not UNSET:
            field_dict["jobs"] = jobs
        if tres is not UNSET:
            field_dict["tres"] = tres
        if per is not UNSET:
            field_dict["per"] = per

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_assoc_max_jobs import V0042AssocMaxJobs
        from ..models.v0042_assoc_max_per import V0042AssocMaxPer
        from ..models.v0042_assoc_max_tres import V0042AssocMaxTres

        d = dict(src_dict)
        _jobs = d.pop("jobs", UNSET)
        jobs: Union[Unset, V0042AssocMaxJobs]
        if isinstance(_jobs, Unset):
            jobs = UNSET
        else:
            jobs = V0042AssocMaxJobs.from_dict(_jobs)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0042AssocMaxTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0042AssocMaxTres.from_dict(_tres)

        _per = d.pop("per", UNSET)
        per: Union[Unset, V0042AssocMaxPer]
        if isinstance(_per, Unset):
            per = UNSET
        else:
            per = V0042AssocMaxPer.from_dict(_per)

        v0042_assoc_max = cls(
            jobs=jobs,
            tres=tres,
            per=per,
        )

        v0042_assoc_max.additional_properties = d
        return v0042_assoc_max

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
