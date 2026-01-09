# src/domains/oil.py

from src.domains.base import DomainConfig

OIL_DOMAIN = DomainConfig(
    name="oil",
    customer_id_field="customer_id",
    category_field="category",
    velocity_unit="refuel_frequency",
    quality_keywords={
        "Premium": [
            "premium",
            "power",
            "xtra",
            "high octane",
        ],
        "Value": [
            "regular",
            "standard",
            "basic",
        ],
    },
)
