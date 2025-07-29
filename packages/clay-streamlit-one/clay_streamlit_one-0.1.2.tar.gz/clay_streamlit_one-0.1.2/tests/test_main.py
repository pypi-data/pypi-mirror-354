from clay_streamlit_one import get_hello_world

def test_get_hello_world():
    assert get_hello_world() == "hello"
