from marshmallow import Schema, fields


class PC_cpu(Schema):
    hours = fields.Int()

class PC_ram(Schema):
    hours = fields.Int()

class GetEchoLogs(Schema):
    logs_dir = fields.String()
    from_date = fields.DateTime()
    quantity = fields.Int()
