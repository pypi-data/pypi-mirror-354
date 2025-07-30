# =================================================================
# == nonebot_plugin_binance/handlers/trade.py
# == 说明：处理交易和资产查询命令。
# =================================================================
import asyncio
from typing import Any
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment
from loguru import logger
from .. import drawer, api_client, auth_manager
from .market import format_symbol

balance_cmd = on_command(
    "bn balance", aliases={"bn bal", "币安资产"}, priority=10, block=True
)
order_cmd = on_command("bn order", aliases={"币安下单"}, priority=10, block=True)
open_orders_cmd = on_command("bn open", aliases={"币安挂单"}, priority=10, block=True)
cancel_cmd = on_command("bn cancel", aliases={"币安撤单"}, priority=10, block=True)


def get_error_message(data: Any) -> str:
    """从API返回的数据中安全地提取错误信息"""
    if isinstance(data, dict):
        error_content = data.get("error", "未知字典格式错误")
        if isinstance(error_content, dict):
            return error_content.get("msg", str(error_content))
        return str(error_content)
    elif isinstance(data, str):
        return data
    return "未知的错误类型"


@balance_cmd.handle()
async def handle_balance(event: Event):
    user_id = event.get_user_id()
    if not auth_manager.get_keys(user_id):
        await balance_cmd.finish(
            "请先私聊我绑定API Key: bn bind [API Key] [Secret Key]"
        )

    await balance_cmd.send("正在查询您的现货账户资产...")
    data = await api_client.get_account_info(user_id)

    logger.debug(f"现货账户API原始响应 (用户: {user_id}): {data}")

    if isinstance(data, dict) and "balances" in data:
        balances_list = data["balances"]
        if isinstance(balances_list, list):
            processed_balances = []

            cache_tasks = []
            assets_to_process = []

            for b in balances_list:
                if isinstance(b, dict):
                    assets_to_process.append(b)
                    # 为每个资产创建一个图标缓存/下载任务
                    task = drawer.image_cache.get_icon_path(b.get("asset", ""))
                    cache_tasks.append(task)

            # 并发执行所有图标的下载/缓存任务
            if cache_tasks:
                logger.info(f"正在为 {len(cache_tasks)} 个资产准备图标...")
                icon_paths = await asyncio.gather(*cache_tasks)
            else:
                icon_paths = []

            # 将资产数据和已获取的图标路径结合起来
            for i, b in enumerate(assets_to_process):
                try:
                    free_val = float(b.get("free", 0))
                    locked_val = float(b.get("locked", 0))
                except (ValueError, TypeError):
                    logger.warning(f"无法解析资产数据: {b}")
                    continue

                total_val = free_val + locked_val
                processed_balances.append(
                    {
                        "asset": b.get("asset"),
                        "free": f"{free_val:.8f}".rstrip("0").rstrip(".") or "0",
                        "locked": f"{locked_val:.8f}".rstrip("0").rstrip(".") or "0",
                        "total": f"{total_val:.8f}".rstrip("0").rstrip(".") or "0",
                        "icon_path": icon_paths[i],  # 添加已缓存的图标路径
                    }
                )

            processed_balances.sort(key=lambda x: x["asset"])
            logger.debug(f"处理后用于渲染的现货资产数据: {processed_balances}")

            template_data = {"balances": processed_balances}
            img = await drawer.draw_balance(template_data)
            if img:
                await balance_cmd.finish(MessageSegment.image(img))
            else:
                await balance_cmd.finish("生成资产图片失败，请检查后台日志。")
        else:
            await balance_cmd.finish("资产查询失败：API返回数据格式异常。")
    else:
        error_msg = get_error_message(data)
        logger.error(f"现货资产查询失败 (用户: {user_id}): {error_msg}")
        await balance_cmd.finish(f"资产查询失败: {error_msg}")


@open_orders_cmd.handle()
async def handle_open_orders(event: Event, args: Message = CommandArg()):
    user_id = event.get_user_id()
    if not auth_manager.get_keys(user_id):
        await open_orders_cmd.finish(
            "请先私聊我绑定API Key: bn bind [API Key] [Secret Key]"
        )

    symbol = args.extract_plain_text().strip()
    formatted_symbol = format_symbol(symbol) if symbol else None

    await open_orders_cmd.send(
        f"正在查询 {'全部' if not formatted_symbol else formatted_symbol} 挂单..."
    )
    data = await api_client.get_open_orders(user_id, formatted_symbol)

    if isinstance(data, list):
        if not data:
            await open_orders_cmd.finish(
                f"没有找到 {'该交易对的' if formatted_symbol else ''} 当前挂单。"
            )
            return
        img = await drawer.draw_orders(data, "当前挂单")
        if img:
            await open_orders_cmd.finish(MessageSegment.image(img))
        else:
            await open_orders_cmd.finish("生成挂单列表图片失败，请检查后台日志。")
    else:
        error_msg = get_error_message(data)
        await open_orders_cmd.finish(f"查询挂单失败: {error_msg}")


@cancel_cmd.handle()
async def handle_cancel_order(event: Event, args: Message = CommandArg()):
    user_id = event.get_user_id()
    if not auth_manager.get_keys(user_id):
        await cancel_cmd.finish("请先私聊我绑定API Key: bn bind [API Key] [Secret Key]")

    arg_text = args.extract_plain_text().strip()
    if not arg_text:
        await cancel_cmd.finish("参数不足。用法: bn cancel <交易对> <订单ID>")

    parts = arg_text.split()
    if len(parts) != 2:
        await cancel_cmd.finish("参数格式错误。用法: bn cancel <交易对> <订单ID>")

    symbol, order_id_str = parts
    if not order_id_str.isdigit():
        await cancel_cmd.finish("订单ID必须是数字。")

    formatted_symbol = format_symbol(symbol)
    order_id = int(order_id_str)

    await cancel_cmd.send(f"正在尝试撤销 {formatted_symbol} 的订单 {order_id}...")
    data = await api_client.cancel_order(user_id, formatted_symbol, order_id)

    if isinstance(data, dict) and "error" not in data:
        await cancel_cmd.finish(f"✅ 订单 {data.get('orderId')} 已成功撤销。")
    else:
        error_msg = get_error_message(data)
        await cancel_cmd.finish(f"❌ 撤单失败: {error_msg}")


@order_cmd.handle()
async def handle_order(event: Event, args: Message = CommandArg()):
    await order_cmd.finish(
        "下单功能暂未开放，以防止误操作造成损失。如有需要请自行修改代码。"
    )
