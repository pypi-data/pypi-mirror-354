from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_job_array_response_msg_entry import V0042JobArrayResponseMsgEntry
    from ..models.v0042_openapi_error import V0042OpenapiError
    from ..models.v0042_openapi_meta import V0042OpenapiMeta
    from ..models.v0042_openapi_warning import V0042OpenapiWarning


T = TypeVar("T", bound="V0042OpenapiJobPostResponse")


@_attrs_define
class V0042OpenapiJobPostResponse:
    """
    Attributes:
        results (Union[Unset, list['V0042JobArrayResponseMsgEntry']]):
        meta (Union[Unset, V0042OpenapiMeta]):
        errors (Union[Unset, list['V0042OpenapiError']]):
        warnings (Union[Unset, list['V0042OpenapiWarning']]):
    """

    results: Union[Unset, list["V0042JobArrayResponseMsgEntry"]] = UNSET
    meta: Union[Unset, "V0042OpenapiMeta"] = UNSET
    errors: Union[Unset, list["V0042OpenapiError"]] = UNSET
    warnings: Union[Unset, list["V0042OpenapiWarning"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for componentsschemasv0_0_42_job_array_response_array_item_data in self.results:
                componentsschemasv0_0_42_job_array_response_array_item = (
                    componentsschemasv0_0_42_job_array_response_array_item_data.to_dict()
                )
                results.append(componentsschemasv0_0_42_job_array_response_array_item)

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        errors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for componentsschemasv0_0_42_openapi_errors_item_data in self.errors:
                componentsschemasv0_0_42_openapi_errors_item = (
                    componentsschemasv0_0_42_openapi_errors_item_data.to_dict()
                )
                errors.append(componentsschemasv0_0_42_openapi_errors_item)

        warnings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = []
            for componentsschemasv0_0_42_openapi_warnings_item_data in self.warnings:
                componentsschemasv0_0_42_openapi_warnings_item = (
                    componentsschemasv0_0_42_openapi_warnings_item_data.to_dict()
                )
                warnings.append(componentsschemasv0_0_42_openapi_warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_job_array_response_msg_entry import V0042JobArrayResponseMsgEntry
        from ..models.v0042_openapi_error import V0042OpenapiError
        from ..models.v0042_openapi_meta import V0042OpenapiMeta
        from ..models.v0042_openapi_warning import V0042OpenapiWarning

        d = dict(src_dict)
        results = []
        _results = d.pop("results", UNSET)
        for componentsschemasv0_0_42_job_array_response_array_item_data in _results or []:
            componentsschemasv0_0_42_job_array_response_array_item = V0042JobArrayResponseMsgEntry.from_dict(
                componentsschemasv0_0_42_job_array_response_array_item_data
            )

            results.append(componentsschemasv0_0_42_job_array_response_array_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, V0042OpenapiMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = V0042OpenapiMeta.from_dict(_meta)

        errors = []
        _errors = d.pop("errors", UNSET)
        for componentsschemasv0_0_42_openapi_errors_item_data in _errors or []:
            componentsschemasv0_0_42_openapi_errors_item = V0042OpenapiError.from_dict(
                componentsschemasv0_0_42_openapi_errors_item_data
            )

            errors.append(componentsschemasv0_0_42_openapi_errors_item)

        warnings = []
        _warnings = d.pop("warnings", UNSET)
        for componentsschemasv0_0_42_openapi_warnings_item_data in _warnings or []:
            componentsschemasv0_0_42_openapi_warnings_item = V0042OpenapiWarning.from_dict(
                componentsschemasv0_0_42_openapi_warnings_item_data
            )

            warnings.append(componentsschemasv0_0_42_openapi_warnings_item)

        v0042_openapi_job_post_response = cls(
            results=results,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0042_openapi_job_post_response.additional_properties = d
        return v0042_openapi_job_post_response

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
