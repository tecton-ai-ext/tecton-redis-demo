from tecton import stream_window_aggregate_feature_view, RedisConfig, Input, FeatureAggregation
from fraud.entities import merchant
from fraud.data_sources.transactions import transactions_stream
from datetime import datetime


@stream_window_aggregate_feature_view(
    inputs={'transactions': Input(transactions_stream)},
    entities=[merchant],
    mode='spark_sql',
    aggregation_slide_period='1h',
    aggregations=[FeatureAggregation(column='is_fraud', function='mean', time_windows=['1h','24h','72h'])],
    online=True,
    offline=True,
    online_config=RedisConfig(),
    feature_start_time=datetime(2020, 10, 10),
    family='fraud',
    tags={'release': 'production'},
    owner='matt@tecton.ai',
    description='The merchant fraud rate over series of time windows, updated hourly.'
)
def merchant_fraud_rate(transactions):
    return f'''
        SELECT
            merchant,
            is_fraud,
            timestamp
        FROM
            {transactions}
        '''
