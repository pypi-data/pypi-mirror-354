import argparse
import os
from pathlib import Path
import stat
import urllib.request


def run_local(app, argv):
    """
    Execute binary provided by the library

    Parameters:
    app: str = binary name
    argv: [str] = app's arguments
    on_memory: bool = run the binary from memory
    """
    cur_dir = Path(__file__).resolve().parent

    binaries = {
        "vim": cur_dir / "binaries/vim_amd64",
        "busybox": cur_dir / "binaries/busybox_amd64",
    }
    bin_path = binaries[app]

    bin_path.chmod(bin_path.stat().st_mode | stat.S_IEXEC)
    os.execv(str(bin_path), [app] + argv)


def run_remote(url, app, argv, on_memory):
    """
    Download and execute remote binary

    Parameters:
    url: str = binary's remote location
    app: str = binary name. To be pass as first argument to execv
    argv: [str] = app's arguments
    on_memory: bool = run the binary from memory
    """
    if on_memory and "memfd_create" in os.__dict__:
        mem_f = os.memfd_create("binloader")
        bin_path = f"/proc/self/fd/{mem_f}"
    else:
        bin_path = "/tmp/binloader_remote"

    urllib.request.urlretrieve(url, bin_path)
    path = Path(bin_path)

    path.chmod(stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
    arguments = [app if app else "binloader"] + argv
    os.execv(str(path), arguments)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--local")
    parser.add_argument("-r", "--remote")
    parser.add_argument("-a", "--app")
    parser.add_argument("-m", "--on_memory", action="store_true")
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.local:
        run_local(app=args.local, argv=args.rest)
    elif args.remote:
        run_remote(
            url=args.remote, app=args.app, argv=args.rest, on_memory=args.on_memory
        )
    else:
        print("Invalid option. Use --local/--remote")


if __name__ == "__main__":
    main()
