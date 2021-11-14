from fixtures import client2
import pytest

from backend.report_api.report_func import create_segment, convert_segment_to_readable_view
from backend.database import db

from backend.models.segment import Segment


@pytest.mark.parametrize("data", [
    ({"photo_type": "sun", "sun_type": "destruction"})
    ])
def test_create_segment(data, client2):
    segment = create_segment(data)
    assert segment.info == '{"photo_type": "sun", "sun_type": "destruction"}'


def test_segment_representation():
    seg = Segment(info='{"photo_type": "sun", "sun_type": "destruction", "test_fields": "test_1"}')
    print(convert_segment_to_readable_view(seg))
    assert convert_segment_to_readable_view(seg) is None
