# src/agents/campaign_agent.py

from typing import Dict


class CampaignAgent:
    """
    Campaign recommendation & ROI estimation agent.

    Responsibilities:
    - Recommend campaign type & channel
    - Generate customer-facing message
    - Estimate participation rate, cost, and ROI
    """

    # ----------------------------
    # Public API
    # ----------------------------
    def recommend_campaign(
        self,
        segment: str,
        signals: Dict,
        domain_config,
        segment_size: int = 1000,
    ) -> Dict:
        """
        Main entry point.

        Returns a marketing-ready campaign proposal.
        """

        campaign_type, channel = self._select_campaign_type(segment)
        message = self._generate_message(
            segment, signals, domain_config
        )

        participation_rate = self._estimate_participation(segment)
        cost = self._estimate_cost(
            campaign_type, participation_rate, segment_size
        )
        revenue = self._estimate_revenue(
            segment, participation_rate, segment_size
        )

        roi = (
            (revenue - cost) / cost if cost > 0 else 0
        )

        return {
            "segment": segment,
            "campaign_type": campaign_type,
            "channel": channel,
            "duration_days": self._campaign_duration(segment),
            "message": message,
            "estimated_participation_rate": round(
                participation_rate, 2
            ),
            "estimated_cost": round(cost, 2),
            "estimated_revenue": round(revenue, 2),
            "estimated_roi": round(roi, 2),
        }

    # ----------------------------
    # Campaign logic
    # ----------------------------
    def _select_campaign_type(self, segment: str):
        """
        Deterministic mapping from segment → campaign.
        """

        if segment == "Dormant / At-Risk":
            return "Bonus Points", "SMS"

        if segment == "Price-Sensitive Disengagers":
            return "Extra Points", "Push"

        if segment == "Re-Engaging Customers":
            return "Welcome Back Reward", "Email"

        if segment == "Stable Core Customers":
            return "Access / Perk", "Email"

        return "Informational", "Email"

    def _campaign_duration(self, segment: str) -> int:
        if segment == "Dormant / At-Risk":
            return 7
        if segment == "Price-Sensitive Disengagers":
            return 10
        return 14

    # ----------------------------
    # Message generation
    # ----------------------------
    def _generate_message(
        self, segment: str, signals: Dict, domain_config
    ) -> str:
        """
        Simple, empathetic, brand-safe messages.
        """

        if segment == "Dormant / At-Risk":
            return (
                "We’ve missed you! Here’s a little something to welcome "
                "you back. Enjoy bonus rewards on your next visit."
            )

        if segment == "Price-Sensitive Disengagers":
            return (
                "Great value awaits! Earn extra rewards when you shop "
                "with us this week."
            )

        if segment == "Re-Engaging Customers":
            return (
                "Welcome back! We’re excited to have you again. "
                "Enjoy a special reward on us."
            )

        if segment == "Stable Core Customers":
            return (
                "Thanks for being a valued customer! Unlock exclusive "
                "benefits just for you."
            )

        return (
            "Here’s an update on new offers and benefits available "
            "to you."
        )

    # ----------------------------
    # Estimation logic (EXPLAINABLE)
    # ----------------------------
    def _estimate_participation(self, segment: str) -> float:
        """
        Conservative, segment-based participation estimates.
        """

        if segment == "Dormant / At-Risk":
            return 0.12

        if segment == "Price-Sensitive Disengagers":
            return 0.25

        if segment == "Re-Engaging Customers":
            return 0.35

        if segment == "Stable Core Customers":
            return 0.45

        return 0.15

    def _estimate_cost(
        self,
        campaign_type: str,
        participation_rate: float,
        segment_size: int,
    ) -> float:
        """
        Rough but defensible cost model.
        """

        cost_per_participant = {
            "Bonus Points": 40,
            "Extra Points": 30,
            "Welcome Back Reward": 50,
            "Access / Perk": 20,
            "Informational": 5,
        }.get(campaign_type, 20)

        participants = participation_rate * segment_size
        return participants * cost_per_participant

    def _estimate_revenue(
        self,
        segment: str,
        participation_rate: float,
        segment_size: int,
    ) -> float:
        """
        Expected incremental revenue by segment.
        """

        avg_incremental_revenue = {
            "Dormant / At-Risk": 300,
            "Price-Sensitive Disengagers": 450,
            "Re-Engaging Customers": 600,
            "Stable Core Customers": 800,
        }.get(segment, 350)

        participants = participation_rate * segment_size
        return participants * avg_incremental_revenue
