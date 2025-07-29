from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_step_statistics_cpu import V0042StepStatisticsCPU
    from ..models.v0042_step_statistics_energy import V0042StepStatisticsEnergy


T = TypeVar("T", bound="V0042StepStatistics")


@_attrs_define
class V0042StepStatistics:
    """
    Attributes:
        cpu (Union[Unset, V0042StepStatisticsCPU]):
        energy (Union[Unset, V0042StepStatisticsEnergy]):
    """

    cpu: Union[Unset, "V0042StepStatisticsCPU"] = UNSET
    energy: Union[Unset, "V0042StepStatisticsEnergy"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        energy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.energy, Unset):
            energy = self.energy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu is not UNSET:
            field_dict["CPU"] = cpu
        if energy is not UNSET:
            field_dict["energy"] = energy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_step_statistics_cpu import V0042StepStatisticsCPU
        from ..models.v0042_step_statistics_energy import V0042StepStatisticsEnergy

        d = dict(src_dict)
        _cpu = d.pop("CPU", UNSET)
        cpu: Union[Unset, V0042StepStatisticsCPU]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = V0042StepStatisticsCPU.from_dict(_cpu)

        _energy = d.pop("energy", UNSET)
        energy: Union[Unset, V0042StepStatisticsEnergy]
        if isinstance(_energy, Unset):
            energy = UNSET
        else:
            energy = V0042StepStatisticsEnergy.from_dict(_energy)

        v0042_step_statistics = cls(
            cpu=cpu,
            energy=energy,
        )

        v0042_step_statistics.additional_properties = d
        return v0042_step_statistics

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
