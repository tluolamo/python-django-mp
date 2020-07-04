from django.db import models


class Member(models.Model):
    """
    Member model
    Use bigint for IDs to ensure we have plenty of growth room
    Use bigint for phone numbers to support longest possible phone number at 15 digits, shortest possible number is 4 digits long.
    """
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=126)
    last_name = models.CharField(max_length=126)
    phone_number = models.BigIntegerField()
    client_member_id = models.BigIntegerField()
    account_id = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
