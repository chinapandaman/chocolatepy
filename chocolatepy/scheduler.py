# -*- coding: utf-8 -*-

from pydal import Field


class Scheduler(object):
    def __init__(self, db):
        self.db = db

        self.db.define_table(
            "scheduler_task",
            Field("application_name", length=512),
            Field("task_name", length=512),
            Field("group_name", length=512),
            Field("status", length=512),
            Field("function_name", length=512),
            Field("uuid", length=256, unique=True),
            Field("args", type="text"),
            Field("vars", type="text"),
            Field("enabled", type="boolean", default=True),
            Field("start_time", type="datetime"),
            Field("next_run_time", type="datetime"),
            Field("stop_time", type="datetime"),
            Field("repeats", type="integer"),
            Field("retry_failed", type="integer"),
            Field("period", type="integer"),
            Field("prevent_drift", type="boolean"),
            Field("timeout", type="integer"),
            Field("sync_output", type="integer"),
            Field("times_run", type="integer"),
            Field("times_failed", type="integer"),
            Field("last_run_time", type="datetime"),
            Field("assigned_workder_name", length=512),
        )

        self.db.define_table(
            "scheduler_run",
            Field("task_id", "reference scheduler_task"),
            Field("status", length=512),
            Field("start_time", type="datetime"),
            Field("stop_time", type="datetime"),
            Field("run_output", type="text"),
            Field("run_result", type="text"),
            Field("traceback", type="text"),
            Field("worker_name", length=512),
        )

        self.db.define_table(
            "scheduler_worker",
            Field("worker_name", length=256, unique=True),
            Field("first_heartbeat", type="datetime"),
            Field("last_heartbeat", type="datetime"),
            Field("status", length=512),
            Field("is_ticker", type="boolean"),
            Field("group_names", type="json"),
            Field("worker_stats", type="json"),
        )
