from fixtures import client2
import pytest

from backend.report_api.report_func import create_segment
from backend.database import db


@pytest.mark.parametrize("data", [
    ({"photo_type": "sun", "sun_type": "destruction"})
    ])
def test_create_segment(data, client2):
    segment = create_segment(data)
    assert segment.info == '{"photo_type": "sun", "sun_type": "destruction"}'

