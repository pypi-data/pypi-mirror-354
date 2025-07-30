"""Minimal broker protobuf definitions for SDK.

In production, this would be generated from broker.proto
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PublishOptions:
    tier: str = "memory"
    require_ack: bool = False
    timeout_ms: int = 5000


@dataclass
class PublishRequest:
    subject: str
    payload: bytes
    headers: Dict[str, str]
    options: PublishOptions


@dataclass
class PublishResponse:
    message_id: str
    timestamp: Optional[str] = None