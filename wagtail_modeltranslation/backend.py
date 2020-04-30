from modeltranslation.utils import get_language
from wagtail.search.backends.elasticsearch5 import Elasticsearch5AutocompleteQueryCompiler, \
    Elasticsearch5SearchResults, Elasticsearch5SearchQueryCompiler, Elasticsearch5SearchBackend


class Elasticsearch5SearchQueryCompilerLanguageAware(Elasticsearch5SearchQueryCompiler):
    def get_inner_query(self):
        language = get_language()
        inner_query = super().get_inner_query()
        if 'multi_match' in inner_query:
            inner_query['multi_match']['fields'] = [f'*_{language}']
        return inner_query


class Elasticsearch5SearchBackendLanguageAware(Elasticsearch5SearchBackend):
    query_compiler_class = Elasticsearch5SearchQueryCompilerLanguageAware
    autocomplete_query_compiler_class = Elasticsearch5AutocompleteQueryCompiler
    results_class = Elasticsearch5SearchResults


SearchBackend = Elasticsearch5SearchBackendLanguageAware
