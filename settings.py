import os

QUERY_PATH = "query.json"
INDEX = "art"

CUSTOM_ANALYSER = {
    "analysis": {
        "filter": {
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "english_keywords": {
                "type": "keyword_marker",
                "keywords": ["medieval painting"]
            },
            "english_stemmer": {
                "type": "stemmer",
                "language": "english"
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
            }
        },
        "analyzer": {
            "custom_analyzer": {
                "tokenizer": "standard",
                "char_filter": [
                    "emoticons"
                ],
                "filter": [
                    "lowercase",
                    "english_possessive_stemmer",
                    "english_stop",
                    "english_stemmer"
                ]
            }
        },
        "char_filter": {
            "emoticons": {
                "type": "mapping",
                "mappings": [
                    ":) => happy",
                    ":( => sad",
                    "^_^ => cute",
                    ";) => wink",
                    "xD => laugh"
                ]
            }
        }
    }
}
