from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class AbstractSoftDeleteQuerySet(models.QuerySet):
    """
    QuerySet class for implementing soft delete functionality.
    """

    def delete(self):
        """
        Override the delete method to perform a soft delete by setting is_deleted to True and updating deleted_at.

        Returns:
        -------
        int
            The number of rows updated.
        """
        return self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def active(self):
        """
        Return only active (non-deleted) records.
        """
        return self.filter(is_deleted=False)


class AbstractSoftDeleteManager(models.Manager):
    """
    Manager class for AbstractSoftDeleteModel, which ensures that only non-deleted objects are queried by default.
    """

    def get_queryset(self):
        """
        Override default queryset to exclude soft-deleted records.
        """
        return AbstractSoftDeleteQuerySet(self.model, self._db).active()

    def all_objects(self):
        # This returns all objects, including deleted ones
        return AbstractSoftDeleteQuerySet(self.model, using=self._db)

    def restore(self, *args, **kwargs):
        """
        Restore soft-deleted records.
        """
        self.model.objects.filter(pk__in=kwargs["ids"]).update(
            is_deleted=False, deleted_at=None
        )


class AbstractSoftDeleteModel(models.Model):
    """
    Abstract base model that adds soft delete functionality.
    """

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(
        default=False, editable=False, verbose_name=_("Is Deleted")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Deleted Time")
    )

    objects = AbstractSoftDeleteManager()

    def formatted_deleted_at(self):
        """
        Returns the deleted_at timestamp formatted according to DATE_INPUT_FORMAT and TIME_INPUT_FORMAT settings, or None if not set.

        Returns:
        -------
        str or None
            The formatted deleted_at timestamp or None.
        """
        if not self.deleted_at:
            return None
        return self.deleted_at.strftime(
            f"{settings.DATE_INPUT_FORMAT} {settings.TIME_INPUT_FORMAT}"
        )

    def delete_related_objects(self):
        """
        Find and delete related objects that are set to cascade on delete.
        """
        for related_object in self._meta.related_objects:
            # Check for CASCADE related fields
            if related_object.on_delete == models.CASCADE:
                related_name = related_object.get_accessor_name()
                related_manager = getattr(self, related_name)
                # Delete all related objects (cascading delete)
                try:
                    related_manager.all().delete()
                except AttributeError:
                    related_manager.delete()

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        """
        Override the delete method to perform a soft delete by setting is_deleted to True and updating deleted_at.
        This method is atomic to ensure data integrity.

        Parameters:
        ----------
        using : str, optional
            The database alias to use.
        keep_parents : bool, optional
            Whether to keep parent model relationships. Defaults to False.
        """
        self.delete_related_objects()  # Delete all CASCADE-related objects
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    @transaction.atomic
    def restore(self):
        """
        Restore the soft-deleted record.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()
