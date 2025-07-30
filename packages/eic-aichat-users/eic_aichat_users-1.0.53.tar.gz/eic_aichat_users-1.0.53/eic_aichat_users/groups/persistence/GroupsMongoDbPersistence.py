# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, Any

from pip_services4_components.context import IContext
from pip_services4_data.query import DataPage, FilterParams, PagingParams
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from eic_aichat_users.groups.data.GroupV1 import GroupV1
from eic_aichat_users.groups.persistence.IGroupsPersistence import IGroupsPersistence

class AccountsMongoDbPersistence(IdentifiableMongoDbPersistence, IGroupsPersistence):

    def __init__(self):
        super().__init__('groups')
        self._max_page_size = 1000

        self._ensure_index({'org_id': 1})

    def _convert_to_public(self, value: Any) -> Optional[GroupV1]:
        if value is None:
            return None

        return GroupV1(
            id=value.get('_id'),
            title=value.get('title'),
            active_since=value.get('active_since'),
            org_id=value.get('org_id'),
            group_active=value.get('group_active'),

            bage_active=value.get('bage_active'),
            bage_title=value.get('bage_title'),
            bage_subtitle=value.get('bage_subtitle'),
            image_id=value.get('image_id'),
            design=value.get('design')  # Преобразование в enum — если нужно
        )
    
    def __compose_filter(self, filter_params: FilterParams) -> Any:
        filter_params = filter_params or FilterParams()
        criteria = []

        id = filter_params.get_as_nullable_string('id')
        if id:
            criteria.append({'_id': id})

        ids = filter_params.get_as_object('ids')
        if isinstance(ids, str):
            ids = ids.split(',')
        if isinstance(ids, list):
            criteria.append({'_id': {'$in': ids}})

        org_id = filter_params.get_as_nullable_string('org_id')
        if org_id:
            criteria.append({'org_id': org_id})

        not_in_org_ids = filter_params.get_as_object('not_in_org_ids')
        if isinstance(not_in_org_ids, str):
            not_in_org_ids = not_in_org_ids.split(',')
        if isinstance(not_in_org_ids, list):
            criteria.append({'org_id': {'$nin': not_in_org_ids}})

        title = filter_params.get_as_nullable_string('title')
        if title:
            criteria.append({'title': title})

        active_since = filter_params.get_as_nullable_datetime('active_since')
        if active_since:
            criteria.append({'active_since': active_since})

        group_active = filter_params.get_as_nullable_boolean('group_active')
        if group_active is not None:
            criteria.append({'group_active': group_active})

        return {'$and': criteria} if criteria else {}
    
    def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                           paging: PagingParams, sort: Any = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(
            context,
            self.__compose_filter(filter_params),
            paging,
            sort,
            select
        )

    def delete_by_filter(self, context: Optional[IContext], filter_params: FilterParams) -> None:
        return super().delete_by_filter(context, self.__compose_filter(filter_params))