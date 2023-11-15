from feast import (
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    Entity
)
from feast.types import String, UnixTimestamp
from feast.data_format import ParquetFormat

entity = Entity(name="entity", join_keys=["entity_no"])

entity_pfv = FeatureView(
    name="entity_pfv",
    entities=[entity],
    schema=[
        Field(name="title", dtype=String),
        Field(name="firstname", dtype=String),
        Field(name="surname", dtype=String),
        Field(name="date_of_birth", dtype=UnixTimestamp),
        Field(name="sys_eff_to", dtype=UnixTimestamp),
    ],
    online=True,
    source=PushSource(
        name="entity_ps",
        batch_source=FileSource(
            file_format=ParquetFormat(),
            path="/work/store/data/mock_data.parquet",
            timestamp_field="sys_eff_from",
        ),
    ),
)

entity_fs = FeatureService(
    name="entity_fs", features=[
        entity_pfv,
    ]
)