from datetime import datetime, timedelta
from random import uniform
import base64, os
import pandas

event_date_time = datetime.fromisoformat("2000-01-01 12:00")

pd = pandas.DataFrame(
    [
        {
            'entity_no': entity_no,
            'title': ["Mr", "Mrs", "Ms", "Dr"][int(uniform(0, 4)//1)],
            'firstname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
            'surname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
            'date_of_birth': event_date_time - timedelta(days=uniform(18, 65)*365),
            'sys_eff_to': event_date_time + timedelta(days=uniform(180, 365*5)),
            'sys_eff_from': event_date_time,
        }
        for entity_no in range(100)
    ]
)

pd = pd.infer_objects()
pd.to_parquet("/work/store/data/mock_data.parquet")