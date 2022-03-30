from tecton import FeatureService
from fraud.features.stream_window_aggregate_feature_views.user_transaction_amount_metrics import user_transaction_amount_metrics
from fraud.features.stream_feature_views.last_transaction_amount_sql import last_transaction_amount_sql
from fraud.features.on_demand_feature_views.transaction_amount_is_higher_than_average import transaction_amount_is_higher_than_average
from fraud.features.stream_window_aggregate_feature_views.merchant_fraud_rate import merchant_fraud_rate


fraud_detection_feature_service = FeatureService(
    name='fraud_detection_feature_service',
    features=[
        merchant_fraud_rate,
        user_transaction_amount_metrics,
        transaction_amount_is_higher_than_average,
        last_transaction_amount_sql,
    ]
)
