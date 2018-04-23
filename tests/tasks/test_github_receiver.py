# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

import json
from app import db
from mock import patch
from app.tasks import GitHubReceiver
from tests.utils import create_board, create_repo, create_list, \
    create_subscription, create_subscribed_list
from tests.base_test_case import BaseTestCase


class PatchClass:
    """A class used to patch methods in the `GitHubReceiver`."""

    def user_not_in_org(self):
        return False

    def user_in_org(self):
        return True


class GitHubReceiverTestCase(BaseTestCase):
    """Tests the `GitHubReceiver` celery task."""

    def setUp(self):
        """Sets up testing context."""
        super().setUp()
        create_board()
        create_repo()
        create_list()
        db.session.commit()

    @patch(
        'app.tasks.GitHubReceiver._user_in_organization',
        new=PatchClass.user_not_in_org
    )
    def test_issue_opened_for_autocard_subscription(self):
        create_subscription()
        create_subscribed_list()

        payload = json.loads(open('./tests/fixtures/issue_opened.json').read())
        GitHubReceiver.delay(payload=payload)
