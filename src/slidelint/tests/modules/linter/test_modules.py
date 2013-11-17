from collections import namedtuple

messages_g1_c1 = (
    dict(id='W1010', msg_name='warning-W1010',
         msg='warning message with id W1010', help="full help message"),
    dict(id='C1011', msg_name='critical-C1011',
         msg='warning message with id C1011', help="full help message"))

messages_g1_c2 = (
    dict(id='W1020', msg_name='warning-W1020',
         msg='warning message with id W1020', help="full help message"),
    dict(id='C1021', msg_name='critical-C1021',
         msg='warning message with id C1021', help="full help message"))

messages_g2_c1 = (
    dict(id='W2010', msg_name='warning-W2010',
         msg='warning message with id W2010', help="full help message"),
    dict(id='C2011', msg_name='critical-C2011',
         msg='warning message with id C2011', help="full help message"))


def exeption_raising_func(arg):
    return [1/arg]


def group1_cheker1(target_file=None, msg_info=None, arg1=None, arg2=None):
    messages = messages_g1_c1
    if msg_info:
        rez = messages if msg_info == 'All' \
            else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
        return rez
    return [dict(id='C1011',
                 msg_name='critical-C1011',
                 msg='warning message with id C1011 '
                     'arg1 is "%s"; arg2 is "%s"' % (arg1, arg2),
                 page='2')]


def group1_cheker2(msg_info=None):
    messages = messages_g1_c2
    if msg_info:
        rez = messages if msg_info == 'All' \
            else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
        return rez


def group2_cheker1(target_file=None, msg_info=None):
    messages = messages_g2_c1
    if msg_info:
        rez = messages if msg_info == 'All' \
            else [m for m in messages if m['id'] in msg_info]
        for m in rez:
            m['page'] = ""
        return rez
    return [dict(id='C2011', msg_name='critical-C2011',
                 msg='warning message with id C2011', page='1')]
