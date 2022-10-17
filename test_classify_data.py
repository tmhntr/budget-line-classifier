import pytest
import pandas as pd

from data import LabelData, OneHotData, classify_data, data_to_one_hot

@pytest.fixture
def labels() -> list[str]:
    return ['one', 'two', 'three', 'one', 'two']
    

@pytest.fixture
def raw_data() -> list[str]:
    return ['a', 'b', 'c', 'a', 'b']

@pytest.fixture
def label_data(labels, raw_data, monkeypatch) -> LabelData:
    responses = iter(labels)
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    return classify_data(raw_data)

def test_classify_data_returns_LabelData(label_data):
    assert isinstance(label_data, LabelData)

def test_classify_data_returns_LabelData_with_correct_X(label_data, raw_data):
    assert label_data.X.tolist() == raw_data

def test_classify_data_returns_LabelData_with_correct_y(label_data, labels):
    assert label_data.y.tolist() == labels


@pytest.fixture
def one_hot_data(label_data) -> OneHotData:
    return data_to_one_hot(label_data)

def test_data_to_one_hot_returns_OneHotData(one_hot_data):
    assert isinstance(one_hot_data, OneHotData)

def test_data_to_one_hot_returns_OneHotData_with_correct_X_keys(one_hot_data):
    assert one_hot_data.X_keys.to_list() == ['a', 'b']

def test_data_to_one_hot_returns_OneHotData_with_correct_y_keys(one_hot_data, labels):
    assert set(one_hot_data.y_keys.tolist()) == set(labels)

def test_data_to_one_hot_returns_OneHotData_with_correct_X(one_hot_data):
    assert one_hot_data.X.to_numpy().tolist() == [[1, 0], [0, 1], [0, 0], [1, 0], [0, 1]]

def test_data_to_one_hot_returns_OneHotData_with_correct_y(one_hot_data):
    assert one_hot_data.y.to_numpy().tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]]

def test_data_to_one_hot_returns_OneHotData_with_correct_X_shape(one_hot_data):
    assert one_hot_data.X.shape == (5, 2)

def test_data_to_one_hot_returns_OneHotData_with_correct_y_shape(one_hot_data):
    assert one_hot_data.y.shape == (5, 3)

def test_data_to_one_hot_returns_OneHotData_with_correct_X_keys_shape(one_hot_data):
    assert one_hot_data.X_keys.shape == (2,)

def test_data_to_one_hot_returns_OneHotData_with_correct_y_keys_shape(one_hot_data):
    assert one_hot_data.y_keys.shape == (3,)

