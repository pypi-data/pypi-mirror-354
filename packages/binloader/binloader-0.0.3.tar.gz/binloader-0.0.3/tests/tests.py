import time
import subprocess
import unittest


class TestBinaryLoader(unittest.TestCase):
    def _get_cmdline_by_pid(self, pid):
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmd = f.read().replace("\0", " ").strip()
            return cmd

    def _test_cmd(self, cmd):
        p = subprocess.Popen(
            cmd.split(" "),
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )

        assert self._get_cmdline_by_pid(p.pid) == cmd
        p.terminate()
        time.sleep(1)

    def test_local_vim(self):
        cmd = "python binloader/__main__.py --local vim /etc/passwd"
        self._test_cmd(cmd)

    def test_local_busybox(self):
        cmd = "python binloader/__main__.py --local busybox vi /etc/passwd"
        self._test_cmd(cmd)

    def test_remote_vim(self):
        cmd = "python binloader/__main__.py --remote https://github.com/dtschan/vim-static/releases/download/v8.1.1045/vim /etc/passwd"
        self._test_cmd(cmd)

    def test_remote_app_parameter_vim(self):
        cmd = "python binloader/__main__.py --remote https://github.com/dtschan/vim-static/releases/download/v8.1.1045/vim --app vim /etc/passwd"
        self._test_cmd(cmd)

    def test_remote_on_memory_vim(self):
        cmd = "python binloader/__main__.py --remote https://github.com/dtschan/vim-static/releases/download/v8.1.1045/vim --app vim /etc/passwd"
        self._test_cmd(cmd)


if __name__ == "__main__":
    unittest.main()
