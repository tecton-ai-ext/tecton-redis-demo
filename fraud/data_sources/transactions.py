from tecton import FileDSConfig, KinesisDSConfig, StreamDataSource, BatchDataSource, DatetimePartitionColumn

def raw_data_deserialization(df):
    from pyspark.sql.functions import col, from_json, from_utc_timestamp, when
    from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, BooleanType, IntegerType

    payload_schema = StructType([
        StructField('user_id', StringType(), False),
        StructField('transaction_id', StringType(), False),
        StructField('category', StringType(), False),
        StructField('amt', StringType(), False),
        StructField('is_fraud', StringType(), False),
        StructField('merchant', StringType(), False),
        StructField('merch_lat', StringType(), False),
        StructField('merch_long', StringType(), False),
        StructField('timestamp', StringType(), False),
    ])

    return (
        df.selectExpr('cast (data as STRING) jsonData')
        .select(from_json('jsonData', payload_schema).alias('payload'))
        .select(
            col('payload.user_id').alias('user_id'),
            col('payload.transaction_id').alias('transaction_id'),
            col('payload.category').alias('category'),
            col('payload.amt').cast('double').alias('amt'),
            col('payload.is_fraud').cast('long').alias('is_fraud'),
            col('payload.merchant').alias('merchant'),
            col('payload.merch_lat').cast('double').alias('merch_lat'),
            col('payload.merch_long').cast('double').alias('merch_long'),
            from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
        )
    )

batch_config = FileDSConfig(
    uri='s3://redis-tecton-fraud-demo/transactions.pq',
    file_format="parquet",
    timestamp_column_name="timestamp"
)


transactions_stream = StreamDataSource(
    name='transactions_stream',
    stream_ds_config=KinesisDSConfig(
        stream_name='redis-fraud-demo-stream-2',
        region='us-west-2',
        default_initial_stream_position='latest',
        default_watermark_delay_threshold='24 hours',
        timestamp_key='timestamp',
        raw_stream_translator=raw_data_deserialization,
        # options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
    ),
    batch_ds_config=batch_config,
    family='fraud',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)

transactions_batch = BatchDataSource(
    name='transactions_batch',
    batch_ds_config=batch_config,
    family='fraud_detection',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)
