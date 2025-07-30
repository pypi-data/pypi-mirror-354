# =================================================================
# == nonebot_plugin_binance/handlers/alert.py
# == 说明：处理价格预警命令。
# =================================================================
import re
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from .. import ws_manager, drawer
from .market import format_symbol

alert_cmd = on_command("bn alert", aliases={"币安预警"}, priority=10, block=True)


@alert_cmd.handle()
async def handle_alert(event: GroupMessageEvent, args: Message = CommandArg()):
    # 预警功能必须在群里设置
    if not isinstance(event, GroupMessageEvent):
        await alert_cmd.finish("价格预警功能请在群聊中使用。")

    arg_text = args.extract_plain_text().strip()
    if not arg_text:
        await alert_cmd.finish(
            "预警命令用法: \n- bn alert add <交易对> <或>价格\n- bn alert list\n- bn alert remove <ID>"
        )

    parts = arg_text.split()
    action = parts[0].lower()

    user_id = event.get_user_id()
    group_id = str(event.group_id)

    if action == "add":
        if len(parts) != 3:
            await alert_cmd.finish(
                "添加预警格式错误！\n用法: bn alert add <交易对> <或>价格\n示例: bn alert add btc-usdt >68000"
            )

        symbol_raw = parts[1]
        condition_price = parts[2]

        # 正则表达式匹配 >, <, >=, <=
        match = re.match(r"([><])=?\s*(\d+\.?\d*)", condition_price)
        if not match:
            await alert_cmd.finish(
                "价格条件格式错误！请使用 '>' 或 '<' 加价格，例如 '>68000'。"
            )

        condition, value_str = match.groups()
        value = float(value_str)
        # websocket stream name is lowercase, but we want to show the user the upper case version
        symbol_upper = format_symbol(symbol_raw).upper()
        symbol_lower = symbol_upper.lower()

        alert_id = await ws_manager.add_alert(
            symbol_lower, user_id, group_id, condition, value
        )
        await alert_cmd.finish(
            f"✅ 预警设置成功！\nID: {alert_id}\n当 {symbol_upper} 价格 {condition} {value} 时，我会 @你。"
        )

    elif action == "list":
        user_alerts = ws_manager.get_user_alerts(user_id)
        if not user_alerts:
            await alert_cmd.finish("您当前没有设置任何价格预警。")

        img = await drawer.draw_alert_list(user_alerts)
        if img:
            await alert_cmd.finish(MessageSegment.image(img))
        else:
            await alert_cmd.finish("生成预警列表图片失败，请检查后台日志。")

    elif action == "remove":
        if len(parts) != 2:
            await alert_cmd.finish("移除预警格式错误！\n用法: bn alert remove <预警ID>")

        alert_id = parts[1]
        if ws_manager.remove_alert(alert_id):
            await alert_cmd.finish(f"✅ 预警 {alert_id} 已成功移除。")
        else:
            # 这里的提示需要模糊一些，因为可能是ID错误，也可能是别人的预警
            await alert_cmd.finish(f"❌ 未找到ID为 {alert_id} 的预警，或它已被触发。")

    else:
        await alert_cmd.finish(
            f"未知的操作 '{action}'。请使用 'add', 'list', 或 'remove'。"
        )
