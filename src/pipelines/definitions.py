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

CDC_MERGE = PipelineDef(
    name="CDC Merge",
    steps=[
        Step("Read Change Feed", "Ingest CDC stream", annotation="Datastream / BQ"),
        Step("Deduplicate", "Resolve late and duplicate events", annotation="SQL / CustomJob"),
        Step("Merge Upsert", "Apply changes to target", annotation="BigQuery MERGE"),
        Step("Audit Log", "Write audit rows", annotation="BQ / Logging"),
    ],
    edges=[
        ("Read Change Feed", "Deduplicate"),
        ("Deduplicate", "Merge Upsert"),
        ("Merge Upsert", "Audit Log"),
    ],
)

SNAPSHOT_DIFF = PipelineDef(
    name="Snapshot Diff",
    steps=[
        Step("Extract Snapshot", "Full snapshot extract", annotation="CustomJob"),
        Step("Compare Snapshots", "Detect changes", annotation="SQL / Dataflow"),
        Step("Apply Deltas", "Update targets", annotation="BigQuery / GCS"),
        Step("Publish Metrics", "Counts, drift, failures", annotation="BQ / Logging"),
    ],
    edges=[
        ("Extract Snapshot", "Compare Snapshots"),
        ("Compare Snapshots", "Apply Deltas"),
        ("Apply Deltas", "Publish Metrics"),
    ],
)

PIPELINES = {
    SIMPLE_ETL.name: SIMPLE_ETL,
    INCREMENTAL_LOAD.name: INCREMENTAL_LOAD,
    BACKFILL.name: BACKFILL,
    CDC_MERGE.name: CDC_MERGE,
    SNAPSHOT_DIFF.name: SNAPSHOT_DIFF,
}
