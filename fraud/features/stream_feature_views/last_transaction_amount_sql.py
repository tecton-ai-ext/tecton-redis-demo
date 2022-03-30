from tecton import stream_feature_view, Input, RedisConfig
from fraud.entities import user
from fraud.data_sources.transactions import transactions_stream
from datetime import datetime

@stream_feature_view(
    inputs={'transactions': Input(transactions_stream)},
    entities=[user],
    mode='spark_sql',
    online=True,
    offline=True,
    online_config=RedisConfig(),
    feature_start_time=datetime(2021, 5, 20),
    batch_schedule='1d',
    ttl='30days',
    family='fraud',
    description='Last user transaction amount (stream calculated)'
)
def last_transaction_amount_sql(transactions):
    return f'''
        SELECT
            timestamp,
            user_id,
            amt
        FROM
            {transactions}
        '''
