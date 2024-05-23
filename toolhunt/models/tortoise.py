from tortoise import fields, models


class Tool(models.Model):
    name = fields.CharField(max_length=255, pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    url = fields.CharField(max_length=2047)
    last_updated = fields.DatetimeField()

    # tasks: fields.ReverseRelation["Task"]

    class Meta:
        table = "tool"
        charset = "binary"
