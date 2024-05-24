from tortoise import fields, models


class Tool(models.Model):
    name = fields.CharField(max_length=255, pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    url = fields.CharField(max_length=2047)
    last_updated = fields.DatetimeField()

    tasks: fields.ReverseRelation["Task"]

    class Meta:
        table = "tool"
        charset = "binary"


class Field(models.Model):
    name = fields.CharField(max_length=80, pk=True)
    description = fields.CharField(max_length=2047)
    input_options = fields.CharField(max_length=2047, null=True)
    pattern = fields.CharField(max_length=320, null=True)

    tasks: fields.ReverseRelation["Task"]

    class Meta:
        table = "field"
        charset = "binary"


class Task(models.Model):
    id = fields.IntField(pk=True)
    tool_name = fields.ForeignKeyField("models.Tool", related_name="tasks", on_delete=fields.CASCADE)
    field_name = fields.ForeignKeyField("models.Field", related_name="tasks")
    last_attempted = fields.DatetimeField(null=True)
    last_updated = fields.DatetimeField()

    class Meta:
        table = "task"
        charset = "binary"


class CompletedTask(models.Model):
    id = fields.IntField(pk=True)
    tool_name = fields.CharField(max_length=255)
    tool_title = fields.CharField(max_length=255)
    field = fields.CharField(max_length=80)
    user = fields.CharField(max_length=255)
    completed_date = fields.DatetimeField()

    class Meta:
        table = "completed_task"
        charset = "binary"
