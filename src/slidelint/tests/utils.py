from contextlib import contextmanager
from testfixtures import Replacer
import os


@contextmanager
def subprocess_context_helper(temp_dir, cmd):
    config_file = os.path.join(temp_dir.path, 'tmp_file')
    import subprocess
    origing_popen = subprocess.Popen
    with Replacer() as r:
        def not_existing_program(*args, **kwargs):
            return origing_popen(cmd, *args[1:], **kwargs)
        r.replace('subprocess.Popen', not_existing_program)
        yield config_file
