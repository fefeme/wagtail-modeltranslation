from django.utils.translation import activate as trans_activate
from django.utils.translation import deactivate as trans_deactivate

try:
    from wagtail.search.index import SearchField
except ImportError:
    # noinspection PyUnresolvedReferences
    from wagtail.wagtailsearch.index import SearchField


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
