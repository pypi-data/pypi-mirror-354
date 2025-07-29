"""Contains all the data models used in inputs/outputs"""

from .slurm_v0042_delete_job_flags import SlurmV0042DeleteJobFlags
from .slurm_v0042_get_job_flags import SlurmV0042GetJobFlags
from .slurm_v0042_get_jobs_flags import SlurmV0042GetJobsFlags
from .slurm_v0042_get_jobs_state_flags import SlurmV0042GetJobsStateFlags
from .slurm_v0042_get_node_flags import SlurmV0042GetNodeFlags
from .slurm_v0042_get_nodes_flags import SlurmV0042GetNodesFlags
from .slurm_v0042_get_partition_flags import SlurmV0042GetPartitionFlags
from .slurm_v0042_get_partitions_flags import SlurmV0042GetPartitionsFlags
from .slurmdb_v0042_delete_cluster_classification import SlurmdbV0042DeleteClusterClassification
from .slurmdb_v0042_delete_cluster_flags import SlurmdbV0042DeleteClusterFlags
from .slurmdb_v0042_get_cluster_classification import SlurmdbV0042GetClusterClassification
from .slurmdb_v0042_get_cluster_flags import SlurmdbV0042GetClusterFlags
from .slurmdb_v0042_get_qos_preempt_mode import SlurmdbV0042GetQosPreemptMode
from .slurmdb_v0042_get_users_admin_level import SlurmdbV0042GetUsersAdminLevel
from .slurmdb_v0042_post_qos_preempt_mode import SlurmdbV0042PostQosPreemptMode
from .slurmdb_v0042_post_users_association_flags import SlurmdbV0042PostUsersAssociationFlags
from .v0042_account import V0042Account
from .v0042_account_flags_item import V0042AccountFlagsItem
from .v0042_account_short import V0042AccountShort
from .v0042_accounting import V0042Accounting
from .v0042_accounting_allocated import V0042AccountingAllocated
from .v0042_accounts_add_cond import V0042AccountsAddCond
from .v0042_acct_gather_energy import V0042AcctGatherEnergy
from .v0042_acct_gather_profile_item import V0042AcctGatherProfileItem
from .v0042_admin_lvl_item import V0042AdminLvlItem
from .v0042_assoc import V0042Assoc
from .v0042_assoc_default import V0042AssocDefault
from .v0042_assoc_flags_item import V0042AssocFlagsItem
from .v0042_assoc_max import V0042AssocMax
from .v0042_assoc_max_jobs import V0042AssocMaxJobs
from .v0042_assoc_max_jobs_per import V0042AssocMaxJobsPer
from .v0042_assoc_max_per import V0042AssocMaxPer
from .v0042_assoc_max_per_account import V0042AssocMaxPerAccount
from .v0042_assoc_max_tres import V0042AssocMaxTres
from .v0042_assoc_max_tres_group import V0042AssocMaxTresGroup
from .v0042_assoc_max_tres_minutes import V0042AssocMaxTresMinutes
from .v0042_assoc_max_tres_minutes_per import V0042AssocMaxTresMinutesPer
from .v0042_assoc_max_tres_per import V0042AssocMaxTresPer
from .v0042_assoc_min import V0042AssocMin
from .v0042_assoc_rec_set import V0042AssocRecSet
from .v0042_assoc_shares_obj_wrap import V0042AssocSharesObjWrap
from .v0042_assoc_shares_obj_wrap_fairshare import V0042AssocSharesObjWrapFairshare
from .v0042_assoc_shares_obj_wrap_tres import V0042AssocSharesObjWrapTres
from .v0042_assoc_shares_obj_wrap_type_item import V0042AssocSharesObjWrapTypeItem
from .v0042_assoc_short import V0042AssocShort
from .v0042_bf_exit_fields import V0042BfExitFields
from .v0042_cluster_rec import V0042ClusterRec
from .v0042_cluster_rec_associations import V0042ClusterRecAssociations
from .v0042_cluster_rec_controller import V0042ClusterRecController
from .v0042_cluster_rec_flags_item import V0042ClusterRecFlagsItem
from .v0042_controller_ping import V0042ControllerPing
from .v0042_coord import V0042Coord
from .v0042_cpu_binding_flags_item import V0042CpuBindingFlagsItem
from .v0042_cr_type_item import V0042CrTypeItem
from .v0042_cron_entry import V0042CronEntry
from .v0042_cron_entry_flags_item import V0042CronEntryFlagsItem
from .v0042_cron_entry_line import V0042CronEntryLine
from .v0042_float_64_no_val_struct import V0042Float64NoValStruct
from .v0042_instance import V0042Instance
from .v0042_instance_time import V0042InstanceTime
from .v0042_job import V0042Job
from .v0042_job_alloc_req import V0042JobAllocReq
from .v0042_job_array import V0042JobArray
from .v0042_job_array_limits import V0042JobArrayLimits
from .v0042_job_array_limits_max import V0042JobArrayLimitsMax
from .v0042_job_array_limits_max_running import V0042JobArrayLimitsMaxRunning
from .v0042_job_array_response_msg_entry import V0042JobArrayResponseMsgEntry
from .v0042_job_comment import V0042JobComment
from .v0042_job_desc_msg import V0042JobDescMsg
from .v0042_job_desc_msg_rlimits import V0042JobDescMsgRlimits
from .v0042_job_flags_item import V0042JobFlagsItem
from .v0042_job_het import V0042JobHet
from .v0042_job_info import V0042JobInfo
from .v0042_job_info_power import V0042JobInfoPower
from .v0042_job_mail_flags_item import V0042JobMailFlagsItem
from .v0042_job_mcs import V0042JobMcs
from .v0042_job_required import V0042JobRequired
from .v0042_job_res import V0042JobRes
from .v0042_job_res_core import V0042JobResCore
from .v0042_job_res_core_status_item import V0042JobResCoreStatusItem
from .v0042_job_res_node import V0042JobResNode
from .v0042_job_res_node_cpus import V0042JobResNodeCpus
from .v0042_job_res_node_memory import V0042JobResNodeMemory
from .v0042_job_res_nodes import V0042JobResNodes
from .v0042_job_res_socket import V0042JobResSocket
from .v0042_job_reservation import V0042JobReservation
from .v0042_job_shared_item import V0042JobSharedItem
from .v0042_job_state import V0042JobState
from .v0042_job_state_item import V0042JobStateItem
from .v0042_job_submit_req import V0042JobSubmitReq
from .v0042_job_time import V0042JobTime
from .v0042_job_time_system import V0042JobTimeSystem
from .v0042_job_time_total import V0042JobTimeTotal
from .v0042_job_time_user import V0042JobTimeUser
from .v0042_job_tres import V0042JobTres
from .v0042_kill_jobs_msg import V0042KillJobsMsg
from .v0042_kill_jobs_resp_job import V0042KillJobsRespJob
from .v0042_kill_jobs_resp_job_error import V0042KillJobsRespJobError
from .v0042_kill_jobs_resp_job_federation import V0042KillJobsRespJobFederation
from .v0042_license import V0042License
from .v0042_memory_binding_type_item import V0042MemoryBindingTypeItem
from .v0042_node import V0042Node
from .v0042_node_cr_type_item import V0042NodeCrTypeItem
from .v0042_node_external_sensors import V0042NodeExternalSensors
from .v0042_node_power import V0042NodePower
from .v0042_node_states_item import V0042NodeStatesItem
from .v0042_open_mode_item import V0042OpenModeItem
from .v0042_openapi_accounts_add_cond_resp import V0042OpenapiAccountsAddCondResp
from .v0042_openapi_accounts_add_cond_resp_str import V0042OpenapiAccountsAddCondRespStr
from .v0042_openapi_accounts_removed_resp import V0042OpenapiAccountsRemovedResp
from .v0042_openapi_accounts_resp import V0042OpenapiAccountsResp
from .v0042_openapi_assocs_removed_resp import V0042OpenapiAssocsRemovedResp
from .v0042_openapi_assocs_resp import V0042OpenapiAssocsResp
from .v0042_openapi_clusters_removed_resp import V0042OpenapiClustersRemovedResp
from .v0042_openapi_clusters_resp import V0042OpenapiClustersResp
from .v0042_openapi_diag_resp import V0042OpenapiDiagResp
from .v0042_openapi_error import V0042OpenapiError
from .v0042_openapi_instances_resp import V0042OpenapiInstancesResp
from .v0042_openapi_job_alloc_resp import V0042OpenapiJobAllocResp
from .v0042_openapi_job_info_resp import V0042OpenapiJobInfoResp
from .v0042_openapi_job_post_response import V0042OpenapiJobPostResponse
from .v0042_openapi_job_submit_response import V0042OpenapiJobSubmitResponse
from .v0042_openapi_kill_job_resp import V0042OpenapiKillJobResp
from .v0042_openapi_kill_jobs_resp import V0042OpenapiKillJobsResp
from .v0042_openapi_licenses_resp import V0042OpenapiLicensesResp
from .v0042_openapi_meta import V0042OpenapiMeta
from .v0042_openapi_meta_client import V0042OpenapiMetaClient
from .v0042_openapi_meta_plugin import V0042OpenapiMetaPlugin
from .v0042_openapi_meta_slurm import V0042OpenapiMetaSlurm
from .v0042_openapi_meta_slurm_version import V0042OpenapiMetaSlurmVersion
from .v0042_openapi_nodes_resp import V0042OpenapiNodesResp
from .v0042_openapi_partition_resp import V0042OpenapiPartitionResp
from .v0042_openapi_ping_array_resp import V0042OpenapiPingArrayResp
from .v0042_openapi_reservation_resp import V0042OpenapiReservationResp
from .v0042_openapi_resp import V0042OpenapiResp
from .v0042_openapi_shares_resp import V0042OpenapiSharesResp
from .v0042_openapi_slurmdbd_config_resp import V0042OpenapiSlurmdbdConfigResp
from .v0042_openapi_slurmdbd_jobs_resp import V0042OpenapiSlurmdbdJobsResp
from .v0042_openapi_slurmdbd_ping_resp import V0042OpenapiSlurmdbdPingResp
from .v0042_openapi_slurmdbd_qos_removed_resp import V0042OpenapiSlurmdbdQosRemovedResp
from .v0042_openapi_slurmdbd_qos_resp import V0042OpenapiSlurmdbdQosResp
from .v0042_openapi_slurmdbd_stats_resp import V0042OpenapiSlurmdbdStatsResp
from .v0042_openapi_tres_resp import V0042OpenapiTresResp
from .v0042_openapi_users_add_cond_resp import V0042OpenapiUsersAddCondResp
from .v0042_openapi_users_add_cond_resp_str import V0042OpenapiUsersAddCondRespStr
from .v0042_openapi_users_resp import V0042OpenapiUsersResp
from .v0042_openapi_warning import V0042OpenapiWarning
from .v0042_openapi_wckey_removed_resp import V0042OpenapiWckeyRemovedResp
from .v0042_openapi_wckey_resp import V0042OpenapiWckeyResp
from .v0042_oversubscribe_flags_item import V0042OversubscribeFlagsItem
from .v0042_part_prio import V0042PartPrio
from .v0042_partition_info import V0042PartitionInfo
from .v0042_partition_info_accounts import V0042PartitionInfoAccounts
from .v0042_partition_info_cpus import V0042PartitionInfoCpus
from .v0042_partition_info_defaults import V0042PartitionInfoDefaults
from .v0042_partition_info_groups import V0042PartitionInfoGroups
from .v0042_partition_info_maximums import V0042PartitionInfoMaximums
from .v0042_partition_info_maximums_oversubscribe import V0042PartitionInfoMaximumsOversubscribe
from .v0042_partition_info_minimums import V0042PartitionInfoMinimums
from .v0042_partition_info_nodes import V0042PartitionInfoNodes
from .v0042_partition_info_partition import V0042PartitionInfoPartition
from .v0042_partition_info_priority import V0042PartitionInfoPriority
from .v0042_partition_info_qos import V0042PartitionInfoQos
from .v0042_partition_info_timeouts import V0042PartitionInfoTimeouts
from .v0042_partition_info_tres import V0042PartitionInfoTres
from .v0042_partition_states_item import V0042PartitionStatesItem
from .v0042_process_exit_code_status_item import V0042ProcessExitCodeStatusItem
from .v0042_process_exit_code_verbose import V0042ProcessExitCodeVerbose
from .v0042_process_exit_code_verbose_signal import V0042ProcessExitCodeVerboseSignal
from .v0042_qos import V0042Qos
from .v0042_qos_flags_item import V0042QosFlagsItem
from .v0042_qos_limits import V0042QosLimits
from .v0042_qos_limits_max import V0042QosLimitsMax
from .v0042_qos_limits_max_accruing import V0042QosLimitsMaxAccruing
from .v0042_qos_limits_max_accruing_per import V0042QosLimitsMaxAccruingPer
from .v0042_qos_limits_max_active_jobs import V0042QosLimitsMaxActiveJobs
from .v0042_qos_limits_max_jobs import V0042QosLimitsMaxJobs
from .v0042_qos_limits_max_jobs_active_jobs import V0042QosLimitsMaxJobsActiveJobs
from .v0042_qos_limits_max_jobs_active_jobs_per import V0042QosLimitsMaxJobsActiveJobsPer
from .v0042_qos_limits_max_jobs_per import V0042QosLimitsMaxJobsPer
from .v0042_qos_limits_max_tres import V0042QosLimitsMaxTres
from .v0042_qos_limits_max_tres_minutes import V0042QosLimitsMaxTresMinutes
from .v0042_qos_limits_max_tres_minutes_per import V0042QosLimitsMaxTresMinutesPer
from .v0042_qos_limits_max_tres_per import V0042QosLimitsMaxTresPer
from .v0042_qos_limits_max_wall_clock import V0042QosLimitsMaxWallClock
from .v0042_qos_limits_max_wall_clock_per import V0042QosLimitsMaxWallClockPer
from .v0042_qos_limits_min import V0042QosLimitsMin
from .v0042_qos_limits_min_tres import V0042QosLimitsMinTres
from .v0042_qos_limits_min_tres_per import V0042QosLimitsMinTresPer
from .v0042_qos_preempt import V0042QosPreempt
from .v0042_qos_preempt_modes_item import V0042QosPreemptModesItem
from .v0042_reservation_core_spec import V0042ReservationCoreSpec
from .v0042_reservation_flags_item import V0042ReservationFlagsItem
from .v0042_reservation_info import V0042ReservationInfo
from .v0042_reservation_info_purge_completed import V0042ReservationInfoPurgeCompleted
from .v0042_rollup_stats import V0042RollupStats
from .v0042_rollup_stats_daily import V0042RollupStatsDaily
from .v0042_rollup_stats_daily_duration import V0042RollupStatsDailyDuration
from .v0042_rollup_stats_hourly import V0042RollupStatsHourly
from .v0042_rollup_stats_hourly_duration import V0042RollupStatsHourlyDuration
from .v0042_rollup_stats_monthly import V0042RollupStatsMonthly
from .v0042_rollup_stats_monthly_duration import V0042RollupStatsMonthlyDuration
from .v0042_schedule_exit_fields import V0042ScheduleExitFields
from .v0042_shares_float_128_tres import V0042SharesFloat128Tres
from .v0042_shares_resp_msg import V0042SharesRespMsg
from .v0042_shares_uint_64_tres import V0042SharesUint64Tres
from .v0042_slurmdb_job_flags_item import V0042SlurmdbJobFlagsItem
from .v0042_slurmdbd_ping import V0042SlurmdbdPing
from .v0042_stats_msg import V0042StatsMsg
from .v0042_stats_msg_rpc_dump import V0042StatsMsgRpcDump
from .v0042_stats_msg_rpc_queue import V0042StatsMsgRpcQueue
from .v0042_stats_msg_rpc_type import V0042StatsMsgRpcType
from .v0042_stats_msg_rpc_user import V0042StatsMsgRpcUser
from .v0042_stats_rec import V0042StatsRec
from .v0042_stats_rpc import V0042StatsRpc
from .v0042_stats_rpc_time import V0042StatsRpcTime
from .v0042_stats_user import V0042StatsUser
from .v0042_stats_user_time import V0042StatsUserTime
from .v0042_step import V0042Step
from .v0042_step_cpu import V0042StepCPU
from .v0042_step_cpu_requested_frequency import V0042StepCPURequestedFrequency
from .v0042_step_nodes import V0042StepNodes
from .v0042_step_statistics import V0042StepStatistics
from .v0042_step_statistics_cpu import V0042StepStatisticsCPU
from .v0042_step_statistics_energy import V0042StepStatisticsEnergy
from .v0042_step_step import V0042StepStep
from .v0042_step_task import V0042StepTask
from .v0042_step_tasks import V0042StepTasks
from .v0042_step_time import V0042StepTime
from .v0042_step_time_system import V0042StepTimeSystem
from .v0042_step_time_total import V0042StepTimeTotal
from .v0042_step_time_user import V0042StepTimeUser
from .v0042_step_tres import V0042StepTres
from .v0042_step_tres_consumed import V0042StepTresConsumed
from .v0042_step_tres_requested import V0042StepTresRequested
from .v0042_tres import V0042Tres
from .v0042_uint_16_no_val_struct import V0042Uint16NoValStruct
from .v0042_uint_32_no_val_struct import V0042Uint32NoValStruct
from .v0042_uint_64_no_val_struct import V0042Uint64NoValStruct
from .v0042_update_node_msg import V0042UpdateNodeMsg
from .v0042_user import V0042User
from .v0042_user_default import V0042UserDefault
from .v0042_user_flags_item import V0042UserFlagsItem
from .v0042_user_short import V0042UserShort
from .v0042_users_add_cond import V0042UsersAddCond
from .v0042_warn_flags_item import V0042WarnFlagsItem
from .v0042_wckey import V0042Wckey
from .v0042_wckey_flags_item import V0042WckeyFlagsItem
from .v0042_wckey_tag_flags_item import V0042WckeyTagFlagsItem
from .v0042_wckey_tag_struct import V0042WckeyTagStruct
from .v0042x11_flags_item import V0042X11FlagsItem

__all__ = (
    "SlurmdbV0042DeleteClusterClassification",
    "SlurmdbV0042DeleteClusterFlags",
    "SlurmdbV0042GetClusterClassification",
    "SlurmdbV0042GetClusterFlags",
    "SlurmdbV0042GetQosPreemptMode",
    "SlurmdbV0042GetUsersAdminLevel",
    "SlurmdbV0042PostQosPreemptMode",
    "SlurmdbV0042PostUsersAssociationFlags",
    "SlurmV0042DeleteJobFlags",
    "SlurmV0042GetJobFlags",
    "SlurmV0042GetJobsFlags",
    "SlurmV0042GetJobsStateFlags",
    "SlurmV0042GetNodeFlags",
    "SlurmV0042GetNodesFlags",
    "SlurmV0042GetPartitionFlags",
    "SlurmV0042GetPartitionsFlags",
    "V0042Account",
    "V0042AccountFlagsItem",
    "V0042Accounting",
    "V0042AccountingAllocated",
    "V0042AccountsAddCond",
    "V0042AccountShort",
    "V0042AcctGatherEnergy",
    "V0042AcctGatherProfileItem",
    "V0042AdminLvlItem",
    "V0042Assoc",
    "V0042AssocDefault",
    "V0042AssocFlagsItem",
    "V0042AssocMax",
    "V0042AssocMaxJobs",
    "V0042AssocMaxJobsPer",
    "V0042AssocMaxPer",
    "V0042AssocMaxPerAccount",
    "V0042AssocMaxTres",
    "V0042AssocMaxTresGroup",
    "V0042AssocMaxTresMinutes",
    "V0042AssocMaxTresMinutesPer",
    "V0042AssocMaxTresPer",
    "V0042AssocMin",
    "V0042AssocRecSet",
    "V0042AssocSharesObjWrap",
    "V0042AssocSharesObjWrapFairshare",
    "V0042AssocSharesObjWrapTres",
    "V0042AssocSharesObjWrapTypeItem",
    "V0042AssocShort",
    "V0042BfExitFields",
    "V0042ClusterRec",
    "V0042ClusterRecAssociations",
    "V0042ClusterRecController",
    "V0042ClusterRecFlagsItem",
    "V0042ControllerPing",
    "V0042Coord",
    "V0042CpuBindingFlagsItem",
    "V0042CronEntry",
    "V0042CronEntryFlagsItem",
    "V0042CronEntryLine",
    "V0042CrTypeItem",
    "V0042Float64NoValStruct",
    "V0042Instance",
    "V0042InstanceTime",
    "V0042Job",
    "V0042JobAllocReq",
    "V0042JobArray",
    "V0042JobArrayLimits",
    "V0042JobArrayLimitsMax",
    "V0042JobArrayLimitsMaxRunning",
    "V0042JobArrayResponseMsgEntry",
    "V0042JobComment",
    "V0042JobDescMsg",
    "V0042JobDescMsgRlimits",
    "V0042JobFlagsItem",
    "V0042JobHet",
    "V0042JobInfo",
    "V0042JobInfoPower",
    "V0042JobMailFlagsItem",
    "V0042JobMcs",
    "V0042JobRequired",
    "V0042JobRes",
    "V0042JobResCore",
    "V0042JobResCoreStatusItem",
    "V0042JobReservation",
    "V0042JobResNode",
    "V0042JobResNodeCpus",
    "V0042JobResNodeMemory",
    "V0042JobResNodes",
    "V0042JobResSocket",
    "V0042JobSharedItem",
    "V0042JobState",
    "V0042JobStateItem",
    "V0042JobSubmitReq",
    "V0042JobTime",
    "V0042JobTimeSystem",
    "V0042JobTimeTotal",
    "V0042JobTimeUser",
    "V0042JobTres",
    "V0042KillJobsMsg",
    "V0042KillJobsRespJob",
    "V0042KillJobsRespJobError",
    "V0042KillJobsRespJobFederation",
    "V0042License",
    "V0042MemoryBindingTypeItem",
    "V0042Node",
    "V0042NodeCrTypeItem",
    "V0042NodeExternalSensors",
    "V0042NodePower",
    "V0042NodeStatesItem",
    "V0042OpenapiAccountsAddCondResp",
    "V0042OpenapiAccountsAddCondRespStr",
    "V0042OpenapiAccountsRemovedResp",
    "V0042OpenapiAccountsResp",
    "V0042OpenapiAssocsRemovedResp",
    "V0042OpenapiAssocsResp",
    "V0042OpenapiClustersRemovedResp",
    "V0042OpenapiClustersResp",
    "V0042OpenapiDiagResp",
    "V0042OpenapiError",
    "V0042OpenapiInstancesResp",
    "V0042OpenapiJobAllocResp",
    "V0042OpenapiJobInfoResp",
    "V0042OpenapiJobPostResponse",
    "V0042OpenapiJobSubmitResponse",
    "V0042OpenapiKillJobResp",
    "V0042OpenapiKillJobsResp",
    "V0042OpenapiLicensesResp",
    "V0042OpenapiMeta",
    "V0042OpenapiMetaClient",
    "V0042OpenapiMetaPlugin",
    "V0042OpenapiMetaSlurm",
    "V0042OpenapiMetaSlurmVersion",
    "V0042OpenapiNodesResp",
    "V0042OpenapiPartitionResp",
    "V0042OpenapiPingArrayResp",
    "V0042OpenapiReservationResp",
    "V0042OpenapiResp",
    "V0042OpenapiSharesResp",
    "V0042OpenapiSlurmdbdConfigResp",
    "V0042OpenapiSlurmdbdJobsResp",
    "V0042OpenapiSlurmdbdPingResp",
    "V0042OpenapiSlurmdbdQosRemovedResp",
    "V0042OpenapiSlurmdbdQosResp",
    "V0042OpenapiSlurmdbdStatsResp",
    "V0042OpenapiTresResp",
    "V0042OpenapiUsersAddCondResp",
    "V0042OpenapiUsersAddCondRespStr",
    "V0042OpenapiUsersResp",
    "V0042OpenapiWarning",
    "V0042OpenapiWckeyRemovedResp",
    "V0042OpenapiWckeyResp",
    "V0042OpenModeItem",
    "V0042OversubscribeFlagsItem",
    "V0042PartitionInfo",
    "V0042PartitionInfoAccounts",
    "V0042PartitionInfoCpus",
    "V0042PartitionInfoDefaults",
    "V0042PartitionInfoGroups",
    "V0042PartitionInfoMaximums",
    "V0042PartitionInfoMaximumsOversubscribe",
    "V0042PartitionInfoMinimums",
    "V0042PartitionInfoNodes",
    "V0042PartitionInfoPartition",
    "V0042PartitionInfoPriority",
    "V0042PartitionInfoQos",
    "V0042PartitionInfoTimeouts",
    "V0042PartitionInfoTres",
    "V0042PartitionStatesItem",
    "V0042PartPrio",
    "V0042ProcessExitCodeStatusItem",
    "V0042ProcessExitCodeVerbose",
    "V0042ProcessExitCodeVerboseSignal",
    "V0042Qos",
    "V0042QosFlagsItem",
    "V0042QosLimits",
    "V0042QosLimitsMax",
    "V0042QosLimitsMaxAccruing",
    "V0042QosLimitsMaxAccruingPer",
    "V0042QosLimitsMaxActiveJobs",
    "V0042QosLimitsMaxJobs",
    "V0042QosLimitsMaxJobsActiveJobs",
    "V0042QosLimitsMaxJobsActiveJobsPer",
    "V0042QosLimitsMaxJobsPer",
    "V0042QosLimitsMaxTres",
    "V0042QosLimitsMaxTresMinutes",
    "V0042QosLimitsMaxTresMinutesPer",
    "V0042QosLimitsMaxTresPer",
    "V0042QosLimitsMaxWallClock",
    "V0042QosLimitsMaxWallClockPer",
    "V0042QosLimitsMin",
    "V0042QosLimitsMinTres",
    "V0042QosLimitsMinTresPer",
    "V0042QosPreempt",
    "V0042QosPreemptModesItem",
    "V0042ReservationCoreSpec",
    "V0042ReservationFlagsItem",
    "V0042ReservationInfo",
    "V0042ReservationInfoPurgeCompleted",
    "V0042RollupStats",
    "V0042RollupStatsDaily",
    "V0042RollupStatsDailyDuration",
    "V0042RollupStatsHourly",
    "V0042RollupStatsHourlyDuration",
    "V0042RollupStatsMonthly",
    "V0042RollupStatsMonthlyDuration",
    "V0042ScheduleExitFields",
    "V0042SharesFloat128Tres",
    "V0042SharesRespMsg",
    "V0042SharesUint64Tres",
    "V0042SlurmdbdPing",
    "V0042SlurmdbJobFlagsItem",
    "V0042StatsMsg",
    "V0042StatsMsgRpcDump",
    "V0042StatsMsgRpcQueue",
    "V0042StatsMsgRpcType",
    "V0042StatsMsgRpcUser",
    "V0042StatsRec",
    "V0042StatsRpc",
    "V0042StatsRpcTime",
    "V0042StatsUser",
    "V0042StatsUserTime",
    "V0042Step",
    "V0042StepCPU",
    "V0042StepCPURequestedFrequency",
    "V0042StepNodes",
    "V0042StepStatistics",
    "V0042StepStatisticsCPU",
    "V0042StepStatisticsEnergy",
    "V0042StepStep",
    "V0042StepTask",
    "V0042StepTasks",
    "V0042StepTime",
    "V0042StepTimeSystem",
    "V0042StepTimeTotal",
    "V0042StepTimeUser",
    "V0042StepTres",
    "V0042StepTresConsumed",
    "V0042StepTresRequested",
    "V0042Tres",
    "V0042Uint16NoValStruct",
    "V0042Uint32NoValStruct",
    "V0042Uint64NoValStruct",
    "V0042UpdateNodeMsg",
    "V0042User",
    "V0042UserDefault",
    "V0042UserFlagsItem",
    "V0042UsersAddCond",
    "V0042UserShort",
    "V0042WarnFlagsItem",
    "V0042Wckey",
    "V0042WckeyFlagsItem",
    "V0042WckeyTagFlagsItem",
    "V0042WckeyTagStruct",
    "V0042X11FlagsItem",
)
