# src/domains/base.py

from typing import Dict, List

class DomainConfig:
    def __init__(
        self,
        name: str,
        customer_id_field: str,
        category_field: str,
        velocity_unit: str,
        quality_keywords: dict,
    ):
        self.name = name
        self.customer_id_field = customer_id_field
        self.category_field = category_field
        self.velocity_unit = velocity_unit
        self.quality_keywords = quality_keywords
