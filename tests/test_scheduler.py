# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp
from chocolatepy.scheduler import Scheduler


@pytest.fixture
def scheduler():
    app = ChocolateApp("app")
    return Scheduler(app.db)


def test_scheduler_init(scheduler):
    db = scheduler.db

    assert db.scheduler_task.application_name.length == 512
    assert db.scheduler_task.task_name.length == 512
    assert db.scheduler_task.group_name.length == 512
    assert db.scheduler_task.group_name.default == "main"
    assert db.scheduler_task.status.length == 512
    assert db.scheduler_task.status.default == "QUEUED"
    assert db.scheduler_task.broadcast.type == "boolean"
    assert not db.scheduler_task.broadcast.default
    assert db.scheduler_task.function_name.length == 512
    assert db.scheduler_task.uuid.length == 256
    assert db.scheduler_task.uuid.unique
    assert db.scheduler_task.args.type == "json"
    assert db.scheduler_task.vars.type == "json"
    assert db.scheduler_task.enabled.type == "boolean"
    assert db.scheduler_task.enabled.default
    assert db.scheduler_task.start_time.type == "datetime"
    assert db.scheduler_task.next_run_time.type == "datetime"
    assert db.scheduler_task.stop_time.type == "datetime"
    assert db.scheduler_task.repeats.type == "integer"
    assert db.scheduler_task.repeats.default == 1
    assert db.scheduler_task.retry_failed.type == "integer"
    assert db.scheduler_task.retry_failed.default == 0
    assert db.scheduler_task.period.type == "integer"
    assert db.scheduler_task.period.default == 60
    assert db.scheduler_task.prevent_drift.type == "boolean"
    assert not db.scheduler_task.prevent_drift.default
    assert db.scheduler_task.timeout.type == "integer"
    assert db.scheduler_task.timeout.default == 60
    assert db.scheduler_task.sync_output.type == "integer"
    assert db.scheduler_task.sync_output.default == 0
    assert db.scheduler_task.times_run.type == "integer"
    assert db.scheduler_task.times_run.default == 0
    assert db.scheduler_task.times_failed.type == "integer"
    assert db.scheduler_task.times_failed.default == 0
    assert db.scheduler_task.last_run_time.type == "datetime"
    assert db.scheduler_task.assigned_worker_name.length == 512

    assert db.scheduler_run.task_id.type == "reference scheduler_task"
    assert db.scheduler_run.status.length == 512
    assert db.scheduler_run.start_time.type == "datetime"
    assert db.scheduler_run.stop_time.type == "datetime"
    assert db.scheduler_run.run_output.type == "text"
    assert db.scheduler_run.run_result.type == "text"
    assert db.scheduler_run.traceback.type == "text"
    assert db.scheduler_run.worker_name.length == 512

    assert db.scheduler_worker.worker_name.length == 256
    assert db.scheduler_worker.worker_name.unique
    assert db.scheduler_worker.first_heartbeat.type == "datetime"
    assert db.scheduler_worker.last_heartbeat.type == "datetime"
    assert db.scheduler_worker.status.length == 512
    assert db.scheduler_worker.is_ticker.type == "boolean"
    assert not db.scheduler_worker.is_ticker.default
    assert db.scheduler_worker.group_names.type == "json"
    assert db.scheduler_worker.worker_stats.type == "json"
