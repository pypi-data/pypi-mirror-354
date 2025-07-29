from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_rollup_stats_daily import V0042RollupStatsDaily
    from ..models.v0042_rollup_stats_hourly import V0042RollupStatsHourly
    from ..models.v0042_rollup_stats_monthly import V0042RollupStatsMonthly


T = TypeVar("T", bound="V0042RollupStats")


@_attrs_define
class V0042RollupStats:
    """
    Attributes:
        hourly (Union[Unset, V0042RollupStatsHourly]):
        daily (Union[Unset, V0042RollupStatsDaily]):
        monthly (Union[Unset, V0042RollupStatsMonthly]):
    """

    hourly: Union[Unset, "V0042RollupStatsHourly"] = UNSET
    daily: Union[Unset, "V0042RollupStatsDaily"] = UNSET
    monthly: Union[Unset, "V0042RollupStatsMonthly"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hourly: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.hourly, Unset):
            hourly = self.hourly.to_dict()

        daily: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.daily, Unset):
            daily = self.daily.to_dict()

        monthly: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.monthly, Unset):
            monthly = self.monthly.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hourly is not UNSET:
            field_dict["hourly"] = hourly
        if daily is not UNSET:
            field_dict["daily"] = daily
        if monthly is not UNSET:
            field_dict["monthly"] = monthly

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_rollup_stats_daily import V0042RollupStatsDaily
        from ..models.v0042_rollup_stats_hourly import V0042RollupStatsHourly
        from ..models.v0042_rollup_stats_monthly import V0042RollupStatsMonthly

        d = dict(src_dict)
        _hourly = d.pop("hourly", UNSET)
        hourly: Union[Unset, V0042RollupStatsHourly]
        if isinstance(_hourly, Unset):
            hourly = UNSET
        else:
            hourly = V0042RollupStatsHourly.from_dict(_hourly)

        _daily = d.pop("daily", UNSET)
        daily: Union[Unset, V0042RollupStatsDaily]
        if isinstance(_daily, Unset):
            daily = UNSET
        else:
            daily = V0042RollupStatsDaily.from_dict(_daily)

        _monthly = d.pop("monthly", UNSET)
        monthly: Union[Unset, V0042RollupStatsMonthly]
        if isinstance(_monthly, Unset):
            monthly = UNSET
        else:
            monthly = V0042RollupStatsMonthly.from_dict(_monthly)

        v0042_rollup_stats = cls(
            hourly=hourly,
            daily=daily,
            monthly=monthly,
        )

        v0042_rollup_stats.additional_properties = d
        return v0042_rollup_stats

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
