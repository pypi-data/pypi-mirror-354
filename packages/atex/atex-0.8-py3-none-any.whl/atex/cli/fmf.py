import sys
import pprint

from .. import fmf


def _fatal(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def _get_context(args):
    context = {}
    if args.context:
        for c in args.context:
            key, value = c.split("=", 1)
            context[key] = value
    return context or None


def discover(args):
    result = fmf.FMFTests(args.root, args.plan, context=_get_context(args))
    for name in result.tests:
        print(name)


def show(args):
    result = fmf.FMFTests(args.root, args.plan, context=_get_context(args))
    if tests := list(result.match(args.test)):
        for test in tests:
            print(f"\n--- {test.name} ---")
            pprint.pprint(test.data)
    else:
        _fatal(f"Not reachable via {args.plan} discovery: {args.test}")


def prepare(args):
    result = fmf.FMFTests(args.root, args.plan, context=_get_context(args))
    print("--- fmf root ---")
    print(str(result.root))
    print("--- prepare packages ---")
    print("\n".join(result.prepare_pkgs))
    print("--- plan environment ---")
    print("\n".join("{k}={v}" for k,v in result.plan_env))
    for script in result.prepare_scripts:
        print("--- prepare script ---")
        print(script)
        print("----------------------")


def parse_args(parser):
    parser.add_argument("--root", help="path to directory with fmf tests", default=".")
    parser.add_argument("--context", "-c", help="tmt style key=value context", action="append")
    cmds = parser.add_subparsers(
        dest="_cmd", help="executor feature", metavar="<cmd>", required=True,
    )

    cmd = cmds.add_parser(
        "discover", aliases=("di",),
        help="list tests, post-processed by tmt plans",
    )
    cmd.add_argument("plan", help="tmt plan to use for discovery")

    cmd = cmds.add_parser(
        "show",
        help="show fmf data of a test",
    )
    cmd.add_argument("plan", help="tmt plan to use for discovery")
    cmd.add_argument("test", help="fmf style test regex")

    cmd = cmds.add_parser(
        "prepare",
        help="show prepare-related FMFTests details",
    )
    cmd.add_argument("plan", help="tmt plan to parse")


def main(args):
    if args._cmd in ("discover", "di"):
        discover(args)
    elif args._cmd == "show":
        show(args)
    elif args._cmd == "prepare":
        prepare(args)
    else:
        raise RuntimeError(f"unknown args: {args}")


CLI_SPEC = {
    "help": "simple CLI interface to atex.fmf",
    "args": parse_args,
    "main": main,
}
