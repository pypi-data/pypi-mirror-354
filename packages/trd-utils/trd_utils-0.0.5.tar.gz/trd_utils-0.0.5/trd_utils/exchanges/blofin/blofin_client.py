from decimal import Decimal
import json
import logging
from typing import Type
import httpx

import time
from pathlib import Path

from trd_utils.exchanges.blofin.blofin_types import (
    BlofinApiResponse,
    CmsColorResponse,
    CopyTraderInfoResponse,
    CopyTraderOrderHistoryResponse,
    CopyTraderOrderListResponse,
    ShareConfigResponse,
)
from trd_utils.cipher import AESCipher
from trd_utils.exchanges.exchange_base import ExchangeBase

logger = logging.getLogger(__name__)


class BlofinClient(ExchangeBase):
    ###########################################################
    # region client parameters
    blofin_api_base_host: str = "https://\u0062lofin.co\u006d"
    blofin_api_base_url: str = "https://\u0062lofin.co\u006d/uapi/v1"
    origin_header: str = "https://\u0062lofin.co\u006d"

    timezone: str = "Etc/UTC"

    # endregion
    ###########################################################
    # region client constructor
    def __init__(
        self,
        account_name: str = "default",
        http_verify: bool = True,
        fav_letter: str = "^",
        read_session_file: bool = True,
        sessions_dir: str = "sessions",
    ):
        self.httpx_client = httpx.AsyncClient(
            verify=http_verify,
            http2=True,
            http1=False,
        )
        self.account_name = account_name
        self._fav_letter = fav_letter
        self.sessions_dir = sessions_dir

        if read_session_file:
            self.read_from_session_file(f"{sessions_dir}/{self.account_name}.bf")

    # endregion
    ###########################################################
    # region v1/cms/
    async def get_share_config(self) -> ShareConfigResponse:
        headers = self.get_headers()
        return await self.invoke_get(
            f"{self.blofin_api_base_url}/cms/share_config",
            headers=headers,
            model=ShareConfigResponse,
        )

    async def get_cms_color(self) -> CmsColorResponse:
        headers = self.get_headers()
        return await self.invoke_get(
            f"{self.blofin_api_base_url}/cms/color",
            headers=headers,
            model=CmsColorResponse,
        )

    # endregion
    ###########################################################
    # region copy/trader
    async def get_copy_trader_info(self, uid: int) -> CopyTraderInfoResponse:
        payload = {
            "uid": uid,
        }
        headers = self.get_headers()
        return await self.invoke_post(
            f"{self.blofin_api_base_url}/copy/trader/info",
            headers=headers,
            content=payload,
            model=CopyTraderInfoResponse,
        )

    async def get_copy_trader_order_list(
        self,
        from_param: int,
        limit_param: 0,
        uid: int,
    ) -> CopyTraderOrderListResponse:
        payload = {
            "from": from_param,
            "limit": limit_param,
            "uid": uid,
        }
        headers = self.get_headers()
        return await self.invoke_post(
            f"{self.blofin_api_base_url}/copy/trader/order/list",
            headers=headers,
            content=payload,
            model=CopyTraderOrderListResponse,
        )
    
    async def get_copy_trader_order_history(
        self,
        from_param: int,
        limit_param: 0,
        uid: int,
    ) -> CopyTraderOrderHistoryResponse:
        payload = {
            "from": from_param,
            "limit": limit_param,
            "uid": uid,
        }
        headers = self.get_headers()
        return await self.invoke_post(
            f"{self.blofin_api_base_url}/copy/trader/order/history",
            headers=headers,
            content=payload,
            model=CopyTraderOrderHistoryResponse,
        )

    # endregion
    ###########################################################
    # region client helper methods
    def get_headers(self, payload=None, needs_auth: bool = False) -> dict:
        the_timestamp = int(time.time() * 1000)
        the_headers = {
            # "Host": self.blofin_api_base_host,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": self.origin_header,
            "X-Tz": self.timezone,
            "Fp-Request-Id": f"{the_timestamp}.n1fDrN",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "User-Agent": self.user_agent,
            "Connection": "close",
            "appsiteid": "0",
        }

        if self.x_requested_with:
            the_headers["X-Requested-With"] = self.x_requested_with

        if needs_auth:
            the_headers["Authorization"] = f"Bearer {self.authorization_token}"
        return the_headers

    async def invoke_get(
        self,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        model: Type[BlofinApiResponse] | None = None,
        parse_float=Decimal,
    ) -> "BlofinApiResponse":
        """
        Invokes the specific request to the specific url with the specific params and headers.
        """
        response = await self.httpx_client.get(
            url=url,
            headers=headers,
            params=params,
        )
        return model.deserialize(response.json(parse_float=parse_float))

    async def invoke_post(
        self,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        content: dict | str | bytes = "",
        model: Type[BlofinApiResponse] | None = None,
        parse_float=Decimal,
    ) -> "BlofinApiResponse":
        """
        Invokes the specific request to the specific url with the specific params and headers.
        """

        if isinstance(content, dict):
            content = json.dumps(content, separators=(",", ":"), sort_keys=True)

        response = await self.httpx_client.post(
            url=url,
            headers=headers,
            params=params,
            content=content,
        )
        if not model:
            return response.json()

        return model.deserialize(response.json(parse_float=parse_float))

    async def aclose(self) -> None:
        await self.httpx_client.aclose()
        logger.info("BlofinClient closed")
        return True

    def read_from_session_file(self, file_path: str) -> None:
        """
        Reads from session file; if it doesn't exist, creates it.
        """
        # check if path exists
        target_path = Path(file_path)
        if not target_path.exists():
            return self._save_session_file(file_path=file_path)

        aes = AESCipher(key=f"bf_{self.account_name}_bf", fav_letter=self._fav_letter)
        content = aes.decrypt(target_path.read_text()).decode("utf-8")
        json_data: dict = json.loads(content)

        self.authorization_token = json_data.get(
            "authorization_token",
            self.authorization_token,
        )
        self.timezone = json_data.get("timezone", self.timezone)
        self.user_agent = json_data.get("user_agent", self.user_agent)

    def _save_session_file(self, file_path: str) -> None:
        """
        Saves current information to the session file.
        """

        json_data = {
            "authorization_token": self.authorization_token,
            "timezone": self.timezone,
            "user_agent": self.user_agent,
        }
        aes = AESCipher(key=f"bf_{self.account_name}_bf", fav_letter=self._fav_letter)
        target_path = Path(file_path)
        target_path.write_text(aes.encrypt(json.dumps(json_data)))

    # endregion
    ###########################################################
