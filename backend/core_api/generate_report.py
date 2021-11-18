import random
import json

from backend.models.report import Report
from backend.models.segment import Segment
from backend.core_api.fields_control import config

from backend.report_api.report_func import convert_segment_info_to_readable_view


photo_type = {'ultraviolet': 'uf_type', 'sun': 'sun_type'}
photo_val = {
    'uf_type': [('glow', 'glow_kind')],
    'sun_type': [('destruction', 'destr_kind'), ('formation', 'formation_kind')]
}
val_val = {
    'glow_kind': ['lack', 'carbonate', 'saturated'],
    'formation_kind': ['interleaving', 'sandstone', 'clay_sandstone', 'siltstone', 'clay_silstone', 'argillite'],
    'destr_kind': ['fault', 'content']

}


def gen_report(user_id, ph_type, ph_url, photo_name):
    ph_type = (ph_type, photo_type[ph_type])
    report = Report(photo_name=photo_name,
                    photo_url=ph_url,
                    photo_type=ph_type[0], user_id=user_id)
    n = random.randint(3,10)
    for i in range(random.randint(3,10)):
        ph_val = random.choice(photo_val[ph_type[1]])
        v_val = random.choice(val_val[ph_val[1]])
        info = {
            "photo_type": ph_type[0],
            ph_type[1]: ph_val[0],
            ph_val[1]: v_val,
        }
        segment = Segment(offset=i/n, info=json.dumps(info))
        report.segments.append(segment)
    return report


if __name__ == '__main__':
    gen_report(1)