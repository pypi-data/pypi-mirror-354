from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_account_short import V0042AccountShort
    from ..models.v0042_accounts_add_cond import V0042AccountsAddCond
    from ..models.v0042_openapi_error import V0042OpenapiError
    from ..models.v0042_openapi_meta import V0042OpenapiMeta
    from ..models.v0042_openapi_warning import V0042OpenapiWarning


T = TypeVar("T", bound="V0042OpenapiAccountsAddCondResp")


@_attrs_define
class V0042OpenapiAccountsAddCondResp:
    """
    Attributes:
        association_condition (Union[Unset, V0042AccountsAddCond]):
        account (Union[Unset, V0042AccountShort]):
        meta (Union[Unset, V0042OpenapiMeta]):
        errors (Union[Unset, list['V0042OpenapiError']]):
        warnings (Union[Unset, list['V0042OpenapiWarning']]):
    """

    association_condition: Union[Unset, "V0042AccountsAddCond"] = UNSET
    account: Union[Unset, "V0042AccountShort"] = UNSET
    meta: Union[Unset, "V0042OpenapiMeta"] = UNSET
    errors: Union[Unset, list["V0042OpenapiError"]] = UNSET
    warnings: Union[Unset, list["V0042OpenapiWarning"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        association_condition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.association_condition, Unset):
            association_condition = self.association_condition.to_dict()

        account: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

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
        if association_condition is not UNSET:
            field_dict["association_condition"] = association_condition
        if account is not UNSET:
            field_dict["account"] = account
        if meta is not UNSET:
            field_dict["meta"] = meta
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_account_short import V0042AccountShort
        from ..models.v0042_accounts_add_cond import V0042AccountsAddCond
        from ..models.v0042_openapi_error import V0042OpenapiError
        from ..models.v0042_openapi_meta import V0042OpenapiMeta
        from ..models.v0042_openapi_warning import V0042OpenapiWarning

        d = dict(src_dict)
        _association_condition = d.pop("association_condition", UNSET)
        association_condition: Union[Unset, V0042AccountsAddCond]
        if isinstance(_association_condition, Unset):
            association_condition = UNSET
        else:
            association_condition = V0042AccountsAddCond.from_dict(_association_condition)

        _account = d.pop("account", UNSET)
        account: Union[Unset, V0042AccountShort]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = V0042AccountShort.from_dict(_account)

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

        v0042_openapi_accounts_add_cond_resp = cls(
            association_condition=association_condition,
            account=account,
            meta=meta,
            errors=errors,
            warnings=warnings,
        )

        v0042_openapi_accounts_add_cond_resp.additional_properties = d
        return v0042_openapi_accounts_add_cond_resp

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
