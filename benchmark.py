from datetime import datetime, timedelta
from random import uniform
import base64, os
import pandas
from pathlib import Path

event_date_time = datetime.fromisoformat("2000-01-01 12:00")

entities = pandas.DataFrame(
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
        for entity_no in range(200000)
    ]
)

entities = entities.infer_objects()

import time
from feast import FeatureStore
from feast.data_source import PushMode
from feast.repo_config import load_repo_config, RepoConfig
from feast.repo_operations import apply_total
from pathlib import Path

feature_store_config = load_repo_config(
    Path("/work/store/"),
    "/work/store/feature_store.yaml"
)
feature_store = FeatureStore(config=feature_store_config)

# apply_total(
#     feature_store_config,
#     Path("/work/store"),
#     False
# )

t_start = time.time()
feature_store.push("entity_ps", entities, to=PushMode.ONLINE)
print(f"Pushed {len(entities)} in: {time.time() - t_start} s")

entity_counts = []
for factor in [1, 10, 100]:
    for factor2 in [5, 10, 15, 50, 1000, 2000]:
        count = factor*factor2
        if count <= len(entities):
            entity_counts.append(count)
entity_counts = list(set(entity_counts))
entity_counts.sort()
entity_counts

whcaent_ent_fs = feature_store.get_feature_service("entity_fs")
# entity_counts.reverse()
average_over_n = 3
batch_elapsed_map = {}
for entity_count in entity_counts:
    entity_rows = [
        # {join_key: entity_value}
        {"entity_no": entity_no}
        for entity_no in range(entity_count)
    ]
    print(f"entity_count: {entity_count}")
    batch_elapsed_map[entity_count] = []
    for rev_keys in [False, True]:
        if rev_keys:
            entity_rows.reverse()
        t_start_avg = time.time()
        for i in range(average_over_n):
            t_start = time.time()
            feature_store.get_online_features(
                features=whcaent_ent_fs,
                entity_rows=entity_rows,
            )
            batch_elapsed_map[entity_count].append(time.time() - t_start)
            print(f"({i}) size: {entity_count}, elapsed: {batch_elapsed_map[entity_count][-1]} s")
