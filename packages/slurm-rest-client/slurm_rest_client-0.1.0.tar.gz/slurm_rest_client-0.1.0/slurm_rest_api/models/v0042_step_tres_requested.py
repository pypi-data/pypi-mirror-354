from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_tres import V0042Tres


T = TypeVar("T", bound="V0042StepTresRequested")


@_attrs_define
class V0042StepTresRequested:
    """
    Attributes:
        max_ (Union[Unset, list['V0042Tres']]):
        min_ (Union[Unset, list['V0042Tres']]):
        average (Union[Unset, list['V0042Tres']]):
        total (Union[Unset, list['V0042Tres']]):
    """

    max_: Union[Unset, list["V0042Tres"]] = UNSET
    min_: Union[Unset, list["V0042Tres"]] = UNSET
    average: Union[Unset, list["V0042Tres"]] = UNSET
    total: Union[Unset, list["V0042Tres"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.max_, Unset):
            max_ = []
            for componentsschemasv0_0_42_step_tres_req_max_item_data in self.max_:
                componentsschemasv0_0_42_step_tres_req_max_item = (
                    componentsschemasv0_0_42_step_tres_req_max_item_data.to_dict()
                )
                max_.append(componentsschemasv0_0_42_step_tres_req_max_item)

        min_: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.min_, Unset):
            min_ = []
            for componentsschemasv0_0_42_step_tres_req_min_item_data in self.min_:
                componentsschemasv0_0_42_step_tres_req_min_item = (
                    componentsschemasv0_0_42_step_tres_req_min_item_data.to_dict()
                )
                min_.append(componentsschemasv0_0_42_step_tres_req_min_item)

        average: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.average, Unset):
            average = []
            for componentsschemasv0_0_42_tres_list_item_data in self.average:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                average.append(componentsschemasv0_0_42_tres_list_item)

        total: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.total, Unset):
            total = []
            for componentsschemasv0_0_42_tres_list_item_data in self.total:
                componentsschemasv0_0_42_tres_list_item = componentsschemasv0_0_42_tres_list_item_data.to_dict()
                total.append(componentsschemasv0_0_42_tres_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_
        if average is not UNSET:
            field_dict["average"] = average
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_tres import V0042Tres

        d = dict(src_dict)
        max_ = []
        _max_ = d.pop("max", UNSET)
        for componentsschemasv0_0_42_step_tres_req_max_item_data in _max_ or []:
            componentsschemasv0_0_42_step_tres_req_max_item = V0042Tres.from_dict(
                componentsschemasv0_0_42_step_tres_req_max_item_data
            )

            max_.append(componentsschemasv0_0_42_step_tres_req_max_item)

        min_ = []
        _min_ = d.pop("min", UNSET)
        for componentsschemasv0_0_42_step_tres_req_min_item_data in _min_ or []:
            componentsschemasv0_0_42_step_tres_req_min_item = V0042Tres.from_dict(
                componentsschemasv0_0_42_step_tres_req_min_item_data
            )

            min_.append(componentsschemasv0_0_42_step_tres_req_min_item)

        average = []
        _average = d.pop("average", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _average or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            average.append(componentsschemasv0_0_42_tres_list_item)

        total = []
        _total = d.pop("total", UNSET)
        for componentsschemasv0_0_42_tres_list_item_data in _total or []:
            componentsschemasv0_0_42_tres_list_item = V0042Tres.from_dict(componentsschemasv0_0_42_tres_list_item_data)

            total.append(componentsschemasv0_0_42_tres_list_item)

        v0042_step_tres_requested = cls(
            max_=max_,
            min_=min_,
            average=average,
            total=total,
        )

        v0042_step_tres_requested.additional_properties = d
        return v0042_step_tres_requested

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
