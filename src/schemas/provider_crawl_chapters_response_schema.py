from marshmallow import Schema, fields


class ProviderCrawlChapterSchema(Schema):
    title = fields.Str(required=True)
    html_url = fields.Str(required=True)


class ProviderCrawlChaptersResponseSchema(Schema):
    data = fields.List(fields.Nested(ProviderCrawlChapterSchema))
