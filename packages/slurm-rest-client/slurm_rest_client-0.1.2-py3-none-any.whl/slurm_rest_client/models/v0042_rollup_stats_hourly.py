from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_rollup_stats_hourly_duration import V0042RollupStatsHourlyDuration


T = TypeVar("T", bound="V0042RollupStatsHourly")


@_attrs_define
class V0042RollupStatsHourly:
    """
    Attributes:
        count (Union[Unset, int]): Number of hourly rollups since last_run
        last_run (Union[Unset, int]): Last time hourly rollup ran (UNIX timestamp)
        duration (Union[Unset, V0042RollupStatsHourlyDuration]):
    """

    count: Union[Unset, int] = UNSET
    last_run: Union[Unset, int] = UNSET
    duration: Union[Unset, "V0042RollupStatsHourlyDuration"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        last_run = self.last_run

        duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.duration, Unset):
            duration = self.duration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if last_run is not UNSET:
            field_dict["last_run"] = last_run
        if duration is not UNSET:
            field_dict["duration"] = duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_rollup_stats_hourly_duration import V0042RollupStatsHourlyDuration

        d = dict(src_dict)
        count = d.pop("count", UNSET)

        last_run = d.pop("last_run", UNSET)

        _duration = d.pop("duration", UNSET)
        duration: Union[Unset, V0042RollupStatsHourlyDuration]
        if isinstance(_duration, Unset):
            duration = UNSET
        else:
            duration = V0042RollupStatsHourlyDuration.from_dict(_duration)

        v0042_rollup_stats_hourly = cls(
            count=count,
            last_run=last_run,
            duration=duration,
        )

        v0042_rollup_stats_hourly.additional_properties = d
        return v0042_rollup_stats_hourly

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
