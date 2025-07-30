# Import the package
import trelasticext as ee
import json

# Test basic functionality
def test_basic_functionality():
    # Setup test parameters
    es_params = {"ehost": "http://localhost:9200", "index": "rabbinic2"}
    
    text = "בראשית ברא"
    
    # Test tokenization
    tokens = ee.ftokens(text)
    print(f"Tokenized text: {tokens}")
    
    # Test query building
    query = ee.query_builder(
        text="test query",
        fields=[ "sentence"],
        fuzziness=1,
        query_type="multimatch",
        operator="OR",
        filter= {'must': ["Tanakh", "Bavli", "Tanakh"]}
    )
    print(f"Built query: {json.dumps(query,ensure_ascii=False)}")
    
    # Try to connect to Elasticsearch (if available)
    try:
        from elasticsearch import Elasticsearch
        es = Elasticsearch(es_params["ehost"])
        info = es.info()
        print(f"Connected to Elasticsearch: {info['version']['number']}")
    except Exception as e:
        print(f"Could not connect to Elasticsearch: {e}")

if __name__ == "__main__":
    test_basic_functionality()