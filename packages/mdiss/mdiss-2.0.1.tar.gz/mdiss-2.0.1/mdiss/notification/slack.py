"""
Slack notification service for mdiss.
"""

import json
from typing import List, Dict, Optional
from datetime import datetime
import requests

from ..models import FailedCommand, Priority, Category


class SlackNotificationService:
    """Service for sending Slack notifications."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = requests.Session()

    def send_failure_summary(self, commands: List[FailedCommand],
                           title: str = "Build Failures Detected") -> bool: