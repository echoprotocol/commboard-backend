from marshmallow import Schema, fields, validate


# Rates schema's and responses
class RatesSchema(Schema):
    BTC = fields.String(allow_none=True)
    ETH = fields.String(allow_none=True)


class GetRatesResponse(Schema):
    message = fields.Nested(RatesSchema)


# Node schema's and responses
class GetUptimeResponse(Schema):
    message = fields.String(allow_none=True)


class GetEchoLogsRequest(Schema):
    logs_dir = fields.String(
        validate=validate.OneOf(
            ['api', 'echorand', 'p2p', 'sidechain', 'term'],
            ['api', 'echorand', 'p2p', 'sidechain', 'term']
        ),
        required=True
    )
    hours = fields.Int(required=False)
    quantity = fields.Int(required=False)


class GetEchoLogsResponse(Schema):
    message = fields.List(fields.String(), allow_none=True)


class GetMessageLogsRequest(Schema):
    hours = fields.Int(required=False)
    quantity = fields.Int(required=False)


class GetMessageLogsResponse(Schema):
    message = fields.Dict(fields.String(), fields.String(), allow_none=True)


# PC schema's and responses

class GetCpuHistoryRequest(Schema):
    hours = fields.Int(required=True)


class GetCpuHistoryResponse(Schema):
    message = fields.Dict(fields.String(), fields.Int(), allow_none=True)


class GetRamHistoryRequest(Schema):
    hours = fields.Int(required=True)


class GetRamHistoryResponse(Schema):
    message = fields.Dict(fields.String(), fields.Int(), allow_none=True)


class GetFreeSpaceResponse(Schema):
    message = fields.String(allow_none=True)


class GetExternalIpResponse(Schema):
    message = fields.String(allow_none=True)


# Error and General schema's and responses

class ErrorStringResponse(Schema):
    error = fields.String(required=False)


class GetNullResponse(Schema):
    pass
