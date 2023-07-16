import string
import time
from functools import wraps

import Stemmer
from data_handler.models import Request
from django.db import connection
from nltk import corpus, word_tokenize


def timeit(func):
    """Decorator to measure time of function execution."""

    @wraps(func)
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for {func.__name__}: {elapsed_time:.5f} sec.")
        return result

    return timed


class TextPreprocessor:
    """Class for text preprocessing."""

    ADDITIONAL_STOPWORDS = {
        "инсульт",
        "инсульта",
        "инсульту",
        "инсультом",
        "инсульте",
        "инсульты",
        "инсультов",
        "инсультам",
        "инсультами",
        "инсультах",
    }

    def __init__(self, input_text):
        self.text = input_text
        self.tokens = None
        self.language = "russian"
        self.stemmer = Stemmer.Stemmer(self.language)

    def _tokenize(self):
        """Tokenize text."""
        self.tokens = word_tokenize(self.text.lower())

    def filter_stopwords(self):
        """Filter stopwords."""
        stopwords = set(corpus.stopwords.words(self.language)) | self.ADDITIONAL_STOPWORDS | set(map(str, range(0, 10)))
        self.tokens = [word for word in self.tokens if word not in stopwords]

    def filter_punctuation(self):
        """Filter punctuation."""
        self.tokens = ["".join(c for c in w if c not in string.punctuation) for w in self.tokens]

    def stem_words(self):
        """Stem words."""
        self.tokens = self.stemmer.stemWords([word for word in self.tokens if word])

    def preprocess(self):
        """Preprocess text."""
        self._tokenize()
        self.filter_stopwords()
        self.filter_punctuation()
        self.stem_words()
        return self.tokens

    def get_query_string(self):
        """Get query string ready for ORM."""
        return " & ".join(self.preprocess())


def find_closest_request(user_request):
    """Find closest request in the database."""
    query_string = TextPreprocessor(user_request).get_query_string()
    closest_request = None
    max_rank = 0
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT id, request, ts_rank_cd(tsv, to_tsquery(%s)) AS rank
            FROM {Request._meta.db_table}
            WHERE tsv @@ to_tsquery(%s)
            ORDER BY rank DESC
        """,
            [query_string, query_string],
        )

        for row in cursor.fetchall():
            object_id, db_request, rank = row

            if rank > max_rank:
                max_rank = rank
                closest_request = Request.objects.get(id=object_id)
    return closest_request
