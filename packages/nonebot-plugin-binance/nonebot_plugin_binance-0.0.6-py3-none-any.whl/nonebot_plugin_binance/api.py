# =================================================================
# == nonebot_plugin_binance/api.py
# == 说明：封装所有对Binance API的请求。
# =================================================================
import hmac
import hashlib
import time
import json
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import aiohttp
from loguru import logger
from .auth import AuthManager


class ApiClient:
    BASE_URL = "https://api.binance.com"

    def __init__(self, auth_manager: AuthManager, config):
        self._auth_manager = auth_manager
        self._proxy = config.binance_api_proxy if config.binance_api_proxy else None
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """获取或创建 aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close_session(self):
        """关闭 aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("Aiohttp session closed.")

    def _sign(self, params: Dict[str, Any], secret_key: str) -> str:
        """生成请求签名"""
        query_string = urlencode(params)
        return hmac.new(
            secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    async def _request(
        self, method: str, path: str, user_id: Optional[str] = None, **kwargs
    ):
        """通用请求函数"""
        url = f"{self.BASE_URL}{path}"
        params = kwargs.get("params", {})
        data = kwargs.get("data", {})
        headers = kwargs.get("headers", {})

        if user_id:
            keys = self._auth_manager.get_keys(user_id)
            if not keys:
                return {"error": "用户未绑定或未找到API密钥。"}
            api_key, secret_key = keys
            headers["X-MBX-APIKEY"] = api_key

            # 为需要签名的负载选择 params 或 data
            payload_to_sign = params if method in ["GET", "DELETE"] else data

            payload_to_sign["timestamp"] = int(time.time() * 1000)
            payload_to_sign["signature"] = self._sign(payload_to_sign, secret_key)

            # 因为params和data是可变对象，签名信息已直接添加到其中，无需重新赋值

        session = await self.get_session()
        try:
            # 明确地将处理后的 params, data, 和 headers 传递给请求
            async with session.request(
                method,
                url,
                proxy=self._proxy,
                params=params,
                data=data,
                headers=headers,
            ) as response:
                logger.debug(f"请求: {method} {response.url} | 状态: {response.status}")

                raw_text = await response.text()
                logger.debug(f"API 原始响应文本: '{raw_text}'")

                if not raw_text:
                    logger.warning("API 响应体为空。")
                    return (
                        None
                        if response.status == 200
                        else {"error": "Empty response body"}
                    )

                try:
                    response_data = json.loads(raw_text)
                except json.JSONDecodeError:
                    logger.error(f"JSON 解码失败。 响应文本: {raw_text}")
                    return {"error": "JSON decode error", "data": raw_text}

                if 200 <= response.status < 300:
                    return response_data
                else:
                    logger.error(f"API 错误: {response_data}")
                    return {"error": response_data}
        except aiohttp.ClientError as e:
            logger.error(f"HTTP 请求失败: {e}")
            return {"error": f"请求失败: {e}"}

    # --- 公共端点 ---
    async def get_ping(self):
        return await self._request("GET", "/api/v3/ping")

    async def get_ticker_24hr(self, symbol: str):
        # 此处调用现在可以正确地将 symbol 参数传递给API
        return await self._request(
            "GET", "/api/v3/ticker/24hr", params={"symbol": symbol.upper()}
        )

    async def get_klines(self, symbol: str, interval: str, limit: int = 100):
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
        return await self._request("GET", "/api/v3/klines", params=params)

    # --- 认证端点 ---
    async def get_account_info(self, user_id: str):
        """获取现货账户信息"""
        params = {"omitZeroBalances": "true"}
        return await self._request(
            "GET", "/api/v3/account", user_id=user_id, params=params
        )

    async def post_order(
        self, user_id: str, symbol: str, side: str, order_type: str, **kwargs
    ):
        payload = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
        }
        payload.update(kwargs)
        return await self._request(
            "POST", "/api/v3/order", user_id=user_id, data=payload
        )

    async def get_open_orders(self, user_id: str, symbol: Optional[str] = None):
        params = {}
        if symbol:
            params["symbol"] = symbol.upper()
        return await self._request(
            "GET", "/api/v3/openOrders", user_id=user_id, params=params
        )

    async def cancel_order(self, user_id: str, symbol: str, order_id: int):
        payload = {"symbol": symbol.upper(), "orderId": order_id}
        return await self._request(
            "DELETE", "/api/v3/order", user_id=user_id, data=payload
        )
