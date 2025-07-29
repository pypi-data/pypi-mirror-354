from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_cr_type_item import V0042CrTypeItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_partition_info_accounts import V0042PartitionInfoAccounts
    from ..models.v0042_partition_info_cpus import V0042PartitionInfoCpus
    from ..models.v0042_partition_info_defaults import V0042PartitionInfoDefaults
    from ..models.v0042_partition_info_groups import V0042PartitionInfoGroups
    from ..models.v0042_partition_info_maximums import V0042PartitionInfoMaximums
    from ..models.v0042_partition_info_minimums import V0042PartitionInfoMinimums
    from ..models.v0042_partition_info_nodes import V0042PartitionInfoNodes
    from ..models.v0042_partition_info_partition import V0042PartitionInfoPartition
    from ..models.v0042_partition_info_priority import V0042PartitionInfoPriority
    from ..models.v0042_partition_info_qos import V0042PartitionInfoQos
    from ..models.v0042_partition_info_timeouts import V0042PartitionInfoTimeouts
    from ..models.v0042_partition_info_tres import V0042PartitionInfoTres
    from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct


T = TypeVar("T", bound="V0042PartitionInfo")


@_attrs_define
class V0042PartitionInfo:
    """
    Attributes:
        nodes (Union[Unset, V0042PartitionInfoNodes]):
        accounts (Union[Unset, V0042PartitionInfoAccounts]):
        groups (Union[Unset, V0042PartitionInfoGroups]):
        qos (Union[Unset, V0042PartitionInfoQos]):
        alternate (Union[Unset, str]): Alternate
        tres (Union[Unset, V0042PartitionInfoTres]):
        cluster (Union[Unset, str]): Cluster name
        select_type (Union[Unset, list[V0042CrTypeItem]]):
        cpus (Union[Unset, V0042PartitionInfoCpus]):
        defaults (Union[Unset, V0042PartitionInfoDefaults]):
        grace_time (Union[Unset, int]): GraceTime
        maximums (Union[Unset, V0042PartitionInfoMaximums]):
        minimums (Union[Unset, V0042PartitionInfoMinimums]):
        name (Union[Unset, str]): PartitionName
        node_sets (Union[Unset, str]): NodeSets
        priority (Union[Unset, V0042PartitionInfoPriority]):
        timeouts (Union[Unset, V0042PartitionInfoTimeouts]):
        partition (Union[Unset, V0042PartitionInfoPartition]):
        suspend_time (Union[Unset, V0042Uint32NoValStruct]):
    """

    nodes: Union[Unset, "V0042PartitionInfoNodes"] = UNSET
    accounts: Union[Unset, "V0042PartitionInfoAccounts"] = UNSET
    groups: Union[Unset, "V0042PartitionInfoGroups"] = UNSET
    qos: Union[Unset, "V0042PartitionInfoQos"] = UNSET
    alternate: Union[Unset, str] = UNSET
    tres: Union[Unset, "V0042PartitionInfoTres"] = UNSET
    cluster: Union[Unset, str] = UNSET
    select_type: Union[Unset, list[V0042CrTypeItem]] = UNSET
    cpus: Union[Unset, "V0042PartitionInfoCpus"] = UNSET
    defaults: Union[Unset, "V0042PartitionInfoDefaults"] = UNSET
    grace_time: Union[Unset, int] = UNSET
    maximums: Union[Unset, "V0042PartitionInfoMaximums"] = UNSET
    minimums: Union[Unset, "V0042PartitionInfoMinimums"] = UNSET
    name: Union[Unset, str] = UNSET
    node_sets: Union[Unset, str] = UNSET
    priority: Union[Unset, "V0042PartitionInfoPriority"] = UNSET
    timeouts: Union[Unset, "V0042PartitionInfoTimeouts"] = UNSET
    partition: Union[Unset, "V0042PartitionInfoPartition"] = UNSET
    suspend_time: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = self.nodes.to_dict()

        accounts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = self.accounts.to_dict()

        groups: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups.to_dict()

        qos: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos.to_dict()

        alternate = self.alternate

        tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tres, Unset):
            tres = self.tres.to_dict()

        cluster = self.cluster

        select_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.select_type, Unset):
            select_type = []
            for componentsschemasv0_0_42_cr_type_item_data in self.select_type:
                componentsschemasv0_0_42_cr_type_item = componentsschemasv0_0_42_cr_type_item_data.value
                select_type.append(componentsschemasv0_0_42_cr_type_item)

        cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus, Unset):
            cpus = self.cpus.to_dict()

        defaults: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.defaults, Unset):
            defaults = self.defaults.to_dict()

        grace_time = self.grace_time

        maximums: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.maximums, Unset):
            maximums = self.maximums.to_dict()

        minimums: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimums, Unset):
            minimums = self.minimums.to_dict()

        name = self.name

        node_sets = self.node_sets

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        timeouts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.timeouts, Unset):
            timeouts = self.timeouts.to_dict()

        partition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition, Unset):
            partition = self.partition.to_dict()

        suspend_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.suspend_time, Unset):
            suspend_time = self.suspend_time.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if groups is not UNSET:
            field_dict["groups"] = groups
        if qos is not UNSET:
            field_dict["qos"] = qos
        if alternate is not UNSET:
            field_dict["alternate"] = alternate
        if tres is not UNSET:
            field_dict["tres"] = tres
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if select_type is not UNSET:
            field_dict["select_type"] = select_type
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if grace_time is not UNSET:
            field_dict["grace_time"] = grace_time
        if maximums is not UNSET:
            field_dict["maximums"] = maximums
        if minimums is not UNSET:
            field_dict["minimums"] = minimums
        if name is not UNSET:
            field_dict["name"] = name
        if node_sets is not UNSET:
            field_dict["node_sets"] = node_sets
        if priority is not UNSET:
            field_dict["priority"] = priority
        if timeouts is not UNSET:
            field_dict["timeouts"] = timeouts
        if partition is not UNSET:
            field_dict["partition"] = partition
        if suspend_time is not UNSET:
            field_dict["suspend_time"] = suspend_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_partition_info_accounts import V0042PartitionInfoAccounts
        from ..models.v0042_partition_info_cpus import V0042PartitionInfoCpus
        from ..models.v0042_partition_info_defaults import V0042PartitionInfoDefaults
        from ..models.v0042_partition_info_groups import V0042PartitionInfoGroups
        from ..models.v0042_partition_info_maximums import V0042PartitionInfoMaximums
        from ..models.v0042_partition_info_minimums import V0042PartitionInfoMinimums
        from ..models.v0042_partition_info_nodes import V0042PartitionInfoNodes
        from ..models.v0042_partition_info_partition import V0042PartitionInfoPartition
        from ..models.v0042_partition_info_priority import V0042PartitionInfoPriority
        from ..models.v0042_partition_info_qos import V0042PartitionInfoQos
        from ..models.v0042_partition_info_timeouts import V0042PartitionInfoTimeouts
        from ..models.v0042_partition_info_tres import V0042PartitionInfoTres
        from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct

        d = dict(src_dict)
        _nodes = d.pop("nodes", UNSET)
        nodes: Union[Unset, V0042PartitionInfoNodes]
        if isinstance(_nodes, Unset):
            nodes = UNSET
        else:
            nodes = V0042PartitionInfoNodes.from_dict(_nodes)

        _accounts = d.pop("accounts", UNSET)
        accounts: Union[Unset, V0042PartitionInfoAccounts]
        if isinstance(_accounts, Unset):
            accounts = UNSET
        else:
            accounts = V0042PartitionInfoAccounts.from_dict(_accounts)

        _groups = d.pop("groups", UNSET)
        groups: Union[Unset, V0042PartitionInfoGroups]
        if isinstance(_groups, Unset):
            groups = UNSET
        else:
            groups = V0042PartitionInfoGroups.from_dict(_groups)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, V0042PartitionInfoQos]
        if isinstance(_qos, Unset):
            qos = UNSET
        else:
            qos = V0042PartitionInfoQos.from_dict(_qos)

        alternate = d.pop("alternate", UNSET)

        _tres = d.pop("tres", UNSET)
        tres: Union[Unset, V0042PartitionInfoTres]
        if isinstance(_tres, Unset):
            tres = UNSET
        else:
            tres = V0042PartitionInfoTres.from_dict(_tres)

        cluster = d.pop("cluster", UNSET)

        select_type = []
        _select_type = d.pop("select_type", UNSET)
        for componentsschemasv0_0_42_cr_type_item_data in _select_type or []:
            componentsschemasv0_0_42_cr_type_item = V0042CrTypeItem(componentsschemasv0_0_42_cr_type_item_data)

            select_type.append(componentsschemasv0_0_42_cr_type_item)

        _cpus = d.pop("cpus", UNSET)
        cpus: Union[Unset, V0042PartitionInfoCpus]
        if isinstance(_cpus, Unset):
            cpus = UNSET
        else:
            cpus = V0042PartitionInfoCpus.from_dict(_cpus)

        _defaults = d.pop("defaults", UNSET)
        defaults: Union[Unset, V0042PartitionInfoDefaults]
        if isinstance(_defaults, Unset):
            defaults = UNSET
        else:
            defaults = V0042PartitionInfoDefaults.from_dict(_defaults)

        grace_time = d.pop("grace_time", UNSET)

        _maximums = d.pop("maximums", UNSET)
        maximums: Union[Unset, V0042PartitionInfoMaximums]
        if isinstance(_maximums, Unset):
            maximums = UNSET
        else:
            maximums = V0042PartitionInfoMaximums.from_dict(_maximums)

        _minimums = d.pop("minimums", UNSET)
        minimums: Union[Unset, V0042PartitionInfoMinimums]
        if isinstance(_minimums, Unset):
            minimums = UNSET
        else:
            minimums = V0042PartitionInfoMinimums.from_dict(_minimums)

        name = d.pop("name", UNSET)

        node_sets = d.pop("node_sets", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0042PartitionInfoPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0042PartitionInfoPriority.from_dict(_priority)

        _timeouts = d.pop("timeouts", UNSET)
        timeouts: Union[Unset, V0042PartitionInfoTimeouts]
        if isinstance(_timeouts, Unset):
            timeouts = UNSET
        else:
            timeouts = V0042PartitionInfoTimeouts.from_dict(_timeouts)

        _partition = d.pop("partition", UNSET)
        partition: Union[Unset, V0042PartitionInfoPartition]
        if isinstance(_partition, Unset):
            partition = UNSET
        else:
            partition = V0042PartitionInfoPartition.from_dict(_partition)

        _suspend_time = d.pop("suspend_time", UNSET)
        suspend_time: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_suspend_time, Unset):
            suspend_time = UNSET
        else:
            suspend_time = V0042Uint32NoValStruct.from_dict(_suspend_time)

        v0042_partition_info = cls(
            nodes=nodes,
            accounts=accounts,
            groups=groups,
            qos=qos,
            alternate=alternate,
            tres=tres,
            cluster=cluster,
            select_type=select_type,
            cpus=cpus,
            defaults=defaults,
            grace_time=grace_time,
            maximums=maximums,
            minimums=minimums,
            name=name,
            node_sets=node_sets,
            priority=priority,
            timeouts=timeouts,
            partition=partition,
            suspend_time=suspend_time,
        )

        v0042_partition_info.additional_properties = d
        return v0042_partition_info

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
