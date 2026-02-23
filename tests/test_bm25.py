"""Tests for BM25 keyword search."""

from memotrail.core.bm25 import BM25Index, _tokenize


class TestTokenize:
    def test_basic(self):
        tokens = _tokenize("Hello world")
        assert "hello" in tokens
        assert "world" in tokens

    def test_filters_stop_words(self):
        tokens = _tokenize("the quick and the slow")
        assert "the" not in tokens
        assert "and" not in tokens
        assert "quick" in tokens
        assert "slow" in tokens

    def test_filters_short_tokens(self):
        tokens = _tokenize("I a am OK fine")
        assert "i" not in tokens
        assert "a" not in tokens
        assert "ok" in tokens
        assert "fine" in tokens

    def test_empty_string(self):
        assert _tokenize("") == []


class TestBM25Index:
    def test_empty_index(self):
        index = BM25Index()
        results = index.search("test")
        assert results == []

    def test_basic_search(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1", "2", "3"],
            texts=[
                "Python is a programming language",
                "JavaScript runs in the browser",
                "Python and JavaScript are popular",
            ],
        )

        results = index.search("Python programming")
        assert len(results) > 0
        assert results[0].doc_id == "1"  # Most relevant

    def test_no_match(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1"],
            texts=["cats dogs animals"],
        )
        results = index.search("quantum physics")
        assert results == []

    def test_limit(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1", "2", "3", "4", "5"],
            texts=[f"document about topic {i}" for i in range(5)],
        )
        results = index.search("document topic", limit=2)
        assert len(results) <= 2

    def test_metadata_filter(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1", "2"],
            texts=[
                "Python Flask web server",
                "Python Django web framework",
            ],
            metadatas=[
                {"project": "flask-app"},
                {"project": "django-app"},
            ],
        )
        results = index.search("Python web", where={"project": "flask-app"})
        assert len(results) == 1
        assert results[0].doc_id == "1"

    def test_document_count(self):
        index = BM25Index()
        assert index.document_count == 0

        index.add_documents(["1", "2"], ["hello", "world"])
        assert index.document_count == 2

    def test_scores_are_positive(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1"],
            texts=["Redis caching performance"],
        )
        results = index.search("Redis caching")
        assert len(results) == 1
        assert results[0].score > 0

    def test_relevance_ranking(self):
        index = BM25Index()
        index.add_documents(
            doc_ids=["1", "2", "3"],
            texts=[
                "Python error handling with try except blocks",
                "error error error in the Python code",
                "JavaScript callback functions",
            ],
        )
        results = index.search("Python error")
        # Both Python-related docs should come before JavaScript doc
        result_ids = [r.doc_id for r in results]
        assert "3" not in result_ids or result_ids.index("3") > result_ids.index("1")
