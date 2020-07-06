from django.db import models

from .utils import random_file_name


class Member(models.Model):
    """
    Member model
    Use bigint for IDs to ensure we have plenty of growth room
    Use bigint for phone numbers to support longest possible phone number at 15
    digits, shortest possible number is 4 digits long.
    """

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=126)
    last_name = models.CharField(max_length=126)
    phone_number = models.BigIntegerField()
    client_member_id = models.BigIntegerField()
    account_id = models.BigIntegerField()

    def __str__(self):
        return str(self.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique-phone_number-account_id",
                fields=["phone_number", "account_id"],
            ),
            models.UniqueConstraint(
                name="unique-client_member_id-account_id",
                fields=["client_member_id", "account_id"],
            ),
        ]
        indexes = [
            models.Index(fields=["account_id"]),
        ]
        ordering = ["id"]


class File(models.Model):
    file = models.FileField(upload_to=random_file_name)

    def __str__(self):
        return self.file
