# -*- coding: utf-8 -*-
from typing import Any, Optional
from datetime import datetime

from pip_services4_data.data import IStringIdentifiable
from pip_services4_data.keys import IdGenerator

from eic_aichat_users.groups.data.BageDesignTypeV1 import BageDesignTypeV1

class GroupV1(IStringIdentifiable):
    def __init__(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        active_since: Optional[datetime] = None,
        org_id: Optional[str] = None,
        group_active: Optional[bool] = True,

        # Bage
        bage_active: Optional[bool] = False,
        bage_title: Optional[str] = None,
        bage_subtitle: Optional[str] = None,
        image_id: Optional[str] = None,
        design: Optional[BageDesignTypeV1] = None
    ):
        self.id: str = id or IdGenerator.next_long()
        self.title = title
        self.active_since = active_since or datetime.now()
        self.org_id = org_id
        self.group_active = group_active

        self.bage_active = bage_active
        self.bage_title = bage_title
        self.bage_subtitle = bage_subtitle
        self.image_id = image_id
        self.design = design

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "active_since": self.active_since.isoformat() if isinstance(self.active_since, datetime) else self.active_since,
            "org_id": self.org_id,
            "group_active": self.group_active,

            "bage_active": self.bage_active,
            "bage_title": self.bage_title,
            "bage_subtitle": self.bage_subtitle,
            "image_id": self.image_id,
            "design": self.design.value if self.design else None
        }