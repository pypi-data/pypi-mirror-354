import uuid
from typing import Union
import litestar
from litestar import delete, get, post, put
from litestar.exceptions import NotFoundException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kodosumi.dtypes import Role, RoleCreate, RoleEdit, RoleResponse
from kodosumi.log import logger
from kodosumi.service.jwt import operator_guard


async def update_role(rid: Union[uuid.UUID, str],
                      data: RoleEdit, 
                      transaction: AsyncSession) -> RoleResponse:
    if isinstance(rid, str):
        rid = uuid.UUID(rid)
    query = select(Role).where(Role.id == rid)
    result = await transaction.execute(query)
    role = result.scalar_one_or_none()
    if not role:
        raise NotFoundException(detail=f"role {rid} not found")
    update = False
    for field in ("name", "email", "password", "active", "operator"):
        new = getattr(data, field)
        current = getattr(role, field)
        if new is not None and new != current:
            setattr(role, field, new)
            update = True
    if update:
        await transaction.flush()
        logger.info(f"updated role {role.name} ({role.id})")
    return RoleResponse.model_validate(role)


class RoleControl(litestar.Controller):

    tags = ["Access Management"]
    guards=[operator_guard]

    @post("/")
    async def add_role(self, 
                       data: RoleCreate, 
                       transaction: AsyncSession) -> RoleResponse:
        role = Role(**data.model_dump())
        transaction.add(role)
        await transaction.flush()
        logger.info(f"created role {role.name} ({role.id})")
        return RoleResponse.model_validate(role)    
        
    @get("/")
    async def list_roles(self, 
                         transaction: AsyncSession) -> list[RoleResponse]:
        query = select(Role)
        result = await transaction.execute(query)
        ret = [RoleResponse.model_validate(d) for d in result.scalars().all()]
        ret.sort(key=lambda x: x.name)
        return ret
    
    @get("/{name:str}")
    async def get_role(self, 
                       name: str, 
                       transaction: AsyncSession) -> RoleResponse:
        query = select(Role).where(Role.name == name)
        result = await transaction.execute(query)
        role = result.scalar_one_or_none()
        if not role:
            try:
                uid = uuid.UUID(name)
            except:
                raise NotFoundException(detail=f"role {name} not found")
            query = select(Role).where(Role.id == uid)
            result = await transaction.execute(query)
            role = result.scalar_one_or_none()
        if role:
            return RoleResponse.model_validate(role)
        raise NotFoundException(detail=f"role {name} not found")

    @delete("/{rid:uuid}")
    async def delete_role(self, 
                          rid: uuid.UUID, 
                          transaction: AsyncSession) -> None:
        query = select(Role).where(Role.id == rid)
        result = await transaction.execute(query)
        role = result.scalar_one_or_none()
        if role:
            await transaction.delete(role)
            logger.info(f"deleted role {role.name} ({role.id})")
            return None
        raise NotFoundException(detail=f"role {rid} not found")

    @put("/{rid:uuid}")
    async def edit_role(self, 
                        rid: uuid.UUID, 
                        data: RoleEdit, 
                        transaction: AsyncSession) -> RoleResponse:
        return await update_role(rid, data, transaction)

