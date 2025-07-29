def order_to_one_line(order_info):
    """
    注文情報を1行の文字列にフォーマットする

    Args:
        order_info (dict): convert_order_dataで変換された注文情報
            - datetime_obj: datetimeオブジェクト
            - price: 価格
            - quantity: 数量

    Returns:
        str: フォーマットされた1行の文字列
    """
    time_str = order_info["datetime_obj"].strftime("%Y-%m-%d %H:%M:%S")
    value = f"{int(order_info['price'] * order_info['quantity']):,}"
    return f"[{order_info['long_or_short'].ljust(5)}-{order_info['entry_or_exit'].ljust(5)}] {order_info['symbol']} @{order_info['price']:>6} * {order_info['quantity']:>5} (¥{value:>9}) [{order_info['order_type']}] {time_str}"
