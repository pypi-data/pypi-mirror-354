from django.db import models


class Checkpoint(models.Model):
    composite_id = models.TextField(unique=True)
    thread_id = models.TextField()
    checkpoint_ns = models.TextField(default="")
    checkpoint_id = models.TextField()
    parent_checkpoint_id = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    checkpoint = models.BinaryField()
    metadata = models.JSONField(default=dict)

    class Meta:
        db_table = "checkpoint"
        constraints = [
            models.UniqueConstraint(
                fields=["thread_id", "checkpoint_ns", "checkpoint_id"],
                name="unique_checkpoint",
            )
        ]


class Write(models.Model):
    checkpoint = models.ForeignKey('Checkpoint', on_delete=models.CASCADE, db_constraint=False, to_field='composite_id', related_name='writes')
    task_id = models.TextField()
    task_path = models.TextField()
    idx = models.IntegerField()
    channel = models.TextField()
    type = models.TextField(null=True, blank=True)
    value = models.BinaryField()

    class Meta:
        db_table = "write"
        constraints = [
            models.UniqueConstraint(
                fields=["checkpoint", "task_id", "idx"],
                name="unique_write",
            )
        ]