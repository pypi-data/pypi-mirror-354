# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_mongodb.persistence import IdentifiableMongoDbPersistence

from ..data import GroupMembershipV1
from .IGroupMembershipsPersistence import IGroupMembershipsPersistence


class GroupMembershipsMongoDbPersistence(IdentifiableMongoDbPersistence, IGroupMembershipsPersistence):

    def __init__(self):
        super().__init__('group_memberships')
        self._max_page_size = 100

        self._ensure_index({ "org_id": 1 })
        self._ensure_index({ "profile_id": 1 })
        self._ensure_index({ "offline_id": 1 })
        self._ensure_index({ "group_id": 1 })
        self._ensure_index({ "group_id": 1, "org_id": 1, "profile_id": 1, "offline_id": 1 }, { 'unique': True })

    def _compose_filter(self, filter_params: Optional[FilterParams]) -> Any:
        filter_params = filter_params or FilterParams()
        criteria = []

        def to_list(value):
            if isinstance(value, str):
                return value.split(',')
            elif isinstance(value, list):
                return value
            return None

        id = filter_params.get_as_nullable_string('id')
        if id:
            criteria.append({ '_id': id })

        ids = to_list(filter_params.get_as_object('ids'))
        if ids:
            criteria.append({ '_id': { '$in': ids } })

        profile_ids = to_list(filter_params.get_as_object('profile_ids'))
        if profile_ids:
            criteria.append({ 'profile_id': { '$in': profile_ids } })

        offline_ids = to_list(filter_params.get_as_object('offline_ids'))
        if offline_ids:
            criteria.append({ 'offline_id': { '$in': offline_ids } })

        not_in_org_ids = to_list(filter_params.get_as_object('not_in_org_ids'))
        if not_in_org_ids:
            criteria.append({ 'org_id': { '$nin': not_in_org_ids } })

        offline_or_online_id = filter_params.get_as_nullable_string('offline_or_onlie_id')
        if offline_or_online_id:
            criteria.append({
                '$or': [
                    { 'profile_id': offline_or_online_id },
                    { 'offline_id': offline_or_online_id }
                ]
            })

        offline_or_online_ids = to_list(filter_params.get_as_object('offline_or_onlie_ids'))
        if offline_or_online_ids:
            criteria.append({
                '$or': [
                    { 'profile_id': { '$in': offline_or_online_ids } },
                    { 'offline_id': { '$in': offline_or_online_ids } }
                ]
            })

        org_id = filter_params.get_as_nullable_string('org_id')
        if org_id:
            criteria.append({ 'org_id': org_id })

        profile_id = filter_params.get_as_nullable_string('profile_id')
        if profile_id:
            criteria.append({ 'profile_id': profile_id })

        offline_id = filter_params.get_as_nullable_string('offline_id')
        if offline_id:
            criteria.append({ 'offline_id': offline_id })

        group_id = filter_params.get_as_nullable_string('group_id')
        if group_id:
            criteria.append({ 'group_id': group_id })

        active = filter_params.get_as_nullable_boolean('active')
        if active is not None:
            criteria.append({ 'active': active })

        attempts = filter_params.get_as_nullable_integer('attempts')
        if attempts is not None:
            criteria.append({ 'attempts': attempts })

        return { '$and': criteria } if criteria else {}

    async def get_page_by_filter(self, context: Optional[IContext], filter_params: FilterParams,
                                 paging: PagingParams) -> DataPage:
        return await super().get_page_by_filter(
            context,
            self._compose_filter(filter_params),
            paging,
            None,
            None
        )

    async def delete_by_filter(self, context: Optional[IContext], filter_params: FilterParams) -> None:
        await super().delete_by_filter(context, self._compose_filter(filter_params))

    async def create(self, context: Optional[IContext], item: GroupMembershipV1) -> GroupMembershipV1:
        return await super().create(context, item)
