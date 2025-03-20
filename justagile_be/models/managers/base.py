from django.db import models


class BaseModelQueryset(models.QuerySet):
    def delete(self, is_soft: bool = True):
        """
        Performs hard/soft delete on the instance record based on the soft attribute
        """
        if is_soft:
            return super().update(is_deleted=True)

        return super().delete()

    def restore(self):
        """
        Restores a soft deleted record in the model
        """
        return super().update(is_deleted=False)

    def get_by_id(self, pk):
        """
        Retrieves the record by it's primary key and if it is not soft deleted

        Attributes:
        - pk : (str | int)
            - The primary key of the record
        """
        try:
            return self.get(pk=pk, is_deleted=False)
        except self.model.DoesNotExist:
            return None


class BaseModelManager(models.Manager):
    """
    A Model manager that implements all the basic methods that can be done on BaseModel
    """

    def get_by_id(self, pk):
        return self.get_queryset().get_by_id(pk)

    def get_queryset(self) -> models.QuerySet:
        """
        Retrieve a queryset of all the non-deleted records
        """
        return BaseModelQueryset(self.model).filter(is_deleted=False)
