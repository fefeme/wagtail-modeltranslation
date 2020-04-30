import re
from typing import Any

from django.conf import settings
from django.utils.translation import activate as trans_activate
from django.utils.translation import deactivate as trans_deactivate

try:
    from wagtail.search.index import SearchField
except ImportError:
    # noinspection PyUnresolvedReferences
    from wagtail.wagtailsearch.index import SearchField

RE_LANGUAGES = '|'.join(t[0].replace('-', '_') for t in settings.LANGUAGES)
RE_LANGUAGE_MATCHER = re.compile(rf'_({RE_LANGUAGES})$')

ELASTIC_LANGUAGE_ANALYZERS = {
    'en': 'english',
    'fr': 'french',
    'de': 'german',
    'es': 'spanish',
    'it': 'italian',
    'ru': 'russian',
    'pt': 'portuguese',
}


# noinspection PyMissingConstructor
class TranslatableSearchFieldWrapper(SearchField):
    """Wrapper class to enhance SearchFields get_value method
       to return the fallback value using django modeltranslations
       fallback logic.
     """

    def __init__(self, search_field_instance, language):
        self._search_field_instance = search_field_instance
        self.language = language

    def get_value(self, obj):
        trans_activate(self.language)
        value = self._search_field_instance.get_value(obj)
        trans_deactivate()
        return value

    def get_field(self, cls):
        return cls._meta.get_field(self.field_name)

    def __getattr__(self, item):
        return getattr(self._search_field_instance, item)
