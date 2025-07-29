from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_process_exit_code_status_item import V0042ProcessExitCodeStatusItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_process_exit_code_verbose_signal import V0042ProcessExitCodeVerboseSignal
    from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct


T = TypeVar("T", bound="V0042ProcessExitCodeVerbose")


@_attrs_define
class V0042ProcessExitCodeVerbose:
    """
    Attributes:
        status (Union[Unset, list[V0042ProcessExitCodeStatusItem]]):
        return_code (Union[Unset, V0042Uint32NoValStruct]):
        signal (Union[Unset, V0042ProcessExitCodeVerboseSignal]):
    """

    status: Union[Unset, list[V0042ProcessExitCodeStatusItem]] = UNSET
    return_code: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    signal: Union[Unset, "V0042ProcessExitCodeVerboseSignal"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, list[str]] = UNSET
        if not isinstance(self.status, Unset):
            status = []
            for componentsschemasv0_0_42_process_exit_code_status_item_data in self.status:
                componentsschemasv0_0_42_process_exit_code_status_item = (
                    componentsschemasv0_0_42_process_exit_code_status_item_data.value
                )
                status.append(componentsschemasv0_0_42_process_exit_code_status_item)

        return_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.return_code, Unset):
            return_code = self.return_code.to_dict()

        signal: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.signal, Unset):
            signal = self.signal.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if return_code is not UNSET:
            field_dict["return_code"] = return_code
        if signal is not UNSET:
            field_dict["signal"] = signal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_process_exit_code_verbose_signal import V0042ProcessExitCodeVerboseSignal
        from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct

        d = dict(src_dict)
        status = []
        _status = d.pop("status", UNSET)
        for componentsschemasv0_0_42_process_exit_code_status_item_data in _status or []:
            componentsschemasv0_0_42_process_exit_code_status_item = V0042ProcessExitCodeStatusItem(
                componentsschemasv0_0_42_process_exit_code_status_item_data
            )

            status.append(componentsschemasv0_0_42_process_exit_code_status_item)

        _return_code = d.pop("return_code", UNSET)
        return_code: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_return_code, Unset):
            return_code = UNSET
        else:
            return_code = V0042Uint32NoValStruct.from_dict(_return_code)

        _signal = d.pop("signal", UNSET)
        signal: Union[Unset, V0042ProcessExitCodeVerboseSignal]
        if isinstance(_signal, Unset):
            signal = UNSET
        else:
            signal = V0042ProcessExitCodeVerboseSignal.from_dict(_signal)

        v0042_process_exit_code_verbose = cls(
            status=status,
            return_code=return_code,
            signal=signal,
        )

        v0042_process_exit_code_verbose.additional_properties = d
        return v0042_process_exit_code_verbose

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
