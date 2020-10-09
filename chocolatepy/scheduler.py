# -*- coding: utf-8 -*-

from pydal import Field


class Scheduler(object):
    def __init__(self, db):
        self.db = db

        self.db.define_table(
            "scheduler_task",
            Field("application_name", length=512),
            Field("task_name", length=512),
            Field("group_name", length=512, default="main"),
            Field("status", length=512, default="QUEUED"),
            Field("broadcast", type="boolean", default=False),
            Field("function_name", length=512),
            Field("uuid", length=256, unique=True),
            Field("args", type="json"),
            Field("vars", type="json"),
            Field("enabled", type="boolean", default=True),
            Field("start_time", type="datetime"),
            Field("next_run_time", type="datetime"),
            Field("stop_time", type="datetime"),
            Field("repeats", type="integer", default=1),
            Field("retry_failed", type="integer", default=0),
            Field("period", type="integer", default=60),
            Field("prevent_drift", type="boolean", default=False),
            Field("timeout", type="integer", default=60),
            Field("sync_output", type="integer", default=0),
            Field("times_run", type="integer", default=0),
            Field("times_failed", type="integer", default=0),
            Field("last_run_time", type="datetime"),
            Field("assigned_worker_name", length=512),
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
            Field("is_ticker", type="boolean", default=False),
            Field("group_names", type="json"),
            Field("worker_stats", type="json"),
        )
