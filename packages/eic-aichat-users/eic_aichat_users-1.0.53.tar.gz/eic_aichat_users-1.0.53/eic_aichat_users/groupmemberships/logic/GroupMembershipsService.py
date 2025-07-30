# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pip_services4_components.config import ConfigParams, IConfigurable
from pip_services4_components.context import IContext
from pip_services4_components.refer import IReferenceable, IReferences, Descriptor
from pip_services4_data.keys import IdGenerator
from pip_services4_data.query import FilterParams, PagingParams, DataPage
from pip_services4_rpc.commands import ICommandable, CommandSet

from eic_aichat_users.groupmemberships.logic.IGroupMembershipService import IGroupMembershipsService

from ..data import GroupMembershipV1
from ..persistence import IGroupMembershipsPersistence


class GroupMembershipsService(IGroupMembershipsService, IConfigurable, IReferenceable, ICommandable):
    _persistence: IGroupMembershipsPersistence = None

    def configure(self, config: ConfigParams):
        pass

    def set_references(self, references: IReferences):
        self._persistence = references.get_one_required(
            Descriptor('service-groupmemberships', 'persistence', '*', '*', '1.0')
        )

    async def get_memberships(self, context: Optional[IContext], filter_params: FilterParams,
                              paging: PagingParams) -> DataPage:
        return await self._persistence.get_page_by_filter(context, filter_params, paging)

    async def get_membership_by_id(self, context: Optional[IContext], membership_id: str) -> Optional[GroupMembershipV1]:
        return await self._persistence.get_one_by_id(context, membership_id)

    async def create_membership(self, context: Optional[IContext], membership: GroupMembershipV1) -> GroupMembershipV1:
        membership.id = membership.id or IdGenerator.next_long()
        membership.created = membership.created or datetime.utcnow()
        return await self._persistence.create(context, membership)

    async def update_membership(self, context: Optional[IContext], membership: GroupMembershipV1) -> GroupMembershipV1:
        return await self._persistence.update(context, membership)

    async def delete_membership_by_id(self, context: Optional[IContext], membership_id: str) -> Optional[GroupMembershipV1]:
        return await self._persistence.delete_by_id(context, membership_id)

    async def delete_memberships_by_filter(self, context: Optional[IContext], filter_params: FilterParams) -> None:
        await self._persistence.delete_by_filter(context, filter_params)
