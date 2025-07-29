from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.v0042_acct_gather_profile_item import V0042AcctGatherProfileItem
from ..models.v0042_job_flags_item import V0042JobFlagsItem
from ..models.v0042_job_mail_flags_item import V0042JobMailFlagsItem
from ..models.v0042_job_shared_item import V0042JobSharedItem
from ..models.v0042_job_state_item import V0042JobStateItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.v0042_float_64_no_val_struct import V0042Float64NoValStruct
    from ..models.v0042_job_info_power import V0042JobInfoPower
    from ..models.v0042_job_res import V0042JobRes
    from ..models.v0042_part_prio import V0042PartPrio
    from ..models.v0042_process_exit_code_verbose import V0042ProcessExitCodeVerbose
    from ..models.v0042_uint_16_no_val_struct import V0042Uint16NoValStruct
    from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct
    from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct


T = TypeVar("T", bound="V0042JobInfo")


@_attrs_define
class V0042JobInfo:
    """
    Attributes:
        account (Union[Unset, str]): Account associated with the job
        accrue_time (Union[Unset, V0042Uint64NoValStruct]):
        admin_comment (Union[Unset, str]): Arbitrary comment made by administrator
        allocating_node (Union[Unset, str]): Local node making the resource allocation
        array_job_id (Union[Unset, V0042Uint32NoValStruct]):
        array_task_id (Union[Unset, V0042Uint32NoValStruct]):
        array_max_tasks (Union[Unset, V0042Uint32NoValStruct]):
        array_task_string (Union[Unset, str]): String expression of task IDs in this record
        association_id (Union[Unset, int]): Unique identifier for the association
        batch_features (Union[Unset, str]): Features required for batch script's node
        batch_flag (Union[Unset, bool]): True if batch job
        batch_host (Union[Unset, str]): Name of host running batch script
        flags (Union[Unset, list[V0042JobFlagsItem]]):
        burst_buffer (Union[Unset, str]): Burst buffer specifications
        burst_buffer_state (Union[Unset, str]): Burst buffer state details
        cluster (Union[Unset, str]): Cluster name
        cluster_features (Union[Unset, str]): List of required cluster features
        command (Union[Unset, str]): Executed command
        comment (Union[Unset, str]): Arbitrary comment
        container (Union[Unset, str]): Absolute path to OCI container bundle
        container_id (Union[Unset, str]): OCI container ID
        contiguous (Union[Unset, bool]): True if job requires contiguous nodes
        core_spec (Union[Unset, int]): Specialized core count
        thread_spec (Union[Unset, int]): Specialized thread count
        cores_per_socket (Union[Unset, V0042Uint16NoValStruct]):
        billable_tres (Union[Unset, V0042Float64NoValStruct]):
        cpus_per_task (Union[Unset, V0042Uint16NoValStruct]):
        cpu_frequency_minimum (Union[Unset, V0042Uint32NoValStruct]):
        cpu_frequency_maximum (Union[Unset, V0042Uint32NoValStruct]):
        cpu_frequency_governor (Union[Unset, V0042Uint32NoValStruct]):
        cpus_per_tres (Union[Unset, str]): Semicolon delimited list of TRES=# values indicating how many CPUs should be
            allocated for each specified TRES (currently only used for gres/gpu)
        cron (Union[Unset, str]): Time specification for scrontab job
        deadline (Union[Unset, V0042Uint64NoValStruct]):
        delay_boot (Union[Unset, V0042Uint32NoValStruct]):
        dependency (Union[Unset, str]): Other jobs that must meet certain criteria before this job can start
        derived_exit_code (Union[Unset, V0042ProcessExitCodeVerbose]):
        eligible_time (Union[Unset, V0042Uint64NoValStruct]):
        end_time (Union[Unset, V0042Uint64NoValStruct]):
        excluded_nodes (Union[Unset, str]): Comma separated list of nodes that may not be used
        exit_code (Union[Unset, V0042ProcessExitCodeVerbose]):
        extra (Union[Unset, str]): Arbitrary string used for node filtering if extra constraints are enabled
        failed_node (Union[Unset, str]): Name of node that caused job failure
        features (Union[Unset, str]): Comma separated list of features that are required
        federation_origin (Union[Unset, str]): Origin cluster's name (when using federation)
        federation_siblings_active (Union[Unset, str]): Active sibling job names
        federation_siblings_viable (Union[Unset, str]): Viable sibling job names
        gres_detail (Union[Unset, list[str]]):
        group_id (Union[Unset, int]): Group ID of the user that owns the job
        group_name (Union[Unset, str]): Group name of the user that owns the job
        het_job_id (Union[Unset, V0042Uint32NoValStruct]):
        het_job_id_set (Union[Unset, str]): Job ID range for all heterogeneous job components
        het_job_offset (Union[Unset, V0042Uint32NoValStruct]):
        job_id (Union[Unset, int]): Job ID
        job_resources (Union[Unset, V0042JobRes]):
        job_size_str (Union[Unset, list[str]]):
        job_state (Union[Unset, list[V0042JobStateItem]]):
        last_sched_evaluation (Union[Unset, V0042Uint64NoValStruct]):
        licenses (Union[Unset, str]): License(s) required by the job
        mail_type (Union[Unset, list[V0042JobMailFlagsItem]]):
        mail_user (Union[Unset, str]): User to receive email notifications
        max_cpus (Union[Unset, V0042Uint32NoValStruct]):
        max_nodes (Union[Unset, V0042Uint32NoValStruct]):
        mcs_label (Union[Unset, str]): Multi-Category Security label on the job
        memory_per_tres (Union[Unset, str]): Semicolon delimited list of TRES=# values indicating how much memory in
            megabytes should be allocated for each specified TRES (currently only used for gres/gpu)
        name (Union[Unset, str]): Job name
        network (Union[Unset, str]): Network specs for the job
        nodes (Union[Unset, str]): Node(s) allocated to the job
        nice (Union[Unset, int]): Requested job priority change
        tasks_per_core (Union[Unset, V0042Uint16NoValStruct]):
        tasks_per_tres (Union[Unset, V0042Uint16NoValStruct]):
        tasks_per_node (Union[Unset, V0042Uint16NoValStruct]):
        tasks_per_socket (Union[Unset, V0042Uint16NoValStruct]):
        tasks_per_board (Union[Unset, V0042Uint16NoValStruct]):
        cpus (Union[Unset, V0042Uint32NoValStruct]):
        node_count (Union[Unset, V0042Uint32NoValStruct]):
        tasks (Union[Unset, V0042Uint32NoValStruct]):
        partition (Union[Unset, str]): Partition assigned to the job
        prefer (Union[Unset, str]): Feature(s) the job requested but that are not required
        memory_per_cpu (Union[Unset, V0042Uint64NoValStruct]):
        memory_per_node (Union[Unset, V0042Uint64NoValStruct]):
        minimum_cpus_per_node (Union[Unset, V0042Uint16NoValStruct]):
        minimum_tmp_disk_per_node (Union[Unset, V0042Uint32NoValStruct]):
        power (Union[Unset, V0042JobInfoPower]):
        preempt_time (Union[Unset, V0042Uint64NoValStruct]):
        preemptable_time (Union[Unset, V0042Uint64NoValStruct]):
        pre_sus_time (Union[Unset, V0042Uint64NoValStruct]):
        hold (Union[Unset, bool]): Hold (true) or release (false) job
        priority (Union[Unset, V0042Uint32NoValStruct]):
        priority_by_partition (Union[Unset, list['V0042PartPrio']]):
        profile (Union[Unset, list[V0042AcctGatherProfileItem]]):
        qos (Union[Unset, str]): Quality of Service assigned to the job, if pending the QOS requested
        reboot (Union[Unset, bool]): Node reboot requested before start
        required_nodes (Union[Unset, str]): Comma separated list of required nodes
        required_switches (Union[Unset, int]): Maximum number of switches
        requeue (Union[Unset, bool]): Determines whether the job may be requeued
        resize_time (Union[Unset, V0042Uint64NoValStruct]):
        restart_cnt (Union[Unset, int]): Number of job restarts
        resv_name (Union[Unset, str]): Name of reservation to use
        scheduled_nodes (Union[Unset, str]): List of nodes scheduled to be used for the job
        selinux_context (Union[Unset, str]): SELinux context
        shared (Union[Unset, list[V0042JobSharedItem]]):
        sockets_per_board (Union[Unset, int]): Number of sockets per board required
        sockets_per_node (Union[Unset, V0042Uint16NoValStruct]):
        start_time (Union[Unset, V0042Uint64NoValStruct]):
        state_description (Union[Unset, str]): Optional details for state_reason
        state_reason (Union[Unset, str]): Reason for current Pending or Failed state
        standard_error (Union[Unset, str]): Path to stderr file
        standard_input (Union[Unset, str]): Path to stdin file
        standard_output (Union[Unset, str]): Path to stdout file
        submit_time (Union[Unset, V0042Uint64NoValStruct]):
        suspend_time (Union[Unset, V0042Uint64NoValStruct]):
        system_comment (Union[Unset, str]): Arbitrary comment from slurmctld
        time_limit (Union[Unset, V0042Uint32NoValStruct]):
        time_minimum (Union[Unset, V0042Uint32NoValStruct]):
        threads_per_core (Union[Unset, V0042Uint16NoValStruct]):
        tres_bind (Union[Unset, str]): Task to TRES binding directives
        tres_freq (Union[Unset, str]): TRES frequency directives
        tres_per_job (Union[Unset, str]): Comma separated list of TRES=# values to be allocated per job
        tres_per_node (Union[Unset, str]): Comma separated list of TRES=# values to be allocated per node
        tres_per_socket (Union[Unset, str]): Comma separated list of TRES=# values to be allocated per socket
        tres_per_task (Union[Unset, str]): Comma separated list of TRES=# values to be allocated per task
        tres_req_str (Union[Unset, str]): TRES requested by the job
        tres_alloc_str (Union[Unset, str]): TRES used by the job
        user_id (Union[Unset, int]): User ID that owns the job
        user_name (Union[Unset, str]): User name that owns the job
        maximum_switch_wait_time (Union[Unset, int]): Maximum time to wait for switches in seconds
        wckey (Union[Unset, str]): Workload characterization key
        current_working_directory (Union[Unset, str]): Working directory to use for the job
    """

    account: Union[Unset, str] = UNSET
    accrue_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    admin_comment: Union[Unset, str] = UNSET
    allocating_node: Union[Unset, str] = UNSET
    array_job_id: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    array_task_id: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    array_max_tasks: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    array_task_string: Union[Unset, str] = UNSET
    association_id: Union[Unset, int] = UNSET
    batch_features: Union[Unset, str] = UNSET
    batch_flag: Union[Unset, bool] = UNSET
    batch_host: Union[Unset, str] = UNSET
    flags: Union[Unset, list[V0042JobFlagsItem]] = UNSET
    burst_buffer: Union[Unset, str] = UNSET
    burst_buffer_state: Union[Unset, str] = UNSET
    cluster: Union[Unset, str] = UNSET
    cluster_features: Union[Unset, str] = UNSET
    command: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    container: Union[Unset, str] = UNSET
    container_id: Union[Unset, str] = UNSET
    contiguous: Union[Unset, bool] = UNSET
    core_spec: Union[Unset, int] = UNSET
    thread_spec: Union[Unset, int] = UNSET
    cores_per_socket: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    billable_tres: Union[Unset, "V0042Float64NoValStruct"] = UNSET
    cpus_per_task: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    cpu_frequency_minimum: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    cpu_frequency_maximum: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    cpu_frequency_governor: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    cpus_per_tres: Union[Unset, str] = UNSET
    cron: Union[Unset, str] = UNSET
    deadline: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    delay_boot: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    dependency: Union[Unset, str] = UNSET
    derived_exit_code: Union[Unset, "V0042ProcessExitCodeVerbose"] = UNSET
    eligible_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    end_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    excluded_nodes: Union[Unset, str] = UNSET
    exit_code: Union[Unset, "V0042ProcessExitCodeVerbose"] = UNSET
    extra: Union[Unset, str] = UNSET
    failed_node: Union[Unset, str] = UNSET
    features: Union[Unset, str] = UNSET
    federation_origin: Union[Unset, str] = UNSET
    federation_siblings_active: Union[Unset, str] = UNSET
    federation_siblings_viable: Union[Unset, str] = UNSET
    gres_detail: Union[Unset, list[str]] = UNSET
    group_id: Union[Unset, int] = UNSET
    group_name: Union[Unset, str] = UNSET
    het_job_id: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    het_job_id_set: Union[Unset, str] = UNSET
    het_job_offset: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    job_id: Union[Unset, int] = UNSET
    job_resources: Union[Unset, "V0042JobRes"] = UNSET
    job_size_str: Union[Unset, list[str]] = UNSET
    job_state: Union[Unset, list[V0042JobStateItem]] = UNSET
    last_sched_evaluation: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    licenses: Union[Unset, str] = UNSET
    mail_type: Union[Unset, list[V0042JobMailFlagsItem]] = UNSET
    mail_user: Union[Unset, str] = UNSET
    max_cpus: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    max_nodes: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    mcs_label: Union[Unset, str] = UNSET
    memory_per_tres: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    network: Union[Unset, str] = UNSET
    nodes: Union[Unset, str] = UNSET
    nice: Union[Unset, int] = UNSET
    tasks_per_core: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    tasks_per_tres: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    tasks_per_node: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    tasks_per_socket: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    tasks_per_board: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    cpus: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    node_count: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    tasks: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    partition: Union[Unset, str] = UNSET
    prefer: Union[Unset, str] = UNSET
    memory_per_cpu: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    memory_per_node: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    minimum_cpus_per_node: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    minimum_tmp_disk_per_node: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    power: Union[Unset, "V0042JobInfoPower"] = UNSET
    preempt_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    preemptable_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    pre_sus_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    hold: Union[Unset, bool] = UNSET
    priority: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    priority_by_partition: Union[Unset, list["V0042PartPrio"]] = UNSET
    profile: Union[Unset, list[V0042AcctGatherProfileItem]] = UNSET
    qos: Union[Unset, str] = UNSET
    reboot: Union[Unset, bool] = UNSET
    required_nodes: Union[Unset, str] = UNSET
    required_switches: Union[Unset, int] = UNSET
    requeue: Union[Unset, bool] = UNSET
    resize_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    restart_cnt: Union[Unset, int] = UNSET
    resv_name: Union[Unset, str] = UNSET
    scheduled_nodes: Union[Unset, str] = UNSET
    selinux_context: Union[Unset, str] = UNSET
    shared: Union[Unset, list[V0042JobSharedItem]] = UNSET
    sockets_per_board: Union[Unset, int] = UNSET
    sockets_per_node: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    start_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    state_description: Union[Unset, str] = UNSET
    state_reason: Union[Unset, str] = UNSET
    standard_error: Union[Unset, str] = UNSET
    standard_input: Union[Unset, str] = UNSET
    standard_output: Union[Unset, str] = UNSET
    submit_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    suspend_time: Union[Unset, "V0042Uint64NoValStruct"] = UNSET
    system_comment: Union[Unset, str] = UNSET
    time_limit: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    time_minimum: Union[Unset, "V0042Uint32NoValStruct"] = UNSET
    threads_per_core: Union[Unset, "V0042Uint16NoValStruct"] = UNSET
    tres_bind: Union[Unset, str] = UNSET
    tres_freq: Union[Unset, str] = UNSET
    tres_per_job: Union[Unset, str] = UNSET
    tres_per_node: Union[Unset, str] = UNSET
    tres_per_socket: Union[Unset, str] = UNSET
    tres_per_task: Union[Unset, str] = UNSET
    tres_req_str: Union[Unset, str] = UNSET
    tres_alloc_str: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    user_name: Union[Unset, str] = UNSET
    maximum_switch_wait_time: Union[Unset, int] = UNSET
    wckey: Union[Unset, str] = UNSET
    current_working_directory: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        accrue_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accrue_time, Unset):
            accrue_time = self.accrue_time.to_dict()

        admin_comment = self.admin_comment

        allocating_node = self.allocating_node

        array_job_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_job_id, Unset):
            array_job_id = self.array_job_id.to_dict()

        array_task_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_task_id, Unset):
            array_task_id = self.array_task_id.to_dict()

        array_max_tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array_max_tasks, Unset):
            array_max_tasks = self.array_max_tasks.to_dict()

        array_task_string = self.array_task_string

        association_id = self.association_id

        batch_features = self.batch_features

        batch_flag = self.batch_flag

        batch_host = self.batch_host

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = []
            for componentsschemasv0_0_42_job_flags_item_data in self.flags:
                componentsschemasv0_0_42_job_flags_item = componentsschemasv0_0_42_job_flags_item_data.value
                flags.append(componentsschemasv0_0_42_job_flags_item)

        burst_buffer = self.burst_buffer

        burst_buffer_state = self.burst_buffer_state

        cluster = self.cluster

        cluster_features = self.cluster_features

        command = self.command

        comment = self.comment

        container = self.container

        container_id = self.container_id

        contiguous = self.contiguous

        core_spec = self.core_spec

        thread_spec = self.thread_spec

        cores_per_socket: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cores_per_socket, Unset):
            cores_per_socket = self.cores_per_socket.to_dict()

        billable_tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.billable_tres, Unset):
            billable_tres = self.billable_tres.to_dict()

        cpus_per_task: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus_per_task, Unset):
            cpus_per_task = self.cpus_per_task.to_dict()

        cpu_frequency_minimum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_minimum, Unset):
            cpu_frequency_minimum = self.cpu_frequency_minimum.to_dict()

        cpu_frequency_maximum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_maximum, Unset):
            cpu_frequency_maximum = self.cpu_frequency_maximum.to_dict()

        cpu_frequency_governor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu_frequency_governor, Unset):
            cpu_frequency_governor = self.cpu_frequency_governor.to_dict()

        cpus_per_tres = self.cpus_per_tres

        cron = self.cron

        deadline: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.deadline, Unset):
            deadline = self.deadline.to_dict()

        delay_boot: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.delay_boot, Unset):
            delay_boot = self.delay_boot.to_dict()

        dependency = self.dependency

        derived_exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.derived_exit_code, Unset):
            derived_exit_code = self.derived_exit_code.to_dict()

        eligible_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.eligible_time, Unset):
            eligible_time = self.eligible_time.to_dict()

        end_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.to_dict()

        excluded_nodes = self.excluded_nodes

        exit_code: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exit_code, Unset):
            exit_code = self.exit_code.to_dict()

        extra = self.extra

        failed_node = self.failed_node

        features = self.features

        federation_origin = self.federation_origin

        federation_siblings_active = self.federation_siblings_active

        federation_siblings_viable = self.federation_siblings_viable

        gres_detail: Union[Unset, list[str]] = UNSET
        if not isinstance(self.gres_detail, Unset):
            gres_detail = self.gres_detail

        group_id = self.group_id

        group_name = self.group_name

        het_job_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.het_job_id, Unset):
            het_job_id = self.het_job_id.to_dict()

        het_job_id_set = self.het_job_id_set

        het_job_offset: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.het_job_offset, Unset):
            het_job_offset = self.het_job_offset.to_dict()

        job_id = self.job_id

        job_resources: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job_resources, Unset):
            job_resources = self.job_resources.to_dict()

        job_size_str: Union[Unset, list[str]] = UNSET
        if not isinstance(self.job_size_str, Unset):
            job_size_str = self.job_size_str

        job_state: Union[Unset, list[str]] = UNSET
        if not isinstance(self.job_state, Unset):
            job_state = []
            for componentsschemasv0_0_42_job_state_item_data in self.job_state:
                componentsschemasv0_0_42_job_state_item = componentsschemasv0_0_42_job_state_item_data.value
                job_state.append(componentsschemasv0_0_42_job_state_item)

        last_sched_evaluation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.last_sched_evaluation, Unset):
            last_sched_evaluation = self.last_sched_evaluation.to_dict()

        licenses = self.licenses

        mail_type: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mail_type, Unset):
            mail_type = []
            for componentsschemasv0_0_42_job_mail_flags_item_data in self.mail_type:
                componentsschemasv0_0_42_job_mail_flags_item = componentsschemasv0_0_42_job_mail_flags_item_data.value
                mail_type.append(componentsschemasv0_0_42_job_mail_flags_item)

        mail_user = self.mail_user

        max_cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_cpus, Unset):
            max_cpus = self.max_cpus.to_dict()

        max_nodes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.max_nodes, Unset):
            max_nodes = self.max_nodes.to_dict()

        mcs_label = self.mcs_label

        memory_per_tres = self.memory_per_tres

        name = self.name

        network = self.network

        nodes = self.nodes

        nice = self.nice

        tasks_per_core: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_core, Unset):
            tasks_per_core = self.tasks_per_core.to_dict()

        tasks_per_tres: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_tres, Unset):
            tasks_per_tres = self.tasks_per_tres.to_dict()

        tasks_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_node, Unset):
            tasks_per_node = self.tasks_per_node.to_dict()

        tasks_per_socket: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_socket, Unset):
            tasks_per_socket = self.tasks_per_socket.to_dict()

        tasks_per_board: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks_per_board, Unset):
            tasks_per_board = self.tasks_per_board.to_dict()

        cpus: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpus, Unset):
            cpus = self.cpus.to_dict()

        node_count: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.node_count, Unset):
            node_count = self.node_count.to_dict()

        tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = self.tasks.to_dict()

        partition = self.partition

        prefer = self.prefer

        memory_per_cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_cpu, Unset):
            memory_per_cpu = self.memory_per_cpu.to_dict()

        memory_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_per_node, Unset):
            memory_per_node = self.memory_per_node.to_dict()

        minimum_cpus_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimum_cpus_per_node, Unset):
            minimum_cpus_per_node = self.minimum_cpus_per_node.to_dict()

        minimum_tmp_disk_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.minimum_tmp_disk_per_node, Unset):
            minimum_tmp_disk_per_node = self.minimum_tmp_disk_per_node.to_dict()

        power: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.power, Unset):
            power = self.power.to_dict()

        preempt_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.preempt_time, Unset):
            preempt_time = self.preempt_time.to_dict()

        preemptable_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.preemptable_time, Unset):
            preemptable_time = self.preemptable_time.to_dict()

        pre_sus_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pre_sus_time, Unset):
            pre_sus_time = self.pre_sus_time.to_dict()

        hold = self.hold

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        priority_by_partition: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.priority_by_partition, Unset):
            priority_by_partition = []
            for componentsschemasv0_0_42_priority_by_partition_item_data in self.priority_by_partition:
                componentsschemasv0_0_42_priority_by_partition_item = (
                    componentsschemasv0_0_42_priority_by_partition_item_data.to_dict()
                )
                priority_by_partition.append(componentsschemasv0_0_42_priority_by_partition_item)

        profile: Union[Unset, list[str]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = []
            for componentsschemasv0_0_42_acct_gather_profile_item_data in self.profile:
                componentsschemasv0_0_42_acct_gather_profile_item = (
                    componentsschemasv0_0_42_acct_gather_profile_item_data.value
                )
                profile.append(componentsschemasv0_0_42_acct_gather_profile_item)

        qos = self.qos

        reboot = self.reboot

        required_nodes = self.required_nodes

        required_switches = self.required_switches

        requeue = self.requeue

        resize_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resize_time, Unset):
            resize_time = self.resize_time.to_dict()

        restart_cnt = self.restart_cnt

        resv_name = self.resv_name

        scheduled_nodes = self.scheduled_nodes

        selinux_context = self.selinux_context

        shared: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shared, Unset):
            shared = []
            for componentsschemasv0_0_42_job_shared_item_data in self.shared:
                componentsschemasv0_0_42_job_shared_item = componentsschemasv0_0_42_job_shared_item_data.value
                shared.append(componentsschemasv0_0_42_job_shared_item)

        sockets_per_board = self.sockets_per_board

        sockets_per_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sockets_per_node, Unset):
            sockets_per_node = self.sockets_per_node.to_dict()

        start_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.to_dict()

        state_description = self.state_description

        state_reason = self.state_reason

        standard_error = self.standard_error

        standard_input = self.standard_input

        standard_output = self.standard_output

        submit_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.submit_time, Unset):
            submit_time = self.submit_time.to_dict()

        suspend_time: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.suspend_time, Unset):
            suspend_time = self.suspend_time.to_dict()

        system_comment = self.system_comment

        time_limit: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_limit, Unset):
            time_limit = self.time_limit.to_dict()

        time_minimum: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.time_minimum, Unset):
            time_minimum = self.time_minimum.to_dict()

        threads_per_core: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.threads_per_core, Unset):
            threads_per_core = self.threads_per_core.to_dict()

        tres_bind = self.tres_bind

        tres_freq = self.tres_freq

        tres_per_job = self.tres_per_job

        tres_per_node = self.tres_per_node

        tres_per_socket = self.tres_per_socket

        tres_per_task = self.tres_per_task

        tres_req_str = self.tres_req_str

        tres_alloc_str = self.tres_alloc_str

        user_id = self.user_id

        user_name = self.user_name

        maximum_switch_wait_time = self.maximum_switch_wait_time

        wckey = self.wckey

        current_working_directory = self.current_working_directory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if accrue_time is not UNSET:
            field_dict["accrue_time"] = accrue_time
        if admin_comment is not UNSET:
            field_dict["admin_comment"] = admin_comment
        if allocating_node is not UNSET:
            field_dict["allocating_node"] = allocating_node
        if array_job_id is not UNSET:
            field_dict["array_job_id"] = array_job_id
        if array_task_id is not UNSET:
            field_dict["array_task_id"] = array_task_id
        if array_max_tasks is not UNSET:
            field_dict["array_max_tasks"] = array_max_tasks
        if array_task_string is not UNSET:
            field_dict["array_task_string"] = array_task_string
        if association_id is not UNSET:
            field_dict["association_id"] = association_id
        if batch_features is not UNSET:
            field_dict["batch_features"] = batch_features
        if batch_flag is not UNSET:
            field_dict["batch_flag"] = batch_flag
        if batch_host is not UNSET:
            field_dict["batch_host"] = batch_host
        if flags is not UNSET:
            field_dict["flags"] = flags
        if burst_buffer is not UNSET:
            field_dict["burst_buffer"] = burst_buffer
        if burst_buffer_state is not UNSET:
            field_dict["burst_buffer_state"] = burst_buffer_state
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if cluster_features is not UNSET:
            field_dict["cluster_features"] = cluster_features
        if command is not UNSET:
            field_dict["command"] = command
        if comment is not UNSET:
            field_dict["comment"] = comment
        if container is not UNSET:
            field_dict["container"] = container
        if container_id is not UNSET:
            field_dict["container_id"] = container_id
        if contiguous is not UNSET:
            field_dict["contiguous"] = contiguous
        if core_spec is not UNSET:
            field_dict["core_spec"] = core_spec
        if thread_spec is not UNSET:
            field_dict["thread_spec"] = thread_spec
        if cores_per_socket is not UNSET:
            field_dict["cores_per_socket"] = cores_per_socket
        if billable_tres is not UNSET:
            field_dict["billable_tres"] = billable_tres
        if cpus_per_task is not UNSET:
            field_dict["cpus_per_task"] = cpus_per_task
        if cpu_frequency_minimum is not UNSET:
            field_dict["cpu_frequency_minimum"] = cpu_frequency_minimum
        if cpu_frequency_maximum is not UNSET:
            field_dict["cpu_frequency_maximum"] = cpu_frequency_maximum
        if cpu_frequency_governor is not UNSET:
            field_dict["cpu_frequency_governor"] = cpu_frequency_governor
        if cpus_per_tres is not UNSET:
            field_dict["cpus_per_tres"] = cpus_per_tres
        if cron is not UNSET:
            field_dict["cron"] = cron
        if deadline is not UNSET:
            field_dict["deadline"] = deadline
        if delay_boot is not UNSET:
            field_dict["delay_boot"] = delay_boot
        if dependency is not UNSET:
            field_dict["dependency"] = dependency
        if derived_exit_code is not UNSET:
            field_dict["derived_exit_code"] = derived_exit_code
        if eligible_time is not UNSET:
            field_dict["eligible_time"] = eligible_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if excluded_nodes is not UNSET:
            field_dict["excluded_nodes"] = excluded_nodes
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if extra is not UNSET:
            field_dict["extra"] = extra
        if failed_node is not UNSET:
            field_dict["failed_node"] = failed_node
        if features is not UNSET:
            field_dict["features"] = features
        if federation_origin is not UNSET:
            field_dict["federation_origin"] = federation_origin
        if federation_siblings_active is not UNSET:
            field_dict["federation_siblings_active"] = federation_siblings_active
        if federation_siblings_viable is not UNSET:
            field_dict["federation_siblings_viable"] = federation_siblings_viable
        if gres_detail is not UNSET:
            field_dict["gres_detail"] = gres_detail
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if het_job_id is not UNSET:
            field_dict["het_job_id"] = het_job_id
        if het_job_id_set is not UNSET:
            field_dict["het_job_id_set"] = het_job_id_set
        if het_job_offset is not UNSET:
            field_dict["het_job_offset"] = het_job_offset
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_resources is not UNSET:
            field_dict["job_resources"] = job_resources
        if job_size_str is not UNSET:
            field_dict["job_size_str"] = job_size_str
        if job_state is not UNSET:
            field_dict["job_state"] = job_state
        if last_sched_evaluation is not UNSET:
            field_dict["last_sched_evaluation"] = last_sched_evaluation
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if mail_type is not UNSET:
            field_dict["mail_type"] = mail_type
        if mail_user is not UNSET:
            field_dict["mail_user"] = mail_user
        if max_cpus is not UNSET:
            field_dict["max_cpus"] = max_cpus
        if max_nodes is not UNSET:
            field_dict["max_nodes"] = max_nodes
        if mcs_label is not UNSET:
            field_dict["mcs_label"] = mcs_label
        if memory_per_tres is not UNSET:
            field_dict["memory_per_tres"] = memory_per_tres
        if name is not UNSET:
            field_dict["name"] = name
        if network is not UNSET:
            field_dict["network"] = network
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if nice is not UNSET:
            field_dict["nice"] = nice
        if tasks_per_core is not UNSET:
            field_dict["tasks_per_core"] = tasks_per_core
        if tasks_per_tres is not UNSET:
            field_dict["tasks_per_tres"] = tasks_per_tres
        if tasks_per_node is not UNSET:
            field_dict["tasks_per_node"] = tasks_per_node
        if tasks_per_socket is not UNSET:
            field_dict["tasks_per_socket"] = tasks_per_socket
        if tasks_per_board is not UNSET:
            field_dict["tasks_per_board"] = tasks_per_board
        if cpus is not UNSET:
            field_dict["cpus"] = cpus
        if node_count is not UNSET:
            field_dict["node_count"] = node_count
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if partition is not UNSET:
            field_dict["partition"] = partition
        if prefer is not UNSET:
            field_dict["prefer"] = prefer
        if memory_per_cpu is not UNSET:
            field_dict["memory_per_cpu"] = memory_per_cpu
        if memory_per_node is not UNSET:
            field_dict["memory_per_node"] = memory_per_node
        if minimum_cpus_per_node is not UNSET:
            field_dict["minimum_cpus_per_node"] = minimum_cpus_per_node
        if minimum_tmp_disk_per_node is not UNSET:
            field_dict["minimum_tmp_disk_per_node"] = minimum_tmp_disk_per_node
        if power is not UNSET:
            field_dict["power"] = power
        if preempt_time is not UNSET:
            field_dict["preempt_time"] = preempt_time
        if preemptable_time is not UNSET:
            field_dict["preemptable_time"] = preemptable_time
        if pre_sus_time is not UNSET:
            field_dict["pre_sus_time"] = pre_sus_time
        if hold is not UNSET:
            field_dict["hold"] = hold
        if priority is not UNSET:
            field_dict["priority"] = priority
        if priority_by_partition is not UNSET:
            field_dict["priority_by_partition"] = priority_by_partition
        if profile is not UNSET:
            field_dict["profile"] = profile
        if qos is not UNSET:
            field_dict["qos"] = qos
        if reboot is not UNSET:
            field_dict["reboot"] = reboot
        if required_nodes is not UNSET:
            field_dict["required_nodes"] = required_nodes
        if required_switches is not UNSET:
            field_dict["required_switches"] = required_switches
        if requeue is not UNSET:
            field_dict["requeue"] = requeue
        if resize_time is not UNSET:
            field_dict["resize_time"] = resize_time
        if restart_cnt is not UNSET:
            field_dict["restart_cnt"] = restart_cnt
        if resv_name is not UNSET:
            field_dict["resv_name"] = resv_name
        if scheduled_nodes is not UNSET:
            field_dict["scheduled_nodes"] = scheduled_nodes
        if selinux_context is not UNSET:
            field_dict["selinux_context"] = selinux_context
        if shared is not UNSET:
            field_dict["shared"] = shared
        if sockets_per_board is not UNSET:
            field_dict["sockets_per_board"] = sockets_per_board
        if sockets_per_node is not UNSET:
            field_dict["sockets_per_node"] = sockets_per_node
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if state_description is not UNSET:
            field_dict["state_description"] = state_description
        if state_reason is not UNSET:
            field_dict["state_reason"] = state_reason
        if standard_error is not UNSET:
            field_dict["standard_error"] = standard_error
        if standard_input is not UNSET:
            field_dict["standard_input"] = standard_input
        if standard_output is not UNSET:
            field_dict["standard_output"] = standard_output
        if submit_time is not UNSET:
            field_dict["submit_time"] = submit_time
        if suspend_time is not UNSET:
            field_dict["suspend_time"] = suspend_time
        if system_comment is not UNSET:
            field_dict["system_comment"] = system_comment
        if time_limit is not UNSET:
            field_dict["time_limit"] = time_limit
        if time_minimum is not UNSET:
            field_dict["time_minimum"] = time_minimum
        if threads_per_core is not UNSET:
            field_dict["threads_per_core"] = threads_per_core
        if tres_bind is not UNSET:
            field_dict["tres_bind"] = tres_bind
        if tres_freq is not UNSET:
            field_dict["tres_freq"] = tres_freq
        if tres_per_job is not UNSET:
            field_dict["tres_per_job"] = tres_per_job
        if tres_per_node is not UNSET:
            field_dict["tres_per_node"] = tres_per_node
        if tres_per_socket is not UNSET:
            field_dict["tres_per_socket"] = tres_per_socket
        if tres_per_task is not UNSET:
            field_dict["tres_per_task"] = tres_per_task
        if tres_req_str is not UNSET:
            field_dict["tres_req_str"] = tres_req_str
        if tres_alloc_str is not UNSET:
            field_dict["tres_alloc_str"] = tres_alloc_str
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if maximum_switch_wait_time is not UNSET:
            field_dict["maximum_switch_wait_time"] = maximum_switch_wait_time
        if wckey is not UNSET:
            field_dict["wckey"] = wckey
        if current_working_directory is not UNSET:
            field_dict["current_working_directory"] = current_working_directory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.v0042_float_64_no_val_struct import V0042Float64NoValStruct
        from ..models.v0042_job_info_power import V0042JobInfoPower
        from ..models.v0042_job_res import V0042JobRes
        from ..models.v0042_part_prio import V0042PartPrio
        from ..models.v0042_process_exit_code_verbose import V0042ProcessExitCodeVerbose
        from ..models.v0042_uint_16_no_val_struct import V0042Uint16NoValStruct
        from ..models.v0042_uint_32_no_val_struct import V0042Uint32NoValStruct
        from ..models.v0042_uint_64_no_val_struct import V0042Uint64NoValStruct

        d = dict(src_dict)
        account = d.pop("account", UNSET)

        _accrue_time = d.pop("accrue_time", UNSET)
        accrue_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_accrue_time, Unset):
            accrue_time = UNSET
        else:
            accrue_time = V0042Uint64NoValStruct.from_dict(_accrue_time)

        admin_comment = d.pop("admin_comment", UNSET)

        allocating_node = d.pop("allocating_node", UNSET)

        _array_job_id = d.pop("array_job_id", UNSET)
        array_job_id: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_array_job_id, Unset):
            array_job_id = UNSET
        else:
            array_job_id = V0042Uint32NoValStruct.from_dict(_array_job_id)

        _array_task_id = d.pop("array_task_id", UNSET)
        array_task_id: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_array_task_id, Unset):
            array_task_id = UNSET
        else:
            array_task_id = V0042Uint32NoValStruct.from_dict(_array_task_id)

        _array_max_tasks = d.pop("array_max_tasks", UNSET)
        array_max_tasks: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_array_max_tasks, Unset):
            array_max_tasks = UNSET
        else:
            array_max_tasks = V0042Uint32NoValStruct.from_dict(_array_max_tasks)

        array_task_string = d.pop("array_task_string", UNSET)

        association_id = d.pop("association_id", UNSET)

        batch_features = d.pop("batch_features", UNSET)

        batch_flag = d.pop("batch_flag", UNSET)

        batch_host = d.pop("batch_host", UNSET)

        flags = []
        _flags = d.pop("flags", UNSET)
        for componentsschemasv0_0_42_job_flags_item_data in _flags or []:
            componentsschemasv0_0_42_job_flags_item = V0042JobFlagsItem(componentsschemasv0_0_42_job_flags_item_data)

            flags.append(componentsschemasv0_0_42_job_flags_item)

        burst_buffer = d.pop("burst_buffer", UNSET)

        burst_buffer_state = d.pop("burst_buffer_state", UNSET)

        cluster = d.pop("cluster", UNSET)

        cluster_features = d.pop("cluster_features", UNSET)

        command = d.pop("command", UNSET)

        comment = d.pop("comment", UNSET)

        container = d.pop("container", UNSET)

        container_id = d.pop("container_id", UNSET)

        contiguous = d.pop("contiguous", UNSET)

        core_spec = d.pop("core_spec", UNSET)

        thread_spec = d.pop("thread_spec", UNSET)

        _cores_per_socket = d.pop("cores_per_socket", UNSET)
        cores_per_socket: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_cores_per_socket, Unset):
            cores_per_socket = UNSET
        else:
            cores_per_socket = V0042Uint16NoValStruct.from_dict(_cores_per_socket)

        _billable_tres = d.pop("billable_tres", UNSET)
        billable_tres: Union[Unset, V0042Float64NoValStruct]
        if isinstance(_billable_tres, Unset):
            billable_tres = UNSET
        else:
            billable_tres = V0042Float64NoValStruct.from_dict(_billable_tres)

        _cpus_per_task = d.pop("cpus_per_task", UNSET)
        cpus_per_task: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_cpus_per_task, Unset):
            cpus_per_task = UNSET
        else:
            cpus_per_task = V0042Uint16NoValStruct.from_dict(_cpus_per_task)

        _cpu_frequency_minimum = d.pop("cpu_frequency_minimum", UNSET)
        cpu_frequency_minimum: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_cpu_frequency_minimum, Unset):
            cpu_frequency_minimum = UNSET
        else:
            cpu_frequency_minimum = V0042Uint32NoValStruct.from_dict(_cpu_frequency_minimum)

        _cpu_frequency_maximum = d.pop("cpu_frequency_maximum", UNSET)
        cpu_frequency_maximum: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_cpu_frequency_maximum, Unset):
            cpu_frequency_maximum = UNSET
        else:
            cpu_frequency_maximum = V0042Uint32NoValStruct.from_dict(_cpu_frequency_maximum)

        _cpu_frequency_governor = d.pop("cpu_frequency_governor", UNSET)
        cpu_frequency_governor: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_cpu_frequency_governor, Unset):
            cpu_frequency_governor = UNSET
        else:
            cpu_frequency_governor = V0042Uint32NoValStruct.from_dict(_cpu_frequency_governor)

        cpus_per_tres = d.pop("cpus_per_tres", UNSET)

        cron = d.pop("cron", UNSET)

        _deadline = d.pop("deadline", UNSET)
        deadline: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_deadline, Unset):
            deadline = UNSET
        else:
            deadline = V0042Uint64NoValStruct.from_dict(_deadline)

        _delay_boot = d.pop("delay_boot", UNSET)
        delay_boot: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_delay_boot, Unset):
            delay_boot = UNSET
        else:
            delay_boot = V0042Uint32NoValStruct.from_dict(_delay_boot)

        dependency = d.pop("dependency", UNSET)

        _derived_exit_code = d.pop("derived_exit_code", UNSET)
        derived_exit_code: Union[Unset, V0042ProcessExitCodeVerbose]
        if isinstance(_derived_exit_code, Unset):
            derived_exit_code = UNSET
        else:
            derived_exit_code = V0042ProcessExitCodeVerbose.from_dict(_derived_exit_code)

        _eligible_time = d.pop("eligible_time", UNSET)
        eligible_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_eligible_time, Unset):
            eligible_time = UNSET
        else:
            eligible_time = V0042Uint64NoValStruct.from_dict(_eligible_time)

        _end_time = d.pop("end_time", UNSET)
        end_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = V0042Uint64NoValStruct.from_dict(_end_time)

        excluded_nodes = d.pop("excluded_nodes", UNSET)

        _exit_code = d.pop("exit_code", UNSET)
        exit_code: Union[Unset, V0042ProcessExitCodeVerbose]
        if isinstance(_exit_code, Unset):
            exit_code = UNSET
        else:
            exit_code = V0042ProcessExitCodeVerbose.from_dict(_exit_code)

        extra = d.pop("extra", UNSET)

        failed_node = d.pop("failed_node", UNSET)

        features = d.pop("features", UNSET)

        federation_origin = d.pop("federation_origin", UNSET)

        federation_siblings_active = d.pop("federation_siblings_active", UNSET)

        federation_siblings_viable = d.pop("federation_siblings_viable", UNSET)

        gres_detail = cast(list[str], d.pop("gres_detail", UNSET))

        group_id = d.pop("group_id", UNSET)

        group_name = d.pop("group_name", UNSET)

        _het_job_id = d.pop("het_job_id", UNSET)
        het_job_id: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_het_job_id, Unset):
            het_job_id = UNSET
        else:
            het_job_id = V0042Uint32NoValStruct.from_dict(_het_job_id)

        het_job_id_set = d.pop("het_job_id_set", UNSET)

        _het_job_offset = d.pop("het_job_offset", UNSET)
        het_job_offset: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_het_job_offset, Unset):
            het_job_offset = UNSET
        else:
            het_job_offset = V0042Uint32NoValStruct.from_dict(_het_job_offset)

        job_id = d.pop("job_id", UNSET)

        _job_resources = d.pop("job_resources", UNSET)
        job_resources: Union[Unset, V0042JobRes]
        if isinstance(_job_resources, Unset):
            job_resources = UNSET
        else:
            job_resources = V0042JobRes.from_dict(_job_resources)

        job_size_str = cast(list[str], d.pop("job_size_str", UNSET))

        job_state = []
        _job_state = d.pop("job_state", UNSET)
        for componentsschemasv0_0_42_job_state_item_data in _job_state or []:
            componentsschemasv0_0_42_job_state_item = V0042JobStateItem(componentsschemasv0_0_42_job_state_item_data)

            job_state.append(componentsschemasv0_0_42_job_state_item)

        _last_sched_evaluation = d.pop("last_sched_evaluation", UNSET)
        last_sched_evaluation: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_last_sched_evaluation, Unset):
            last_sched_evaluation = UNSET
        else:
            last_sched_evaluation = V0042Uint64NoValStruct.from_dict(_last_sched_evaluation)

        licenses = d.pop("licenses", UNSET)

        mail_type = []
        _mail_type = d.pop("mail_type", UNSET)
        for componentsschemasv0_0_42_job_mail_flags_item_data in _mail_type or []:
            componentsschemasv0_0_42_job_mail_flags_item = V0042JobMailFlagsItem(
                componentsschemasv0_0_42_job_mail_flags_item_data
            )

            mail_type.append(componentsschemasv0_0_42_job_mail_flags_item)

        mail_user = d.pop("mail_user", UNSET)

        _max_cpus = d.pop("max_cpus", UNSET)
        max_cpus: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_max_cpus, Unset):
            max_cpus = UNSET
        else:
            max_cpus = V0042Uint32NoValStruct.from_dict(_max_cpus)

        _max_nodes = d.pop("max_nodes", UNSET)
        max_nodes: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_max_nodes, Unset):
            max_nodes = UNSET
        else:
            max_nodes = V0042Uint32NoValStruct.from_dict(_max_nodes)

        mcs_label = d.pop("mcs_label", UNSET)

        memory_per_tres = d.pop("memory_per_tres", UNSET)

        name = d.pop("name", UNSET)

        network = d.pop("network", UNSET)

        nodes = d.pop("nodes", UNSET)

        nice = d.pop("nice", UNSET)

        _tasks_per_core = d.pop("tasks_per_core", UNSET)
        tasks_per_core: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_tasks_per_core, Unset):
            tasks_per_core = UNSET
        else:
            tasks_per_core = V0042Uint16NoValStruct.from_dict(_tasks_per_core)

        _tasks_per_tres = d.pop("tasks_per_tres", UNSET)
        tasks_per_tres: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_tasks_per_tres, Unset):
            tasks_per_tres = UNSET
        else:
            tasks_per_tres = V0042Uint16NoValStruct.from_dict(_tasks_per_tres)

        _tasks_per_node = d.pop("tasks_per_node", UNSET)
        tasks_per_node: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_tasks_per_node, Unset):
            tasks_per_node = UNSET
        else:
            tasks_per_node = V0042Uint16NoValStruct.from_dict(_tasks_per_node)

        _tasks_per_socket = d.pop("tasks_per_socket", UNSET)
        tasks_per_socket: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_tasks_per_socket, Unset):
            tasks_per_socket = UNSET
        else:
            tasks_per_socket = V0042Uint16NoValStruct.from_dict(_tasks_per_socket)

        _tasks_per_board = d.pop("tasks_per_board", UNSET)
        tasks_per_board: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_tasks_per_board, Unset):
            tasks_per_board = UNSET
        else:
            tasks_per_board = V0042Uint16NoValStruct.from_dict(_tasks_per_board)

        _cpus = d.pop("cpus", UNSET)
        cpus: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_cpus, Unset):
            cpus = UNSET
        else:
            cpus = V0042Uint32NoValStruct.from_dict(_cpus)

        _node_count = d.pop("node_count", UNSET)
        node_count: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_node_count, Unset):
            node_count = UNSET
        else:
            node_count = V0042Uint32NoValStruct.from_dict(_node_count)

        _tasks = d.pop("tasks", UNSET)
        tasks: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_tasks, Unset):
            tasks = UNSET
        else:
            tasks = V0042Uint32NoValStruct.from_dict(_tasks)

        partition = d.pop("partition", UNSET)

        prefer = d.pop("prefer", UNSET)

        _memory_per_cpu = d.pop("memory_per_cpu", UNSET)
        memory_per_cpu: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_memory_per_cpu, Unset):
            memory_per_cpu = UNSET
        else:
            memory_per_cpu = V0042Uint64NoValStruct.from_dict(_memory_per_cpu)

        _memory_per_node = d.pop("memory_per_node", UNSET)
        memory_per_node: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_memory_per_node, Unset):
            memory_per_node = UNSET
        else:
            memory_per_node = V0042Uint64NoValStruct.from_dict(_memory_per_node)

        _minimum_cpus_per_node = d.pop("minimum_cpus_per_node", UNSET)
        minimum_cpus_per_node: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_minimum_cpus_per_node, Unset):
            minimum_cpus_per_node = UNSET
        else:
            minimum_cpus_per_node = V0042Uint16NoValStruct.from_dict(_minimum_cpus_per_node)

        _minimum_tmp_disk_per_node = d.pop("minimum_tmp_disk_per_node", UNSET)
        minimum_tmp_disk_per_node: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_minimum_tmp_disk_per_node, Unset):
            minimum_tmp_disk_per_node = UNSET
        else:
            minimum_tmp_disk_per_node = V0042Uint32NoValStruct.from_dict(_minimum_tmp_disk_per_node)

        _power = d.pop("power", UNSET)
        power: Union[Unset, V0042JobInfoPower]
        if isinstance(_power, Unset):
            power = UNSET
        else:
            power = V0042JobInfoPower.from_dict(_power)

        _preempt_time = d.pop("preempt_time", UNSET)
        preempt_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_preempt_time, Unset):
            preempt_time = UNSET
        else:
            preempt_time = V0042Uint64NoValStruct.from_dict(_preempt_time)

        _preemptable_time = d.pop("preemptable_time", UNSET)
        preemptable_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_preemptable_time, Unset):
            preemptable_time = UNSET
        else:
            preemptable_time = V0042Uint64NoValStruct.from_dict(_preemptable_time)

        _pre_sus_time = d.pop("pre_sus_time", UNSET)
        pre_sus_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_pre_sus_time, Unset):
            pre_sus_time = UNSET
        else:
            pre_sus_time = V0042Uint64NoValStruct.from_dict(_pre_sus_time)

        hold = d.pop("hold", UNSET)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = V0042Uint32NoValStruct.from_dict(_priority)

        priority_by_partition = []
        _priority_by_partition = d.pop("priority_by_partition", UNSET)
        for componentsschemasv0_0_42_priority_by_partition_item_data in _priority_by_partition or []:
            componentsschemasv0_0_42_priority_by_partition_item = V0042PartPrio.from_dict(
                componentsschemasv0_0_42_priority_by_partition_item_data
            )

            priority_by_partition.append(componentsschemasv0_0_42_priority_by_partition_item)

        profile = []
        _profile = d.pop("profile", UNSET)
        for componentsschemasv0_0_42_acct_gather_profile_item_data in _profile or []:
            componentsschemasv0_0_42_acct_gather_profile_item = V0042AcctGatherProfileItem(
                componentsschemasv0_0_42_acct_gather_profile_item_data
            )

            profile.append(componentsschemasv0_0_42_acct_gather_profile_item)

        qos = d.pop("qos", UNSET)

        reboot = d.pop("reboot", UNSET)

        required_nodes = d.pop("required_nodes", UNSET)

        required_switches = d.pop("required_switches", UNSET)

        requeue = d.pop("requeue", UNSET)

        _resize_time = d.pop("resize_time", UNSET)
        resize_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_resize_time, Unset):
            resize_time = UNSET
        else:
            resize_time = V0042Uint64NoValStruct.from_dict(_resize_time)

        restart_cnt = d.pop("restart_cnt", UNSET)

        resv_name = d.pop("resv_name", UNSET)

        scheduled_nodes = d.pop("scheduled_nodes", UNSET)

        selinux_context = d.pop("selinux_context", UNSET)

        shared = []
        _shared = d.pop("shared", UNSET)
        for componentsschemasv0_0_42_job_shared_item_data in _shared or []:
            componentsschemasv0_0_42_job_shared_item = V0042JobSharedItem(componentsschemasv0_0_42_job_shared_item_data)

            shared.append(componentsschemasv0_0_42_job_shared_item)

        sockets_per_board = d.pop("sockets_per_board", UNSET)

        _sockets_per_node = d.pop("sockets_per_node", UNSET)
        sockets_per_node: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_sockets_per_node, Unset):
            sockets_per_node = UNSET
        else:
            sockets_per_node = V0042Uint16NoValStruct.from_dict(_sockets_per_node)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = V0042Uint64NoValStruct.from_dict(_start_time)

        state_description = d.pop("state_description", UNSET)

        state_reason = d.pop("state_reason", UNSET)

        standard_error = d.pop("standard_error", UNSET)

        standard_input = d.pop("standard_input", UNSET)

        standard_output = d.pop("standard_output", UNSET)

        _submit_time = d.pop("submit_time", UNSET)
        submit_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_submit_time, Unset):
            submit_time = UNSET
        else:
            submit_time = V0042Uint64NoValStruct.from_dict(_submit_time)

        _suspend_time = d.pop("suspend_time", UNSET)
        suspend_time: Union[Unset, V0042Uint64NoValStruct]
        if isinstance(_suspend_time, Unset):
            suspend_time = UNSET
        else:
            suspend_time = V0042Uint64NoValStruct.from_dict(_suspend_time)

        system_comment = d.pop("system_comment", UNSET)

        _time_limit = d.pop("time_limit", UNSET)
        time_limit: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_time_limit, Unset):
            time_limit = UNSET
        else:
            time_limit = V0042Uint32NoValStruct.from_dict(_time_limit)

        _time_minimum = d.pop("time_minimum", UNSET)
        time_minimum: Union[Unset, V0042Uint32NoValStruct]
        if isinstance(_time_minimum, Unset):
            time_minimum = UNSET
        else:
            time_minimum = V0042Uint32NoValStruct.from_dict(_time_minimum)

        _threads_per_core = d.pop("threads_per_core", UNSET)
        threads_per_core: Union[Unset, V0042Uint16NoValStruct]
        if isinstance(_threads_per_core, Unset):
            threads_per_core = UNSET
        else:
            threads_per_core = V0042Uint16NoValStruct.from_dict(_threads_per_core)

        tres_bind = d.pop("tres_bind", UNSET)

        tres_freq = d.pop("tres_freq", UNSET)

        tres_per_job = d.pop("tres_per_job", UNSET)

        tres_per_node = d.pop("tres_per_node", UNSET)

        tres_per_socket = d.pop("tres_per_socket", UNSET)

        tres_per_task = d.pop("tres_per_task", UNSET)

        tres_req_str = d.pop("tres_req_str", UNSET)

        tres_alloc_str = d.pop("tres_alloc_str", UNSET)

        user_id = d.pop("user_id", UNSET)

        user_name = d.pop("user_name", UNSET)

        maximum_switch_wait_time = d.pop("maximum_switch_wait_time", UNSET)

        wckey = d.pop("wckey", UNSET)

        current_working_directory = d.pop("current_working_directory", UNSET)

        v0042_job_info = cls(
            account=account,
            accrue_time=accrue_time,
            admin_comment=admin_comment,
            allocating_node=allocating_node,
            array_job_id=array_job_id,
            array_task_id=array_task_id,
            array_max_tasks=array_max_tasks,
            array_task_string=array_task_string,
            association_id=association_id,
            batch_features=batch_features,
            batch_flag=batch_flag,
            batch_host=batch_host,
            flags=flags,
            burst_buffer=burst_buffer,
            burst_buffer_state=burst_buffer_state,
            cluster=cluster,
            cluster_features=cluster_features,
            command=command,
            comment=comment,
            container=container,
            container_id=container_id,
            contiguous=contiguous,
            core_spec=core_spec,
            thread_spec=thread_spec,
            cores_per_socket=cores_per_socket,
            billable_tres=billable_tres,
            cpus_per_task=cpus_per_task,
            cpu_frequency_minimum=cpu_frequency_minimum,
            cpu_frequency_maximum=cpu_frequency_maximum,
            cpu_frequency_governor=cpu_frequency_governor,
            cpus_per_tres=cpus_per_tres,
            cron=cron,
            deadline=deadline,
            delay_boot=delay_boot,
            dependency=dependency,
            derived_exit_code=derived_exit_code,
            eligible_time=eligible_time,
            end_time=end_time,
            excluded_nodes=excluded_nodes,
            exit_code=exit_code,
            extra=extra,
            failed_node=failed_node,
            features=features,
            federation_origin=federation_origin,
            federation_siblings_active=federation_siblings_active,
            federation_siblings_viable=federation_siblings_viable,
            gres_detail=gres_detail,
            group_id=group_id,
            group_name=group_name,
            het_job_id=het_job_id,
            het_job_id_set=het_job_id_set,
            het_job_offset=het_job_offset,
            job_id=job_id,
            job_resources=job_resources,
            job_size_str=job_size_str,
            job_state=job_state,
            last_sched_evaluation=last_sched_evaluation,
            licenses=licenses,
            mail_type=mail_type,
            mail_user=mail_user,
            max_cpus=max_cpus,
            max_nodes=max_nodes,
            mcs_label=mcs_label,
            memory_per_tres=memory_per_tres,
            name=name,
            network=network,
            nodes=nodes,
            nice=nice,
            tasks_per_core=tasks_per_core,
            tasks_per_tres=tasks_per_tres,
            tasks_per_node=tasks_per_node,
            tasks_per_socket=tasks_per_socket,
            tasks_per_board=tasks_per_board,
            cpus=cpus,
            node_count=node_count,
            tasks=tasks,
            partition=partition,
            prefer=prefer,
            memory_per_cpu=memory_per_cpu,
            memory_per_node=memory_per_node,
            minimum_cpus_per_node=minimum_cpus_per_node,
            minimum_tmp_disk_per_node=minimum_tmp_disk_per_node,
            power=power,
            preempt_time=preempt_time,
            preemptable_time=preemptable_time,
            pre_sus_time=pre_sus_time,
            hold=hold,
            priority=priority,
            priority_by_partition=priority_by_partition,
            profile=profile,
            qos=qos,
            reboot=reboot,
            required_nodes=required_nodes,
            required_switches=required_switches,
            requeue=requeue,
            resize_time=resize_time,
            restart_cnt=restart_cnt,
            resv_name=resv_name,
            scheduled_nodes=scheduled_nodes,
            selinux_context=selinux_context,
            shared=shared,
            sockets_per_board=sockets_per_board,
            sockets_per_node=sockets_per_node,
            start_time=start_time,
            state_description=state_description,
            state_reason=state_reason,
            standard_error=standard_error,
            standard_input=standard_input,
            standard_output=standard_output,
            submit_time=submit_time,
            suspend_time=suspend_time,
            system_comment=system_comment,
            time_limit=time_limit,
            time_minimum=time_minimum,
            threads_per_core=threads_per_core,
            tres_bind=tres_bind,
            tres_freq=tres_freq,
            tres_per_job=tres_per_job,
            tres_per_node=tres_per_node,
            tres_per_socket=tres_per_socket,
            tres_per_task=tres_per_task,
            tres_req_str=tres_req_str,
            tres_alloc_str=tres_alloc_str,
            user_id=user_id,
            user_name=user_name,
            maximum_switch_wait_time=maximum_switch_wait_time,
            wckey=wckey,
            current_working_directory=current_working_directory,
        )

        v0042_job_info.additional_properties = d
        return v0042_job_info

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
