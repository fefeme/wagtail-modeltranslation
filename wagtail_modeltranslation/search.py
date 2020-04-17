import re

from django.conf import settings
from django.utils.translation import activate as translation_activate

try:
    from wagtail.search.index import SearchField
except ImportError:
    # noinspection PyUnresolvedReferences
    from wagtail.wagtailsearch.index import SearchField

RE_LANGUAGES = '|'.join(t[0].replace('-', '_') for t in settings.LANGUAGES)
RE_LANGUAGE_MATCHER = re.compile(rf'_({RE_LANGUAGES})$')


class TranslatableSearchFieldWrapper:
    """Wrapper class to enhance SearchFields get_value method
       to return the fallback value using django modeltranslations
       fallback logic.
     """

    def __init__(self, search_field_instance):
        self._search_field_instance = search_field_instance

    def get_value(self, obj):
        m = RE_LANGUAGE_MATCHER.search(self.field_name)
        translation_activate(m.group(1))
        return self._search_field_instance.get_value(obj)

    def __getattr__(self, item):
        return getattr(self._search_field_instance, item)

    @classmethod
    # We need to lie about who we are- this is for the
    # ElasticSearch2Mapping (get_field_column_name)
    def __instancecheck__(cls, instance):
        return isinstance(instance, SearchField)
