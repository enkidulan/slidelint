def help(messages, msg_ids):
    rez = list(messages) if msg_ids == 'All'else \
        [m for m in messages if m['id'] in msg_ids]
    for m in rez:
        m['page'] = ""
        m['msg'] = m['help']
    return rez
