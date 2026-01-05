from src.models import PipelineDef, Step

SIMPLE_ETL = PipelineDef(
    name="Simple ETL",
    steps=[
        Step("Extract", "Pull data from source", annotation="CustomJob"),
        Step("Validate", "Run data quality checks", annotation="Pipeline component"),
        Step("Transform", "Transform / enrich data", annotation="Dataflow / CustomJob"),
        Step("Load", "Write to BigQuery / GCS", annotation="BigQuery / GCS"),
    ],
    edges=[
        ("Extract", "Validate"),
        ("Validate", "Transform"),
        ("Transform", "Load"),
    ],
)

INCREMENTAL_LOAD = PipelineDef(
    name="Incremental Load",
    steps=[
        Step("Get Watermark", "Read last processed checkpoint", annotation="BigQuery / Metadata"),
        Step("Extract Delta", "Pull only changed records", annotation="CustomJob"),
        Step("Validate", "Run DQ checks", annotation="Pipeline component"),
        Step("Upsert", "Merge into target table", annotation="BigQuery MERGE"),
        Step("Update Watermark", "Write new checkpoint", annotation="BigQuery / Metadata"),
    ],
    edges=[
        ("Get Watermark", "Extract Delta"),
        ("Extract Delta", "Validate"),
        ("Validate", "Upsert"),
        ("Upsert", "Update Watermark"),
    ],
)

BACKFILL = PipelineDef(
    name="Backfill",
    steps=[
        Step("Plan Partitions", "Generate date partitions to process", annotation="CustomJob"),
        Step("Extract", "Pull partitioned raw data", annotation="CustomJob"),
        Step("Transform", "Partition-wise transform", annotation="Dataflow / CustomJob"),
        Step("Load", "Write partition outputs", annotation="BigQuery / GCS"),
        Step("Publish Metrics", "Counts, failures, latency", annotation="BQ / Logging"),
    ],
    edges=[
        ("Plan Partitions", "Extract"),
        ("Extract", "Transform"),
        ("Transform", "Load"),
        ("Load", "Publish Metrics"),
    ],
)

PIPELINES = {
    SIMPLE_ETL.name: SIMPLE_ETL,
    INCREMENTAL_LOAD.name: INCREMENTAL_LOAD,
    BACKFILL.name: BACKFILL,
}
