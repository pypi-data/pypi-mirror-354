# -*- coding: utf-8 -*-
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema


class GroupV1Schema(ObjectSchema):
    def __init__(self):
        super().__init__()

        self.with_optional_property('id', TypeCode.String)
        self.with_optional_property('title', TypeCode.String)
        self.with_optional_property('active_since', TypeCode.DateTime)
        self.with_required_property('org_id', TypeCode.String)
        self.with_required_property('group_active', TypeCode.Boolean)

        self.with_required_property('bage_active', TypeCode.Boolean)
        self.with_optional_property('bage_title', TypeCode.String)
        self.with_optional_property('bage_subtitle', TypeCode.String)
        self.with_optional_property('image_id', TypeCode.String)
        self.with_optional_property('design', TypeCode.String)
