# =================================================================
# == nonebot_plugin_binance/websocket.py
# == 说明：WebSocket管理与价格预警。
# =================================================================
import asyncio
import json
import websockets
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, DefaultDict, Optional
from loguru import logger
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .config import plugin_config


class WebsocketManager:
    BASE_WS_URL = "wss://stream.binance.com:9443/ws"

    def __init__(self, config):
        self._proxy = config.binance_ws_proxy if config.binance_ws_proxy else None
        self._alerts: DefaultDict[str, List[Dict]] = defaultdict(list)
        self._tasks: Dict[str, asyncio.Task] = {}
        self.data_dir = Path(plugin_config.binance_data_path)
        self.alerts_file = self.data_dir / "alerts.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def load_alerts(self):
        """从文件加载预警"""
        if self.alerts_file.exists():
            with open(self.alerts_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for symbol, alerts in data.items():
                        # 确保旧的 triggered 状态被重置
                        for alert in alerts:
                            alert["triggered"] = False
                        self._alerts[symbol] = alerts
                    logger.info(
                        f"从文件成功加载 {sum(len(v) for v in self._alerts.values())} 条预警。"
                    )
                except json.JSONDecodeError:
                    logger.error(f"解码 alerts.json 失败，文件可能已损坏。")

    def _save_alerts(self):
        """保存预警到文件"""
        with open(self.alerts_file, "w", encoding="utf-8") as f:
            json.dump(self._alerts, f, indent=4, ensure_ascii=False)
        logger.info("预警已保存到文件。")

    async def add_alert(
        self, symbol: str, user_id: str, group_id: str, condition: str, value: float
    ) -> str:
        """添加新的价格预警"""
        alert_id = str(uuid.uuid4())[:8]
        self._alerts[symbol.lower()].append(
            {
                "id": alert_id,
                "user_id": user_id,
                "group_id": group_id,
                "condition": condition,  # ">" 或 "<"
                "value": value,
                "symbol": symbol.upper(),  # 保存大写的symbol用于显示
                "triggered": False,
            }
        )
        self._save_alerts()
        # 如果该交易对没有正在运行的ws任务，则启动它
        if symbol.lower() not in self._tasks or self._tasks[symbol.lower()].done():
            await self.start_websocket(symbol.lower())
        return alert_id

    def get_user_alerts(self, user_id: str) -> list:
        """获取指定用户的所有预警"""
        user_alerts = []
        for symbol, alerts in self._alerts.items():
            for alert in alerts:
                if alert["user_id"] == user_id:
                    user_alerts.append({**alert})
        return user_alerts

    def remove_alert(self, alert_id: str) -> bool:
        """
        移除一个预警
        修复: 只有在实际删除了一个元素后才返回 True
        """
        alert_found_and_removed = False
        symbol_to_stop = None
        for symbol, alerts in self._alerts.items():
            initial_len = len(alerts)
            self._alerts[symbol] = [
                alert for alert in alerts if alert["id"] != alert_id
            ]
            if len(self._alerts[symbol]) < initial_len:
                alert_found_and_removed = True
                if not self._alerts[symbol]:
                    symbol_to_stop = symbol
                break  # 找到并删除后即可退出循环

        if symbol_to_stop:
            del self._alerts[symbol_to_stop]
            asyncio.create_task(self.stop_websocket(symbol_to_stop))

        if alert_found_and_removed:
            self._save_alerts()
            return True
        return False

    async def _process_message(self, symbol, message):
        """处理收到的WebSocket消息"""
        data = json.loads(message)
        if "p" in data:  # 这是一个交易流消息
            price = float(data["p"])

            # 使用副本进行迭代，因为我们可能在循环中修改原始列表
            alerts_to_check = list(self._alerts.get(symbol, []))
            for alert in alerts_to_check:
                if alert.get("triggered", False):
                    continue

                condition_met = False
                if alert["condition"] == ">" and price > alert["value"]:
                    condition_met = True
                elif alert["condition"] == "<" and price < alert["value"]:
                    condition_met = True

                if condition_met:
                    logger.info(
                        f"预警触发 {symbol}: 价格 {price} {alert['condition']} {alert['value']}"
                    )
                    # 我们在通知用户后立即移除预警，以避免重复通知
                    await self._notify_user(alert, price)
                    self.remove_alert(alert["id"])

    async def _notify_user(self, alert: dict, price: float):
        """发送通知给用户"""
        try:
            bot = get_bot()
            msg = Message(
                f"[价格预警] {MessageSegment.at(alert['user_id'])}\n您关注的 {alert.get('symbol', '').upper()} 价格已 {alert['condition']} {alert['value']}！\n当前价格: {price}"
            )
            await bot.send_group_msg(group_id=int(alert["group_id"]), message=msg)
        except Exception as e:
            logger.error(f"发送预警通知失败: {e}")

    async def _websocket_client(self, symbol: str):
        """单个交易对的WebSocket客户端，包含自动重连"""
        url = f"{self.BASE_WS_URL}/{symbol}@trade"
        connect_params = {"proxy": self._proxy} if self._proxy else {}

        while symbol in self._alerts:  # 只要这个symbol还有预警，就一直保持连接
            try:
                # websockets.connect 在 v11+ 版本中 proxy 参数是通过 extra_headers 实现的，但更推荐使用 http_proxy 环境变量
                # 为了兼容性，这里我们直接传递 proxy 参数
                async with websockets.connect(url, **connect_params) as ws:
                    logger.info(f"WebSocket 已连接: {symbol}")
                    while symbol in self._alerts:
                        message = await ws.recv()
                        await self._process_message(symbol, message)
            except asyncio.CancelledError:
                logger.info(f"WebSocket 任务被取消: {symbol}")
                break  # 任务被取消，退出循环
            except Exception as e:
                logger.warning(f"WebSocket 连接出错 ({symbol}): {e}. 5秒后重连...")
                await asyncio.sleep(5)
        logger.info(f"WebSocket 已永久停止: {symbol}")

    async def start_websocket(self, symbol: str):
        """启动一个WebSocket连接"""
        if symbol not in self._tasks or self._tasks[symbol].done():
            logger.info(f"正在启动 WebSocket: {symbol}...")
            task = asyncio.create_task(self._websocket_client(symbol))
            self._tasks[symbol] = task

    async def stop_websocket(self, symbol: str):
        """停止一个WebSocket连接"""
        if symbol in self._tasks:
            logger.info(f"正在停止 WebSocket: {symbol}...")
            task = self._tasks.pop(symbol)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass  # 捕获并忽略取消错误

    async def start_all_websockets(self):
        """启动所有需要监控的WebSocket"""
        if not self._alerts:
            logger.info("没有预警需要启动，跳过 WebSocket 连接。")
            return
        logger.info(f"正在为 {len(self._alerts)} 个交易对启动 WebSockets...")
        for symbol in self._alerts.keys():
            await self.start_websocket(symbol)

    async def stop_all_websockets(self):
        """停止所有WebSocket连接"""
        logger.info(f"正在停止所有 {len(self._tasks)} 个 WebSocket 连接...")
        # 创建一个任务列表的副本进行迭代，因为 stop_websocket 会修改 self._tasks
        tasks_to_stop = list(self._tasks.keys())
        for symbol in tasks_to_stop:
            await self.stop_websocket(symbol)
        logger.info("所有 WebSocket 连接已停止。")
