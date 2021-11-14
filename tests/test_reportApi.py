from fixtures import client2
import pytest

from backend.report_api.report_func import create_segment, convert_report_to_json, convert_segment_info_to_readable_view
from backend.database import db

from backend.models.segment import Segment

from backend.report_api.generate_report_file import generate_file
from backend.core_api.generate_report import gen_report


@pytest.mark.parametrize("data", [
    ({"photo_type": "sun", "sun_type": "destruction"})
    ])
def test_create_segment(data, client2):
    segment = create_segment(data, 0.1)
    assert segment.info == '{"photo_type": "sun", "sun_type": "destruction"}'


def test_segment_representation():
    seg = Segment(info='{"photo_type": "sun", "sun_type": "destruction", "test_fields": "test_1"}')
    print(convert_segment_info_to_readable_view(seg))
    assert convert_segment_info_to_readable_view(seg) is None


@pytest.mark.gen
def test_generate_file():
    report = convert_report_to_json(gen_report(1, "sun"))
    report['report_id'] = 1
    assert type(generate_file(report)) is str
