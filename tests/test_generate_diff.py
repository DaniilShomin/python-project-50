from gendiff.modules import generate_diff


def test_generate_diff():
    # flat diff
    with open('tests/test_data/flat_result.txt') as f:
        result = f.read()
    assert generate_diff('data/file1.json', 'data/file2.json') == result
    assert generate_diff('data/file1.yaml', 'data/file2.yaml') == result
    # nested diff
    with open('tests/test_data/nested_result.txt') as f:
        result = f.read()
    assert generate_diff('data/file3.json', 'data/file4.json') == result
    assert generate_diff('data/file3.yaml', 'data/file4.yaml') == result


def test_generate_diff_plain():
    with open('tests/test_data/nested_plain_result.txt') as f:
        result = f.read()
    assert generate_diff(
        'data/file3.json', 
        'data/file4.json', 
        'plain'
        ) == result
    assert generate_diff(
        'data/file3.yaml', 
        'data/file4.yaml', 
        'plain'
        ) == result


def test_generate_diff_json():
    with open('tests/test_data/json_result.txt') as f:
        result = f.read()
    assert generate_diff(
        'data/file3.json', 
        'data/file4.json', 
        'json'
        ) == result
    assert generate_diff(
        'data/file3.yaml', 
        'data/file4.yaml', 
        'json'
        ) == result
    