# -*- coding: utf-8 -*-

import pytest
from chocolatepy import ChocolateApp
from chocolatepy.scheduler import Scheduler


@pytest.fixture
def scheduler():
    app = ChocolateApp("app")
    return Scheduler(app.db)


def test_scheduler_init(scheduler):
    assert False
