#!/usr/bin/env python

# pyright: basic, reportUnusedCallResult=false

import atexit
import sys
import os
import tempfile
import signal
import select
import argparse

Position = tuple[int, int]
SpecList = list[tuple[Position, Position]]


def parse_specs(data: str):
    parsed: SpecList = []
    for entry in data.strip().split():
        if not entry or len(entry) < 9:
            continue
        range_part, _ = entry.split("|", 1)
        start_str, end_str = range_part.split(",")
        sl, sc = map(int, start_str.split("."))
        el, ec = map(int, end_str.split("."))
        parsed.append(((sl, sc), (el, ec)))
    return parsed


def is_cursor_in_any(cursor: Position, diagnostics: SpecList) -> bool:
    cl, cc = cursor
    for (sl, sc), (el, ec) in diagnostics:
        if cl < sl or cl > el:
            continue
        if sl == el:
            if cl == sl and sc <= cc <= ec:
                return True
        elif cl == sl:
            if cc >= sc:
                return True
        elif cl == el:
            if cc <= ec:
                return True
        elif sl < cl < el:
            return True
    return False


def cleanup(inp: str, outp: str, dir: str):
    try:
        os.remove(inp)
        os.remove(outp)
        os.rmdir(dir)
    except FileNotFoundError:
        pass


def get_static_output() -> str:
    static = """\
define-command lsp-diag-set %{
    evaluate-commands %sh{
        {
            printf 'set %s\\n' "$kak_opt_lsp_inline_diagnostics" >"$kak_opt_diagpipe_in"
            read result < "$kak_opt_diagpipe_out"
            if [ "$result" != "ok" ]; then
                cmd=$(printf "eval -try-client '$kak_client' -verbatim info -title lsp-diag 'failed to parse diagnostics'")
                echo "$cmd" | kak -p ${kak_session}
            fi
        } </dev/null >/dev/null 2>&1 &
    }
}

define-command -params 2 lsp-diag-query %{
    evaluate-commands %sh{
        printf 'query %s %s\\n' "$1" "$2" >"$kak_opt_diagpipe_in"
        read result < "$kak_opt_diagpipe_out"
        if [ "$result" = "true" ]; then
            echo "trigger-user-hook lsp-diag-hover-true"
        else
            echo "trigger-user-hook lsp-diag-hover-false"
        fi
    }
}

hook global KakEnd .* %{
    nop %sh{
        printf 'exit\\n' >"$kak_opt_diagpipe_in"
        read result < "$kak_opt_diagpipe_out"
    }
}

define-command lsp-diag-hover-enable %{
    lsp-diag-set

    hook -group lsp-diag window User lsp-diag-hover-false %{
        lsp-inlay-diagnostics-disable
    }

    hook -group lsp-diag window User lsp-diag-hover-true %{
        lsp-inlay-diagnostics-enable
    }
    hook -group lsp-diag window NormalIdle .* %{
        lsp-diag-query %val{cursor_line} %val{cursor_column}
    }
    hook -group lsp-diag window WinSetOption lsp_inline_diagnostics=.* %{
        lsp-diag-set
    }
}
define-command lsp-diag-hover-disable %{
    remove-hooks window lsp-diag
}
    """
    return static


def gen_kakoune_output(inp: str, outp: str, print_static: bool) -> str:
    out_l = [
        f"declare-option -hidden str diagpipe_in {inp}",
        f"declare-option -hidden str diagpipe_out {outp}",
    ]
    if print_static:
        out_l.append(get_static_output())
    out = "\n".join(out_l)
    return out


def daemonize(inp: str, outp: str, dir: str):
    # fork and exit parent
    if os.fork() > 0:
        sys.exit(0)
    # new session
    os.setsid()
    if os.fork() > 0:
        # exit first child
        sys.exit(0)

    # redirect IO to /dev/null
    with open("/dev/null", "rb", 0) as dn:
        os.dup2(dn.fileno(), sys.stdin.fileno())
    with open("/dev/null", "ab", 0) as dn:
        os.dup2(dn.fileno(), sys.stdout.fileno())
        os.dup2(dn.fileno(), sys.stderr.fileno())
    _ = atexit.register(lambda: cleanup(inp, outp, dir))

    def on_exit(*_):
        # cleanup(inp, outp, dir)
        sys.exit(0)

    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)


def main():
    parser = argparse.ArgumentParser(
        description="LSP diagnostic hover plugin for Kakoune.",
        epilog="""
Author : Daniel Fichtinger
License: ISC
Contact: daniel@ficd.ca
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--no-static",
        required=False,
        help="Don't output the contents of static.kak for evaluation. Useful if you want to change the commands yourself.",
        action="store_false",
    )
    parser.add_argument(
        "--print-static",
        required=False,
        help="Output the contents of static.kak but don't start daemon.",
        action="store_true",
    )
    args = parser.parse_args()
    print_static: bool = args.no_static
    dry_run: bool = args.print_static
    if dry_run:
        print(get_static_output())
        sys.exit(0)
    # create unique directory and names
    fifo_dir = tempfile.mkdtemp(prefix="diagpipe-")
    in_path = os.path.join(fifo_dir, "in")
    out_path = os.path.join(fifo_dir, "out")

    # create fifos
    os.mkfifo(in_path)
    os.mkfifo(out_path)

    read_fd = os.open(in_path, os.O_RDONLY | os.O_NONBLOCK)
    infile = os.fdopen(read_fd, "r", buffering=1)

    _dummy = os.open(out_path, os.O_RDONLY | os.O_NONBLOCK)

    write_fd = os.open(out_path, os.O_WRONLY | os.O_NONBLOCK)
    outfile = os.fdopen(write_fd, "w", buffering=1)

    def cleanup_fifos():
        try:
            infile.close()
        except Exception:
            pass
        try:
            outfile.close()
        except Exception:
            pass

    atexit.register(cleanup_fifos)

    output = gen_kakoune_output(in_path, out_path, print_static)
    print(output)
    sys.stdout.flush()
    daemonize(in_path, out_path, fifo_dir)

    diagnostics: SpecList = []
    while True:
        rlist, _, _ = select.select([infile], [], [])
        if rlist:
            line = infile.readline()
            if not line:
                continue
            line = line.strip()
            assert isinstance(line, str)
            if line.startswith("set "):
                _, payload = line.split(" ", 1)
                diagnostics = parse_specs(payload)
                try:
                    outfile.write("ok\n")
                    outfile.flush()
                except BrokenPipeError:
                    pass
            elif line.startswith("query "):
                _, pos = line.split(" ", 1)
                l, c = map(int, pos.strip().split())
                result = is_cursor_in_any((l, c), diagnostics)
                _ = outfile.write("true\n" if result else "false\n")
                outfile.flush()
            elif line.startswith("exit"):
                sys.exit(0)
            elif line.startswith("ping"):
                outfile.write("pong\n")
                outfile.flush()


if __name__ == "__main__":
    main()
