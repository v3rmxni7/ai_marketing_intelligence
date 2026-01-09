# src/domains/supermarket.py

from src.domains.base import DomainConfig

SUPERMARKET_DOMAIN = DomainConfig(
    name="supermarket",
    customer_id_field="customer_id",
    category_field="category",
    velocity_unit="basket_frequency",
    quality_keywords={
        "Premium": [
            "organic",
            "premium",
            "artisan",
            "wagyu",
            "imported",
            "single origin",
            "luxury",
        ],
        "Value": [
            "basic",
            "store brand",
            "instant",
            "budget",
            "frozen",
            "economy",
        ],
    },
)
