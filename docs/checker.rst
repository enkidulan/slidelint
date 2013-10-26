
C2000-2300 - lingvo tool
W1001 - contents
C1002 - fontsize
C1003 - danger zone
C3000 - readability
W4000 - regexp



Writing a checker
=================

Checker is a function that will be called at least with two arguments during the
checking process. This required argument is target_file and msg_info.

::

    from slidelint.utils import help

    messages = (
        dict(id='01000',
             msg_name='msg-name',
             msg='Message',
             help="Message help"),)

    def main(target_file=None, msg_info=None, custom_arg='default_value'):
        if msg_info:
            return help(messages, msg_info)
        return some_check(target_file, custom_arg)
