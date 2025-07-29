from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_job_array_limits_max_running import V0042JobArrayLimitsMaxRunning


T = TypeVar("T", bound="V0042JobArrayLimitsMax")


@_attrs_define
class V0042JobArrayLimitsMax:
    """
    Attributes:
        running (Union[Unset, V0042JobArrayLimitsMaxRunning]):
    """

    running: Union[Unset, "V0042JobArrayLimitsMaxRunning"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        running: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.running, Unset):
            running = self.running.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if running is not UNSET:
            field_dict["running"] = running

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_job_array_limits_max_running import V0042JobArrayLimitsMaxRunning

        d = dict(src_dict)
        _running = d.pop("running", UNSET)
        running: Union[Unset, V0042JobArrayLimitsMaxRunning]
        if isinstance(_running, Unset):
            running = UNSET
        else:
            running = V0042JobArrayLimitsMaxRunning.from_dict(_running)

        v0042_job_array_limits_max = cls(
            running=running,
        )

        v0042_job_array_limits_max.additional_properties = d
        return v0042_job_array_limits_max

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
