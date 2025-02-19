def get_notification_key(notification):
    key_parts = []
    try:
        key_parts.append(notification['tg_user_id'])
        key_parts.append(notification['notification_id'])
        key_parts.append(notification['timestamp'])
    except KeyError:
        return None
    print(key_parts)
    return '_'.join(map(str, key_parts))
