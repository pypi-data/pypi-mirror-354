from typing import Any, Dict, List

import litestar
from litestar import Request, get, post
from litestar.datastructures import State
from litestar.exceptions import NotAuthorizedException
from litestar.response import Redirect, Template
from sqlalchemy.ext.asyncio import AsyncSession

import kodosumi.core
import kodosumi.service.endpoint
from kodosumi.dtypes import RoleEdit
from kodosumi.service.auth import TOKEN_KEY, get_user_details
from kodosumi.service.jwt import operator_guard
from kodosumi.service.role import update_role


class AdminControl(litestar.Controller):

    tags = ["Admin Panel"]
    include_in_schema = False

    @get("/")
    async def home(self) -> Redirect:
        return Redirect("/admin/flow")
    
    @get("/flow")
    async def flow(self, state: State) -> Template:
        data = kodosumi.service.endpoint.get_endpoints(state)
        return Template("flow.html", context={"items": data})

    def _get_endpoints(self, state: State) -> dict:
        endpoints = sorted(state["endpoints"].keys())
        registers = state["settings"].REGISTER_FLOW
        return {
            "endpoints": endpoints,
            "registers": registers,     
            "items": sorted(set(endpoints + registers))
        }

    async def _get_template(self, 
                            request: Request, 
                            transaction: AsyncSession, 
                            state: State,
                            **kwargs) -> Template:
        user = await get_user_details(request.user, transaction)
        data = self._get_endpoints(state)
        return Template(
            "routes.html", context={
                **{
                    "endpoints": data.get("endpoints"),
                    "registers": data.get("registers"),
                    "items": data.get("items"),
                    "user": user,
                    "version": kodosumi.core.__version__
                }, 
                **kwargs
            }
        )

    @get("/routes")
    async def routes(self, 
                     request: Request, 
                     state: State, 
                     transaction: AsyncSession) -> Template:
        return await self._get_template(request, transaction, state)

    @post("/routes", guards=[operator_guard])
    async def routes_update(self, 
                            request: Request, 
                            state: State, 
                            transaction: AsyncSession) -> Template:
        result = {}
        message: Dict[str, List[str]] = {"settings": [], "routes": []}
        form_data = await request.form()
        routes_text = form_data.get("routes", "")
        new_pwd1 = form_data.get("new_password1", "")
        new_pwd2 = form_data.get("new_password2", "")
        email = form_data.get("email", "")
        if routes_text:
            routes = [line.strip() 
                    for line in routes_text.split("\n") 
                    if line.strip()]
            state["routing"] = {}
            state["endpoints"] = {}
            result: Dict[str, Any] = {}
            for url in routes:
                try:
                    ret = await kodosumi.service.endpoint.register(state, url)
                    result[url] = [r.model_dump() for r in ret]
                except Exception as e:
                    result[url] = str(e)  # type: ignore
            message["routes"].append("Routes refreshed")
        else:
            if new_pwd1 and new_pwd2:
                if new_pwd1 != new_pwd2:
                    message["settings"].append("Passwords do not match")
                else:
                    await update_role(
                        request.user, RoleEdit(password=new_pwd1), transaction)
                    message["settings"].append("Password successfully updated")
            if email:
                await update_role(
                    request.user, RoleEdit(email=email), transaction)
                message["settings"].append("Settings updated")
        return await self._get_template(
            request, transaction, state, routes=result, message=message)

    @get("/logout")
    async def logout(self, request: Request) -> Redirect:
        if request.user:
            response = Redirect("/")
            response.delete_cookie(key=TOKEN_KEY)
            return response
        raise NotAuthorizedException(detail="Invalid name or password")
