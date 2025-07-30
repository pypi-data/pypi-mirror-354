# =================================================================
# == nonebot_plugin_binance/handlers/market.py
# == 说明：处理行情查询命令。
# =================================================================
import json
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .. import drawer, api_client

# 已知的所有指令或别名，用于防止快捷指令冲突
KNOWN_COMMANDS = {
    # system.py
    "help",
    "币安帮助",
    "bind",
    "币安绑定",
    "unbind",
    "币安解绑",
    "status",
    "币安状态",
    # market.py
    "price",
    "p",
    "币安价格",
    "kline",
    "k",
    "币安K线",
    # trade.py
    "balance",
    "bal",
    "币安资产",
    "order",
    "币安下单",
    "open",
    "币安挂单",
    "cancel",
    "币安撤单",
    # alert.py
    "alert",
    "币安预警",
}


def format_symbol(raw_symbol: str) -> str:
    """格式化交易对，例如 btc-usdt -> BTCUSDT"""
    return raw_symbol.replace("-", "").replace("/", "").upper()


price_cmd = on_command(
    "bn price", aliases={"bn p", "币安价格"}, priority=10, block=True
)
kline_cmd = on_command("bn kline", aliases={"bn k", "币安K线"}, priority=10, block=True)
# 新增一个低优先级的命令处理器，用于快捷查询
bn_shortcut_cmd = on_command("bn", priority=15, block=True)


@price_cmd.handle()
async def handle_price(args: Message = CommandArg()):
    symbol = args.extract_plain_text().strip()
    if not symbol:
        await price_cmd.finish("请输入要查询的交易对，例如：bn price btc-usdt")

    formatted_symbol = format_symbol(symbol)
    await price_cmd.send(f"正在查询 {formatted_symbol} 的最新行情...")
    data = await api_client.get_ticker_24hr(formatted_symbol)

    if isinstance(data, dict) and "symbol" in data:
        img = await drawer.draw_ticker(data)
        if img:
            await price_cmd.finish(MessageSegment.image(img))
        else:
            await price_cmd.finish("生成行情图片失败，请检查后台日志。")
    else:
        error_msg = "未知错误"
        if isinstance(data, dict):
            error_content = data.get("error", data)
            if isinstance(error_content, dict):
                error_msg = error_content.get("msg", json.dumps(error_content))
            else:
                error_msg = str(error_content)
        elif data is not None:
            error_msg = str(data)

        await price_cmd.finish(
            f"查询失败，请检查交易对 '{symbol}' 是否正确。\n错误: {error_msg}"
        )


@kline_cmd.handle()
async def handle_kline(args: Message = CommandArg()):
    arg_text = args.extract_plain_text().strip()
    if not arg_text:
        await kline_cmd.finish("请输入交易对。例如: `bn k btc-usdt 1h` 或 `bn k btc`")

    parts = arg_text.split()
    symbol_arg = parts[0]

    # 快捷指令: bn k btc -> bn k btc-usdt 1d
    if len(parts) == 1 and "-" not in symbol_arg and "/" not in symbol_arg:
        symbol = f"{symbol_arg}-usdt"
        interval = "1d"
    else:
        # 标准指令: bn k <交易对> [周期]
        symbol = symbol_arg
        interval = parts[1].lower() if len(parts) > 1 else "4h"

    valid_intervals = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]
    if interval not in valid_intervals:
        await kline_cmd.finish(
            f"无效的K线周期 '{interval}'。\n支持的周期: {', '.join(valid_intervals)}"
        )

    formatted_symbol = format_symbol(symbol)
    await kline_cmd.send(f"正在获取 {formatted_symbol} ({interval}) 的K线数据...")
    data = await api_client.get_klines(formatted_symbol, interval)

    if isinstance(data, list) and len(data) > 0:
        img = await drawer.draw_kline(data, formatted_symbol, interval)
        if img:
            await kline_cmd.finish(MessageSegment.image(img))
        else:
            await kline_cmd.finish("生成K线图失败，请检查后台日志。")
    else:
        await kline_cmd.finish(
            f"无法获取 {symbol} 的K线数据，请检查交易对是否正确或该周期是否有数据。"
        )


@bn_shortcut_cmd.handle()
async def handle_bn_main_shortcut(args: Message = CommandArg()):
    """
    处理 `bn <货币名>` 形式的快捷指令。
    """
    arg_text = args.extract_plain_text().strip()

    # 此处理器只处理单参数情况，且该参数不是一个已知指令
    if " " in arg_text or not arg_text or arg_text.lower() in KNOWN_COMMANDS:
        await bn_shortcut_cmd.finish()  # 交给其他处理器
        return

    # 认为是快捷价格查询
    symbol = f"{arg_text}-usdt"
    formatted_symbol = format_symbol(symbol)

    await bn_shortcut_cmd.send(f"正在查询 {formatted_symbol} 的最新行情...")
    data = await api_client.get_ticker_24hr(formatted_symbol)

    if isinstance(data, dict) and "symbol" in data:
        img = await drawer.draw_ticker(data)
        if img:
            await bn_shortcut_cmd.finish(MessageSegment.image(img))
        else:
            await bn_shortcut_cmd.finish("生成行情图片失败，请检查后台日志。")
    else:
        # 如果查询失败（例如，无效的货币名），则静默失败，
        # 避免用户输错其他指令时（如 bn helo）弹出不相关的错误。
        await bn_shortcut_cmd.finish()
