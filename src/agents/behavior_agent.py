# src/agents/behavior_agent.py

from datetime import datetime
from typing import List, Dict


class BehaviorAgent:
    """
    Deterministic behavior intelligence agent.
    """

    def analyze_customer(
        self,
        customer_id: str,
        transactions: List[Dict],
        domain_config,
    ) -> Dict:

        cid_field = domain_config.customer_id_field  # 🔑 FIX

        # Filter transactions for this customer (DOMAIN-AWARE)
        customer_txns = [
            t for t in transactions if t.get(cid_field) == customer_id
        ]

        # ----------------------------
        # TRUE no-activity case
        # ----------------------------
        if len(customer_txns) == 0:
            return {
                "customer_id": customer_id,
                "segment": "No Activity",
                "signals": {},
            }

        # ----------------------------
        # Sparse activity (monitor)
        # ----------------------------
        if len(customer_txns) < 3:
            signals = {
                "velocity_trend": "Stable",
                "velocity_change_pct": 0.0,
                "engagement_score": 1.0,
                "category_concentration": "Stable",
                "quality_shift": "Stable",
                "habit_break_detected": False,
                "velocity_unit": domain_config.velocity_unit,
            }

            return {
                "customer_id": customer_id,
                "segment": "Monitor",
                "signals": signals,
            }

        # ----------------------------
        # Full behavior analysis
        # ----------------------------
        baseline_txns, recent_txns = self._split_time_windows(
            customer_txns
        )

        signals = self._extract_signals(
            baseline_txns, recent_txns, domain_config
        )

        segment = self._assign_segment(signals)

        return {
            "customer_id": customer_id,
            "segment": segment,
            "signals": signals,
        }

    # --------------------------------------------------
    # SIGNAL EXTRACTION (UNCHANGED)
    # --------------------------------------------------

    def _extract_signals(
        self,
        baseline_txns: List[Dict],
        recent_txns: List[Dict],
        domain_config,
    ) -> Dict:

        baseline_count = len(baseline_txns)
        recent_count = len(recent_txns)

        velocity_change_pct = (
            ((recent_count - baseline_count) / baseline_count) * 100
            if baseline_count > 0
            else 0.0
        )

        if velocity_change_pct < -15:
            velocity_trend = "Decreasing"
        elif velocity_change_pct > 15:
            velocity_trend = "Increasing"
        else:
            velocity_trend = "Stable"

        engagement_score = (
            recent_count / baseline_count
            if baseline_count > 0
            else 1.0
        )

        baseline_categories = {
            t[domain_config.category_field] for t in baseline_txns
        }
        recent_categories = {
            t[domain_config.category_field] for t in recent_txns
        }

        if len(recent_categories) < len(baseline_categories):
            category_concentration = "Narrowing"
        elif len(recent_categories) > len(baseline_categories):
            category_concentration = "Expanding"
        else:
            category_concentration = "Stable"

        baseline_quality = self._classify_quality(
            baseline_txns, domain_config
        )
        recent_quality = self._classify_quality(
            recent_txns, domain_config
        )

        if baseline_quality != recent_quality:
            quality_shift = f"{baseline_quality} → {recent_quality}"
        else:
            quality_shift = "Stable"

        habit_break_detected = (
            velocity_trend == "Decreasing"
            or category_concentration == "Narrowing"
            or "→" in quality_shift
        )

        return {
            "velocity_trend": velocity_trend,
            "velocity_change_pct": round(velocity_change_pct, 2),
            "engagement_score": round(engagement_score, 2),
            "category_concentration": category_concentration,
            "quality_shift": quality_shift,
            "habit_break_detected": habit_break_detected,
            "velocity_unit": domain_config.velocity_unit,
        }

    # --------------------------------------------------
    # SEGMENT ASSIGNMENT
    # --------------------------------------------------

    def _assign_segment(self, signals: Dict) -> str:

        engagement = signals["engagement_score"]
        velocity = signals["velocity_trend"]
        quality_shift = signals["quality_shift"]
        habit_break = signals["habit_break_detected"]

        if engagement < 0.4 and habit_break:
            return "Dormant / At-Risk"

        if "Premium → Value" in quality_shift:
            return "Price-Sensitive Disengagers"

        if engagement > 0.85 and velocity == "Stable":
            return "Stable Core Customers"

        if velocity == "Increasing":
            return "Re-Engaging Customers"

        return "Monitor"

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _split_time_windows(self, transactions: List[Dict]):
        """
        60% baseline, 40% recent.
        Guaranteed to work for len >= 3
        """

        txns = sorted(
            transactions,
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
        )

        split_index = max(1, int(len(txns) * 0.6))
        return txns[:split_index], txns[split_index:]

    def _classify_quality(
        self, transactions: List[Dict], domain_config
    ) -> str:

        premium_hits = 0
        value_hits = 0

        for t in transactions:
            name = t["item_name"].lower()

            for kw in domain_config.quality_keywords.get("Premium", []):
                if kw in name:
                    premium_hits += 1

            for kw in domain_config.quality_keywords.get("Value", []):
                if kw in name:
                    value_hits += 1

        if premium_hits > value_hits:
            return "Premium"
        if value_hits > premium_hits:
            return "Value"
        return "Neutral"
