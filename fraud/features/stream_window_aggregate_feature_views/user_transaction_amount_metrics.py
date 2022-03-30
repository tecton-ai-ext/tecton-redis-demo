from tecton import stream_window_aggregate_feature_view, Input, FeatureAggregation, RedisConfig
from fraud.entities import user
from fraud.data_sources.transactions import transactions_stream
from datetime import datetime


# The following defines several sliding time window aggregations over a user's transaction amounts
@stream_window_aggregate_feature_view(
    inputs={'transactions': Input(transactions_stream)},
    entities=[user],
    mode='spark_sql',
    aggregation_slide_period='10m',  # Defines how frequently feature values get updated in the online store
    batch_schedule='1d', # Defines how frequently batch jobs are scheduled to ingest into the offline store
    aggregations=[
        FeatureAggregation(column='amt', function='mean', time_windows=['1h', '12h', '24h','72h']),
        FeatureAggregation(column='amt', function='sum', time_windows=['1h', '12h', '24h','72h'])
    ],
    online=True,
    offline=True,
    online_config=RedisConfig(),
    feature_start_time=datetime(2020, 10, 10),
    family='fraud',
    tags={'release': 'production'},
    owner='kevin@tecton.ai',
    description='Transaction amount statistics and total over a series of time windows, updated every 10 minutes.'
)
def user_transaction_amount_metrics(transactions):
    return f'''
        SELECT
            user_id,
            amt,
            timestamp
        FROM
            {transactions}
        '''
