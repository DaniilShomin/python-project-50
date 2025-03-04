from gendiff.modules import generate_diff


def test_generate_diff():
    result = '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}'''
    assert generate_diff('data/file1.json', 'data/file2.json') == result