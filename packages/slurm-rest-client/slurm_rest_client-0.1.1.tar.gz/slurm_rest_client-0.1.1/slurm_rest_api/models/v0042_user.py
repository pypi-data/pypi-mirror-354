from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_admin_lvl_item import V0042AdminLvlItem
from ..models.v0042_user_flags_item import V0042UserFlagsItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_assoc_short import V0042AssocShort
    from ..models.v0042_coord import V0042Coord
    from ..models.v0042_user_default import V0042UserDefault
    from ..models.v0042_wckey import V0042Wckey


T = TypeVar("T", bound="V0042User")


@_attrs_define
class V0042User:
    """
    Attributes:
        name (str): User name
        administrator_level (Union[Unset, list[V0042AdminLvlItem]]):
        associations (Union[Unset, list['V0042AssocShort']]):
        coordinators (Union[Unset, list['V0042Coord']]):
        default (Union[Unset, V0042UserDefault]):
        flags (Union[Unset, list[V0042UserFlagsItem]]):
        old_name (Union[Unset, str]): Previous user name
        wckeys (Union[Unset, list['V0042Wckey']]):
    """

    name: str
    administrator_level: Union[Unset, list[V0042AdminLvlItem]] = UNSET
    associations: Union[Unset, list["V0042AssocShort"]] = UNSET
    coordinators: Union[Unset, list["V0042Coord"]] = UNSET
    default: Union[Unset, "V0042UserDefault"] = UNSET
    flags: Union[Unset, list[V0042UserFlagsItem]] = UNSET
    old_name: Union[Unset, str] = UNSET
    wckeys: Union[Unset, list["V0042Wckey"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        administrator_level: Union[Unset, list[str]] = UNSET
        if not isinstance(self.administrator_level, Unset):
            administrator_level = []
            for componentsschemasv0_0_42_admin_lvl_item_data in self.administrator_level:
                componentsschemasv0_0_42_admin_lvl_item = componentsschemasv0_0_42_admin_lvl_item_data.value
                administrator_level.append(componentsschemasv0_0_42_admin_lvl_item)

        associations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.associations, Unset):
            associations = []
            for componentsschemasv0_0_42_assoc_short_list_item_data in self.associations:
                componentsschemasv0_0_42_assoc_short_list_item = (
                    componentsschemasv0_0_42_assoc_short_list_item_data.to_dict()
                )
                associations.append(componentsschemasv0_0_42_assoc_short_list_item)

        coordinators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.coordinators, Unset):
            coordinators = []
            for componentsschemasv0_0_42_coord_list_item_data in self.coordinators:
                componentsschemasv0_0_42_coord_list_item = componentsschemasv0_0_42_coord_list_item_data.to_dict()
                coordinators.append(componentsschemasv0_0_42_coord_list_item)

        default: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default, Unset):
            default = self.default.to_dict()

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for componentsschemasv0_0_42_user_flags_item_data in self.flags:
                componentsschemasv0_0_42_user_flags_item = componentsschemasv0_0_42_user_flags_item_data.value
                flags.append(componentsschemasv0_0_42_user_flags_item)

        old_name = self.old_name

        wckeys: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.wckeys, Unset):
            wckeys = []
            for componentsschemasv0_0_42_wckey_list_item_data in self.wckeys:
                componentsschemasv0_0_42_wckey_list_item = componentsschemasv0_0_42_wckey_list_item_data.to_dict()
                wckeys.append(componentsschemasv0_0_42_wckey_list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if administrator_level is not UNSET:
            field_dict["administrator_level"] = administrator_level
        if associations is not UNSET:
            field_dict["associations"] = associations
        if coordinators is not UNSET:
            field_dict["coordinators"] = coordinators
        if default is not UNSET:
            field_dict["default"] = default
        if flags is not UNSET:
            field_dict["flags"] = flags
        if old_name is not UNSET:
            field_dict["old_name"] = old_name
        if wckeys is not UNSET:
            field_dict["wckeys"] = wckeys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_assoc_short import V0042AssocShort
        from ..models.v0042_coord import V0042Coord
        from ..models.v0042_user_default import V0042UserDefault
        from ..models.v0042_wckey import V0042Wckey

        d = dict(src_dict)
        name = d.pop("name")

        administrator_level = []
        _administrator_level = d.pop("administrator_level", UNSET)
        for componentsschemasv0_0_42_admin_lvl_item_data in _administrator_level or []:
            componentsschemasv0_0_42_admin_lvl_item = V0042AdminLvlItem(componentsschemasv0_0_42_admin_lvl_item_data)

            administrator_level.append(componentsschemasv0_0_42_admin_lvl_item)

        associations = []
        _associations = d.pop("associations", UNSET)
        for componentsschemasv0_0_42_assoc_short_list_item_data in _associations or []:
            componentsschemasv0_0_42_assoc_short_list_item = V0042AssocShort.from_dict(
                componentsschemasv0_0_42_assoc_short_list_item_data
            )

            associations.append(componentsschemasv0_0_42_assoc_short_list_item)

        coordinators = []
        _coordinators = d.pop("coordinators", UNSET)
        for componentsschemasv0_0_42_coord_list_item_data in _coordinators or []:
            componentsschemasv0_0_42_coord_list_item = V0042Coord.from_dict(
                componentsschemasv0_0_42_coord_list_item_data
            )

            coordinators.append(componentsschemasv0_0_42_coord_list_item)

        _default = d.pop("default", UNSET)
        default: Union[Unset, V0042UserDefault]
        if isinstance(_default, Unset):
            default = UNSET
        else:
            default = V0042UserDefault.from_dict(_default)

        flags = []
        _flags = d.pop("flags", UNSET)
        for componentsschemasv0_0_42_user_flags_item_data in _flags or []:
            componentsschemasv0_0_42_user_flags_item = V0042UserFlagsItem(componentsschemasv0_0_42_user_flags_item_data)

            flags.append(componentsschemasv0_0_42_user_flags_item)

        old_name = d.pop("old_name", UNSET)

        wckeys = []
        _wckeys = d.pop("wckeys", UNSET)
        for componentsschemasv0_0_42_wckey_list_item_data in _wckeys or []:
            componentsschemasv0_0_42_wckey_list_item = V0042Wckey.from_dict(
                componentsschemasv0_0_42_wckey_list_item_data
            )

            wckeys.append(componentsschemasv0_0_42_wckey_list_item)

        v0042_user = cls(
            name=name,
            administrator_level=administrator_level,
            associations=associations,
            coordinators=coordinators,
            default=default,
            flags=flags,
            old_name=old_name,
            wckeys=wckeys,
        )

        v0042_user.additional_properties = d
        return v0042_user

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
