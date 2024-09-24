from src.evaluation import compare_signatures

def test_compare_signatures():
    signature1 = "(a->b)->[a]->[b]"
    signature2 = "(a -> b) -> [a] -> [b]"
    
    assert compare_signatures(signature1, signature2)
    
    signature1 = "(a->b)->[a]->[b]"
    signature2 = "(a -> b) -> [a] -> [c]"
    
    assert not compare_signatures(signature1, signature2)

if __name__ == "__main__":
    test_compare_signatures()

