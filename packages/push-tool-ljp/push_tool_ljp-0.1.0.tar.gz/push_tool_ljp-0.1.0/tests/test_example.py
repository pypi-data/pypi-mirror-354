from mypackage.example import hello

def test_hello():
    assert hello() == "Hello, World!"
    assert hello("Alice") == "Hello, Alice!"
