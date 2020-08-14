# -*- coding: utf-8 -*-

import pytest
from chocolatepy.auth import Auth
from pydal import DAL


@pytest.fixture
def db():
    return DAL("sqlite:memory")


def test_auth_tables(db):
    auth = Auth(db)

    for each in ["auth_user", "auth_group", "auth_permission", "auth_membership"]:
        assert each in auth.db.tables
