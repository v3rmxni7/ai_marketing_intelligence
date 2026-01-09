# src/domains/banking.py

from src.domains.base import DomainConfig

BANKING_DOMAIN = DomainConfig(
    name="banking",
    customer_id_field="customer_id",
    category_field="category",
    velocity_unit="transaction_frequency",
    quality_keywords={
        "Premium": [
            "credit",
            "loan",
            "investment",
        ],
        "Value": [
            "debit",
            "savings",
        ],
    },
)
