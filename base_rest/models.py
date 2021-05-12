"""
Author: Sanidhya Mangal, Ravinder Singh
github:sanidhyamangal
email: sanidhya.mangal@engineerbabu
"""
import datetime
import uuid

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """A base model to deal with all the asbtracrt level model creations"""
    class Meta:
        abstract = True

    # uuid field
    uid = models.UUIDField(default=uuid.uuid4,
                           primary_key=True,
                           editable=False)

    # date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_seconds_since_creation(self):
        """
        Find how much time has been elapsed since creation, in seconds.
        This function is timezone agnostic, meaning this will work even if
        you have specified a timezone.
        """
        return (datetime.datetime.utcnow() -
                self.created_at.replace(tzinfo=None)).seconds
