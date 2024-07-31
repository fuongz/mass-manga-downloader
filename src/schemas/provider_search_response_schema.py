from marshmallow import Schema, fields


class ProviderSearchResponseSchema(Schema):
    title = fields.Str(required=True)
    html_url = fields.Str(required=True)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
