import os
import select
import threading
import contextlib
import subprocess
from pathlib import Path

from .. import util, fmf
from . import testcontrol, scripts
from .duration import Duration
from .reporter import Reporter


class TestAbortedError(Exception):
    """
    Raised when an infrastructure-related issue happened while running a test.
    """
    pass


class Executor:
    """
    Logic for running tests on a remote system and processing results
    and uploaded files by those tests.

        tests_repo = "path/to/cloned/tests"
        tests_data = atex.fmf.FMFTests(tests_repo, "/plans/default")

        with Executor(tests_data, conn) as e:
            e.upload_tests(tests_repo)
            e.setup_plan()
            e.run_test("/some/test", "results/here.json", "uploaded/files/here")
            e.run_test(...)

    One Executor instance may be used to run multiple tests sequentially.
    In addition, multiple Executor instances can run in parallel on the same
    host, provided each receives a unique class Connection instance to it.

        conn.cmd(["mkdir", "-p", "/shared"])

        with Executor(tests_data, conn, state_dir="/shared") as e:
            e.upload_tests(tests_repo)
            e.setup_plan()

        # in parallel (ie. threading or multiprocessing)
        with Executor(tests_data, unique_conn, state_dir="/shared") as e:
            e.run_test(...)
    """

    def __init__(self, fmf_tests, connection, *, state_dir=None):
        """
        'fmf_tests' is a class FMFTests instance with (discovered) tests.

        'connection' is a class Connection instance, already fully connected.

        'state_dir' is a string or Path specifying path on the remote system for
        storing additional data, such as tests, execution wrappers, temporary
        plan-exported variables, etc. If left as None, a tmpdir is used.
        """
        self.lock = threading.RLock()
        self.conn = connection
        self.fmf_tests = fmf_tests
        self.state_dir = state_dir
        self.work_dir = None
        self.tests_dir = None
        self.plan_env_file = None
        self.cancelled = False

    def setup(self):
        with self.lock:
            state_dir = self.state_dir

        # if user defined a state dir, have shared tests, but use per-instance
        # work_dir for test wrappers, etc., identified by this instance's id(),
        # which should be unique as long as this instance exists
        if state_dir:
            state_dir = Path(state_dir)
            work_dir = state_dir / f"atex-{id(self)}"
            self.conn.cmd(("mkdir", work_dir), check=True)
            with self.lock:
                self.tests_dir = state_dir / "tests"
                self.plan_env_file = state_dir / "plan_env"
                self.work_dir = work_dir

        # else just create a tmpdir
        else:
            tmp_dir = self.conn.cmd(
                # /var is not cleaned up by bootc, /var/tmp is
                ("mktemp", "-d", "-p", "/var", "atex-XXXXXXXXXX"),
                func=util.subprocess_output,
            )
            tmp_dir = Path(tmp_dir)
            with self.lock:
                self.tests_dir = tmp_dir / "tests"
                self.plan_env_file = tmp_dir / "plan_env"
                # use the tmpdir as work_dir, avoid extra mkdir over conn
                self.work_dir = tmp_dir

    def cleanup(self):
        with self.lock:
            work_dir = self.work_dir

        if work_dir:
            self.conn.cmd(("rm", "-rf", work_dir), check=True)

        with self.lock:
            self.work_dir = None
            self.tests_dir = None
            self.plan_env_file = None

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cancel(self):
        with self.lock:
            self.cancelled = True

    def upload_tests(self):
        """
        Upload a directory of all tests, the location of which was provided to
        __init__() inside 'fmf_tests', to the remote host.
        """
        self.conn.rsync(
            "-rv" if util.in_debug_mode() else "-rq",
            "--delete", "--exclude=.git/",
            f"{self.fmf_tests.root}/",
            f"remote:{self.tests_dir}",
        )

    def setup_plan(self):
        """
        Install packages and run scripts extracted from a TMT plan by a FMFTests
        instance given during class initialization.

        Also prepare additional environment for tests, ie. create and export
        a path to TMT_PLAN_ENVIRONMENT_FILE.
        """
        # install packages from the plan
        if self.fmf_tests.prepare_pkgs:
            self.conn.cmd(
                (
                    "dnf", "-y", "--setopt=install_weak_deps=False",
                    "install", *self.fmf_tests.prepare_pkgs,
                ),
                check=True,
                stdout=None if util.in_debug_mode() else subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )

        # make envionment for 'prepare' scripts
        self.conn.cmd(("truncate", "-s", "0", self.plan_env_file), check=True)
        env = self.fmf_tests.plan_env.copy()
        env["TMT_PLAN_ENVIRONMENT_FILE"] = self.plan_env_file
        env_args = (f"{k}={v}" for k, v in env.items())

        # run the prepare scripts
        for script in self.fmf_tests.prepare_scripts:
            self.conn.cmd(
                ("env", *env_args, "bash"),
                input=script,
                text=True,
                check=True,
                stdout=None if util.in_debug_mode() else subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )

    def run_test(self, test_name, json_file, files_dir, *, env=None):
        """
        Run one test on the remote system.

        'test_name' is a string with test name.

        'json_file' is a destination file (string or Path) for results.

        'files_dir' is a destination dir (string or Path) for uploaded files.

        'env' is a dict of extra environment variables to pass to the test.

        Returns an integer exit code of the test script.
        """
        test_data = self.fmf_tests.tests[test_name]

        # start with fmf-plan-defined environment
        env_vars = self.fmf_tests.plan_env.copy()
        # append fmf-test-defined environment into it
        for item in fmf.listlike(test_data, "environment"):
            env_vars.update(item)
        # append additional variables typically exported by tmt
        env_vars["TMT_PLAN_ENVIRONMENT_FILE"] = self.plan_env_file
        env_vars["TMT_TEST_NAME"] = test_name
        env_vars["ATEX_TEST_NAME"] = test_name
        # append variables given to this function call
        if env:
            env_vars.update(env)

        # run a setup script, preparing wrapper + test scripts
        setup_script = scripts.test_setup(
            test=scripts.Test(test_name, test_data, self.fmf_tests.test_dirs[test_name]),
            tests_dir=self.tests_dir,
            wrapper_exec=f"{self.work_dir}/wrapper.sh",
            test_exec=f"{self.work_dir}/test.sh",
        )
        self.conn.cmd(("bash",), input=setup_script, text=True, check=True)

        with contextlib.ExitStack() as stack:
            reporter = stack.enter_context(Reporter(json_file, files_dir))
            testout_fd = stack.enter_context(reporter.open_tmpfile())
            duration = Duration(test_data.get("duration", "5m"))

            test_proc = None
            control_fd = None
            stack.callback(lambda: os.close(control_fd) if control_fd else None)

            reconnects = 0

            def abort(msg):
                if test_proc:
                    test_proc.kill()
                    test_proc.wait()
                raise TestAbortedError(msg) from None

            try:
                # TODO: probably enum
                state = "starting_test"
                while not duration.out_of_time():
                    with self.lock:
                        if self.cancelled:
                            abort("cancel requested")

                    if state == "starting_test":
                        control_fd, pipe_w = os.pipe()
                        os.set_blocking(control_fd, False)
                        control = testcontrol.TestControl(
                            control_fd=control_fd,
                            reporter=reporter,
                            duration=duration,
                            testout_fd=testout_fd,
                        )
                        # reconnect/reboot count (for compatibility)
                        env_vars["TMT_REBOOT_COUNT"] = str(reconnects)
                        env_vars["TMT_TEST_RESTART_COUNT"] = str(reconnects)
                        # run the test in the background, letting it log output directly to
                        # an opened file (we don't handle it, cmd client sends it to kernel)
                        env_args = (f"{k}={v}" for k, v in env_vars.items())
                        test_proc = self.conn.cmd(
                            ("env", *env_args, f"{self.work_dir}/wrapper.sh"),
                            stdout=pipe_w,
                            stderr=testout_fd,
                            func=util.subprocess_Popen,
                        )
                        os.close(pipe_w)
                        state = "reading_control"

                    elif state == "reading_control":
                        rlist, _, xlist = select.select((control_fd,), (), (control_fd,), 0.1)
                        if xlist:
                            abort(f"got exceptional condition on control_fd {control_fd}")
                        elif rlist:
                            control.process()
                            if control.eof:
                                os.close(control_fd)
                                control_fd = None
                                state = "waiting_for_exit"

                    elif state == "waiting_for_exit":
                        # control stream is EOF and it has nothing for us to read,
                        # we're now just waiting for proc to cleanly terminate
                        try:
                            code = test_proc.wait(0.1)
                            if code == 0:
                                # wrapper exited cleanly, testing is done
                                break
                            else:
                                # unexpected error happened (crash, disconnect, etc.)
                                self.conn.disconnect()
                                # if reconnect was requested, do so, otherwise abort
                                if control.reconnect:
                                    state = "reconnecting"
                                    if control.reconnect != "always":
                                        control.reconnect = None
                                else:
                                    abort(
                                        f"test wrapper unexpectedly exited with {code} and "
                                        "reconnect was not sent via test control",
                                    )
                            test_proc = None
                        except subprocess.TimeoutExpired:
                            pass

                    elif state == "reconnecting":
                        try:
                            self.conn.connect(block=False)
                            reconnects += 1
                            state = "starting_test"
                        except BlockingIOError:
                            pass

                    else:
                        raise AssertionError("reached unexpected state")

                else:
                    abort("test duration timeout reached")

                # testing successful, do post-testing tasks

                # test wrapper hasn't provided exitcode
                if control.exit_code is None:
                    abort("exitcode not reported, wrapper bug?")

                # partial results that were never reported
                if control.partial_results:
                    for result in control.partial_results.values():
                        name = result.get("name")
                        if not name:
                            # partial result is also a result
                            control.nameless_result_seen = True
                        if testout := result.get("testout"):
                            try:
                                reporter.link_tmpfile_to(testout_fd, testout, name)
                            except FileExistsError:
                                raise testcontrol.BadReportJSONError(
                                    f"file '{testout}' already exists",
                                ) from None
                        reporter.report(result)

                # test hasn't reported a result for itself, add an automatic one
                # as specified in RESULTS.md
                # {"status": "pass", "testout": "output.txt"}
                if not control.nameless_result_seen:
                    reporter.link_tmpfile_to(testout_fd, "output.txt")
                    reporter.report({
                        "status": "pass" if control.exit_code == 0 else "fail",
                        "testout": "output.txt",
                    })

                return control.exit_code

            except Exception:
                # if the test hasn't reported a result for itself, but still
                # managed to break something, provide at least the default log
                # for manual investigation - otherwise test output disappears
                if not control.nameless_result_seen:
                    try:
                        reporter.link_tmpfile_to(testout_fd, "output.txt")
                        reporter.report({
                            "status": "infra",
                            "testout": "output.txt",
                        })
                    # in case outout.txt exists as a directory
                    except FileExistsError:
                        pass
                raise


#__all__ = [
#    info.name for info in _pkgutil.iter_modules(__spec__.submodule_search_locations)
#]
#
#
#import importlib as _importlib
#import pkgutil as _pkgutil
#
#
#def __dir__():
#    return __all__
#
#
## lazily import submodules
#def __getattr__(attr):
#    # importing a module known to exist
#    if attr in __all__:
#        return _importlib.import_module(f".{attr}", __name__)
#    else:
#        raise AttributeError(f"module '{__name__}' has no attribute '{attr}'")
