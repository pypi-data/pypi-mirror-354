from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_reservation_flags_item import V0042ReservationFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_reservation_core_spec import V0042ReservationCoreSpec
    from ..models.v0042_reservation_info_purge_completed import V0042ReservationInfoPurgeCompleted
    from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct
    from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct


T = TypeVar("T", bound="V0042ReservationInfo")


@_attrs_define
class V0042ReservationInfo:
    """
    Attributes:
        accounts (Union[Unset, str]): Comma separated list of permitted accounts
        burst_buffer (Union[Unset, str]): BurstBuffer
        core_count (Union[Unset, int]): CoreCnt
        core_specializations (Union[Unset, list['V0042ReservationCoreSpec']]):
        end_time (Union[Unset, V0042Uint64NoValStruct]):
        features (Union[Unset, str]): Features
        flags (Union[Unset, list[V0042ReservationFlagsItem]]):
        groups (Union[Unset, str]): Groups
        licenses (Union[Unset, str]): Licenses
        max_start_delay (Union[Unset, int]): MaxStartDelay in seconds
        name (Union[Unset, str]): ReservationName
        node_count (Union[Unset, int]): NodeCnt
        node_list (Union[Unset, str]): Nodes
        partition (Union[Unset, str]): PartitionName
        purge_completed (Union[Unset, V0042ReservationInfoPurgeCompleted]):
        start_time (Union[Unset, V0042Uint64NoValStruct]):
        watts (Union[Unset, V0042Uint32NoValStruct]):
        tres (Union[Unset, str]): Comma separated list of required TRES
        users (Union[Unset, str]): Comma separated list of permitted users
    """

    accounts: Union[Unset, str] = UNSET
    burst_buffer: Union[Unset, str] = UNSET
    core_count: Union[Unset, int] = UNSET
    core_specializations: Union[Unset, list["V0042ReservationCoreSpec"]] = UNSET
    end_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    features: Union[Unset, str] = UNSET
    flags: Union[Unset, list[V0042ReservationFlagsItem]] = UNSET
    groups: Union[Unset, str] = UNSET
    licenses: Union[Unset, str] = UNSET
    max_start_delay: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    node_count: Union[Unset, int] = UNSET
    node_list: Union[Unset, str] = UNSET
    partition: Union[Unset, str] = UNSET
    purge_completed: Union[Unset, "V0042ReservationInfoPurgeCompleted"] = UNSET
    start_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    watts: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    tres: Union[Unset, str] = UNSET
    users: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts

        burst_buffer = self.burst_buffer

        core_count = self.core_count

        core_specializations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.core_specializations, Unset):
            core_specializations = []
            for componentsschemasv0_0_42_reservation_info_core_spec_item_data in self.core_specializations:
                componentsschemasv0_0_42_reservation_info_core_spec_item = (
                    componentsschemasv0_0_42_reservation_info_core_spec_item_data.to_dict()
                )
                core_specializations.append(componentsschemasv0_0_42_reservation_info_core_spec_item)

        end_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.to_dict()

        features = self.features

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for componentsschemasv0_0_42_reservation_flags_item_data in self.flags:
                componentsschemasv0_0_42_reservation_flags_item = (
                    componentsschemasv0_0_42_reservation_flags_item_data.value
                )
                flags.append(componentsschemasv0_0_42_reservation_flags_item)

        groups = self.groups

        licenses = self.licenses

        max_start_delay = self.max_start_delay

        name = self.name

        node_count = self.node_count

        node_list = self.node_list

        partition = self.partition

        purge_completed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.purge_completed, Unset):
            purge_completed = self.purge_completed.to_dict()

        start_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.to_dict()

        watts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.watts, Unset):
            watts = self.watts.to_dict()

        tres = self.tres

        users = self.users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if burst_buffer is not UNSET:
            field_dict["burst_buffer"] = burst_buffer
        if core_count is not UNSET:
            field_dict["core_count"] = core_count
        if core_specializations is not UNSET:
            field_dict["core_specializations"] = core_specializations
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if features is not UNSET:
            field_dict["features"] = features
        if flags is not UNSET:
            field_dict["flags"] = flags
        if groups is not UNSET:
            field_dict["groups"] = groups
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if max_start_delay is not UNSET:
            field_dict["max_start_delay"] = max_start_delay
        if name is not UNSET:
            field_dict["name"] = name
        if node_count is not UNSET:
            field_dict["node_count"] = node_count
        if node_list is not UNSET:
            field_dict["node_list"] = node_list
        if partition is not UNSET:
            field_dict["partition"] = partition
        if purge_completed is not UNSET:
            field_dict["purge_completed"] = purge_completed
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if watts is not UNSET:
            field_dict["watts"] = watts
        if tres is not UNSET:
            field_dict["tres"] = tres
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_reservation_core_spec import V0042ReservationCoreSpec
        from ..models.v0042_reservation_info_purge_completed import V0042ReservationInfoPurgeCompleted
        from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct
        from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct

        d = dict(src_dict)
        accounts = d.pop("accounts", UNSET)

        burst_buffer = d.pop("burst_buffer", UNSET)

        core_count = d.pop("core_count", UNSET)

        core_specializations = []
        _core_specializations = d.pop("core_specializations", UNSET)
        for componentsschemasv0_0_42_reservation_info_core_spec_item_data in _core_specializations or []:
            componentsschemasv0_0_42_reservation_info_core_spec_item = V0042ReservationCoreSpec.from_dict(
                componentsschemasv0_0_42_reservation_info_core_spec_item_data
            )

            core_specializations.append(componentsschemasv0_0_42_reservation_info_core_spec_item)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = V0042Uint64NoValStruct.from_dict(_end_time)

        features = d.pop("features", UNSET)

        flags = []
        _flags = d.pop("flags", UNSET)
        for componentsschemasv0_0_42_reservation_flags_item_data in _flags or []:
            componentsschemasv0_0_42_reservation_flags_item = V0042ReservationFlagsItem(
                componentsschemasv0_0_42_reservation_flags_item_data
            )

            flags.append(componentsschemasv0_0_42_reservation_flags_item)

        groups = d.pop("groups", UNSET)

        licenses = d.pop("licenses", UNSET)

        max_start_delay = d.pop("max_start_delay", UNSET)

        name = d.pop("name", UNSET)

        node_count = d.pop("node_count", UNSET)

        node_list = d.pop("node_list", UNSET)

        partition = d.pop("partition", UNSET)

        _purge_completed = d.pop("purge_completed", UNSET)
        purge_completed: Union[Unset, V0042ReservationInfoPurgeCompleted]
        if isinstance(_purge_completed, Unset):
            purge_completed = UNSET
        else:
            purge_completed = V0042ReservationInfoPurgeCompleted.from_dict(_purge_completed)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = V0042Uint64NoValStruct.from_dict(_start_time)

        _watts = d.pop("watts", UNSET)
        watts: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_watts, Unset):
            watts = UNSET
        else:
            watts = V0042Uint32NoValStruct.from_dict(_watts)

        tres = d.pop("tres", UNSET)

        users = d.pop("users", UNSET)

        v0042_reservation_info = cls(
            accounts=accounts,
            burst_buffer=burst_buffer,
            core_count=core_count,
            core_specializations=core_specializations,
            end_time=end_time,
            features=features,
            flags=flags,
            groups=groups,
            licenses=licenses,
            max_start_delay=max_start_delay,
            name=name,
            node_count=node_count,
            node_list=node_list,
            partition=partition,
            purge_completed=purge_completed,
            start_time=start_time,
            watts=watts,
            tres=tres,
            users=users,
        )

        v0042_reservation_info.additional_properties = d
        return v0042_reservation_info

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
