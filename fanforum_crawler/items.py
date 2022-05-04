
from scrapy import Field, Item


class CommentItem(Item):
    author = Field() # Convert this field to author object
    created_at = Field()
    votes = Field()
    quote = Field() # Convert this field to quote object
    contents = Field()