from tortoise import fields, models


class Tool(models.Model):
    name = fields.CharField(max_length=255, pk=True, unique=True)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=False)
    url = fields.CharField(max_length=2047, null=False)
    last_updated = fields.DatetimeField(auto_now=True)

    tasks: fields.ReverseRelation["Task"]
    completed_tasks: fields.ReverseRelation["CompletedTask"]

    class Meta:
        table = "tool"
        charset = "binary"


class Field(models.Model):
    name = fields.CharField(max_length=80, pk=True, unique=True)
    description = fields.CharField(max_length=2047, null=False)
    input_options = fields.CharField(max_length=2047, null=True)
    pattern = fields.CharField(max_length=320, null=True)

    tasks: fields.ReverseRelation["Task"]
    completed_tasks: fields.ReverseRelation["CompletedTask"]

    class Meta:
        table = "field"
        charset = "binary"


class Task(models.Model):
    id = fields.IntField(pk=True, generated=True)
    tool_name = fields.ForeignKeyField(
        "models.Tool", related_name="tasks", on_delete=fields.CASCADE
    )
    field_name = fields.ForeignKeyField("models.Field", related_name="tasks")
    last_attempted = fields.DatetimeField(null=True)
    last_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "task"
        unique_together = ("tool_name", "field_name")
        charset = "binary"


class CompletedTask(models.Model):
    id = fields.IntField(pk=True, generated=True)  # Ensure id is auto-incremented
    tool = fields.ForeignKeyField(
        "models.Tool",
        related_name="completed_tasks",
        on_delete=fields.SET_NULL,
        null=True,
    )
    tool_title = fields.CharField(max_length=255, null=False)
    field = fields.ForeignKeyField(
        "models.Field",
        related_name="completed_tasks",
        on_delete=fields.SET_NULL,
        null=True,
    )
    user = fields.CharField(max_length=255, null=False)
    completed_date = fields.DatetimeField(null=False)

    class Meta:
        table = "completed_task"
        charset = "binary"
