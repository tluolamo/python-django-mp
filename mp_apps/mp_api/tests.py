import json
import os
import pathlib
import shutil

from celery.contrib.testing.worker import start_worker
from django.db import IntegrityError
from django.test import Client, TestCase

from ..celery import app
from .models import Member
from .tasks import load_data

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
BASE_DIR = pathlib.Path(CURRENT_DIR).parent.absolute().parent.absolute()

john_doe_data = {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": 8185550001,
    "client_member_id": 1,
    "account_id": 1,
}

jane_doe_data = {
    "first_name": "Jane",
    "last_name": "Doe",
    "phone_number": 8185550002,
    "client_member_id": 2,
    "account_id": 2,
}

jim_doe_data = {
    "first_name": "Jim",
    "last_name": "Doe",
    "phone_number": 8185550004,
    "client_member_id": 4,
    "account_id": 4,
}

test_client = Client()


class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.create(**john_doe_data)

    def test_new_member_can_be_created(self):
        jane_doe = Member.objects.create(**jane_doe_data)

        # id should match the object when converted to string
        self.assertEqual(str(getattr(jane_doe, "id")), str(jane_doe))
        for k, v in jane_doe_data.items():
            self.assertEqual(v, getattr(jane_doe, k))

    def test_duplicates_can_not_be_created(self):
        with self.assertRaises(IntegrityError):
            # the same record
            Member.objects.create(**john_doe_data)

            # account_id and phone_number only match
            ac_ph = john_doe_data.copy()
            ac_ph.first_name = "Jack"
            ac_ph.last_name = "Brown"
            ac_ph.client_member_id = 3

            Member.objects.create(**ac_ph)

            # client_member_id and phone_number only match
            cm_ph = john_doe_data.copy()
            cm_ph.first_name = "Jack"
            cm_ph.last_name = "Brown"
            cm_ph.account_id = 3

            Member.objects.create(**cm_ph)

    def test_member_can_be_get(self):
        """get with all the key fields we may need to get"""
        for f in ["id", "phone_number", "account_id", "client_member_id"]:
            find_with = find_with = {f: john_doe_data.get(f, 1)}

            john_doe = Member.objects.get(**find_with)

            self.assertEqual(getattr(john_doe, "id"), 1)
            for k, v in john_doe_data.items():
                # pprint(getattr(jane_doe, k))
                self.assertEqual(v, getattr(john_doe, k))

    def test_member_view_list(self):
        response = test_client.get("/members/")
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertEqual([*content], ["count", "next", "previous", "results"])

        for k, v in john_doe_data.items():
            self.assertEqual(v, content["results"][0][k])

    # def test_member_view_get(self):
    #     response = test_client.get("/members/1/")
    #     self.assertEqual(200, response.status_code)
    #     content = json.loads(response.content)
    #
    #     self.assertEqual(content["id"], 1)
    #     for k, v in john_doe_data.items():
    #         self.assertEqual(v, content[k])
    #
    # def test_member_view_post(self):
    #     response = test_client.post(
    #         "/members/", jim_doe_data, content_type="application/json",
    #     )
    #     self.assertEqual(201, response.status_code)
    #     content = json.loads(response.content)
    #     for k, v in jim_doe_data.items():
    #         self.assertEqual(v, content[k])


class FileTestCase(TestCase):
    def test_file_upload(self):
        with open(os.path.join(CURRENT_DIR, "test_data/members.csv"), "rb") as fp:
            response = test_client.put(
                "/upload/upload.csv",
                fp.read(),
                format="multipart",
                content_type="text/csv",
            )
            self.assertEqual(201, response.status_code)


class TaskTestCase(TestCase):
    def test_load_data_task(self):
        expected_item_count = len(Member.objects.all()) + 2
        filename = os.path.join(BASE_DIR, "upload/test.csv")
        source_file = os.path.join(CURRENT_DIR, "test_data/members.csv")
        shutil.copyfile(
            source_file, filename,
        )
        load_data(filename)
        self.assertFalse(os.path.exists(self.filename))
        self.assertEqual(expected_item_count, len(Member.objects.all()))
