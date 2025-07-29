# tests/test_OTU_predictor.py
from OTU_predictor.your_module import make_predictions

def test_make_predictions():
    input_file_path = 'OTU_predictor/data/test_data.txt'
    predictions = make_predictions(input_file_path)
    assert isinstance(predictions, list)
    assert len(predictions) > 0

