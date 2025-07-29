import time
import tempfile
import traceback
import concurrent
import collections
from pathlib import Path

from .. import util, executor


class Orchestrator:
    """
    A scheduler for parallel execution on multiple resources (machines/systems).
    """

    SetupInfo = collections.namedtuple(
        "SetupInfo",
        (
            # class Provisioner instance this machine is provided by
            # (for logging purposes)
            "provisioner",
            # class Remote instance returned by the Provisioner
            "remote",
            # class Executor instance uploading tests / running setup or tests
            "executor",
        ),
    )
    RunningInfo = collections.namedtuple(
        "RunningInfo",
        (
            # "inherit" from SetupInfo
            *SetupInfo._fields,
            # string with /test/name
            "test_name",
            # class tempfile.TemporaryDirectory instance with 'json_file' and 'files_dir'
            "tmp_dir",
        ),
    )
    FinishedInfo = collections.namedtuple(
        "FinishedInfo",
        (
            # "inherit" from RunningInfo
            *RunningInfo._fields,
            # integer with exit code of the test
            # (None if exception happened)
            "exit_code",
            # exception class instance if running the test failed
            # (None if no exception happened (exit_code is defined))
            "exception",
        ),
    )

    def __init__(self, platform, fmf_tests, provisioners, aggregator, tmp_dir, *, max_reruns=2):
        """
        'platform' is a string with platform name.

        'fmf_tests' is a class FMFTests instance of the tests to run.

        'provisioners' is an iterable of class Provisioner instances.

        'aggregator' is a class CSVAggregator instance.

        'tmp_dir' is a string/Path to a temporary directory, to be used for
        storing per-test results and uploaded files before being ingested
        by the aggregator. Can be safely shared by Orchestrator instances.
        """
        self.platform = platform
        self.fmf_tests = fmf_tests
        self.provisioners = tuple(provisioners)
        self.aggregator = aggregator
        self.tmp_dir = tmp_dir
        # tests still waiting to be run
        self.to_run = set(fmf_tests.tests)
        # running setup functions, as a list of SetupInfo items
        self.running_setups = []
        # running tests as a dict, indexed by test name, with RunningInfo values
        self.running_tests = {}
        # indexed by test name, value being integer of how many times
        self.reruns = collections.defaultdict(lambda: max_reruns)
        # thread queue for actively running tests
        self.test_queue = util.ThreadQueue(daemon=False)
        # thread queue for remotes being set up (uploading tests, etc.)
        self.setup_queue = util.ThreadQueue(daemon=True)
        # NOTE: running_setups and test_running are just for debugging and
        #       cancellation, the execution flow itself uses ThreadQueues

    @staticmethod
    def _run_setup(sinfo):
        sinfo.executor.setup()
        sinfo.executor.upload_tests()
        sinfo.executor.setup_plan()
        # NOTE: we never run executor.cleanup() anywhere - instead, we assume
        #       the remote (and its connection) was invalidated by the test,
        #       so we just rely on remote.release() destroying the system
        return sinfo

    @classmethod
    def _wrap_test(cls, rinfo, func, *args, **kwargs):
        """
        Wrap 'func' (test execution function) to preserve extra metadata
        ('rinfo') and return it with the function return value.
        """
        try:
            return cls.FinishedInfo(*rinfo, func(*args, **kwargs), None)
        except Exception as e:
            return cls.FinishedInfo(*rinfo, None, e)

    def _run_new_test(self, sinfo):
        """
        'sinfo' is a SetupInfo instance.
        """
        next_test_name = self.next_test(self.to_run, self.fmf_tests)
        assert next_test_name in self.to_run, "next_test() returned valid test name"

        self.to_run.remove(next_test_name)

        rinfo = self.RunningInfo(
            *sinfo,
            test_name=next_test_name,
            tmp_dir=tempfile.TemporaryDirectory(
                prefix=next_test_name.strip("/").replace("/","-") + "-",
                dir=self.tmp_dir,
                delete=False,
            ),
        )

        tmp_dir_path = Path(rinfo.tmp_dir.name)
        self.test_queue.start_thread(
            target=self._wrap_test,
            args=(
                rinfo,
                sinfo.executor.run_test,
                next_test_name,
                tmp_dir_path / "json_file",
                tmp_dir_path / "files_dir",
            ),
        )

        self.running_tests[next_test_name] = rinfo

    def _process_finished_test(self, finfo):
        """
        'finfo' is a FinishedInfo instance.
        """
        test_id = f"'{finfo.test_name}' on '{finfo.remote}'"
        tmp_dir_path = Path(finfo.tmp_dir.name)

        # NOTE: document that we intentionally don't .cleanup() executioner below,
        #       we rely on remote .release() destroying the OS, because we don't
        #       want to risk .cleanup() blocking on dead ssh into the remote after
        #       executing a destructive test

        destructive = False

        # if executor (or test) threw exception, schedule a re-run
        if finfo.exception:
            destructive = True
            exc_str = "".join(traceback.format_exception(finfo.exception)).rstrip("\n")
            util.info(f"unexpected exception happened while running {test_id}:\n{exc_str}")
            finfo.remote.release()
            if self.reruns[finfo.test_name] > 0:
                self.reruns[finfo.test_name] -= 1
                self.to_run.add(finfo.test_name)
            else:
                util.info(f"reruns for {test_id} exceeded, ignoring it")

        # if the test exited as non-0, try a re-run
        elif finfo.exit_code != 0:
            destructive = True
            finfo.remote.release()
            if self.reruns[finfo.test_name] > 0:
                util.info(
                    f"{test_id} exited with non-zero: {finfo.exit_code}, re-running "
                    f"({self.reruns[finfo.test_name]} reruns left)",
                )
                self.reruns[finfo.test_name] -= 1
                self.to_run.add(finfo.test_name)
            else:
                util.info(
                    f"{test_id} exited with non-zero: {finfo.exit_code}, "
                    "all reruns exceeded, giving up",
                )
                # record the final result anyway
                self.aggregator.ingest(
                    self.platform,
                    finfo.test_name,
                    tmp_dir_path / "json_file",
                    tmp_dir_path / "files_dir",
                )
                finfo.tmp_dir.cleanup()

        # test finished successfully - ingest its results
        else:
            util.info(f"{test_id} finished successfully")
            self.aggregator.ingest(
                self.platform,
                finfo.test_name,
                tmp_dir_path / "json_file",
                tmp_dir_path / "files_dir",
            )
            finfo.tmp_dir.cleanup()

        # if the remote was not destroyed by traceback / failing test,
        # check if the test always destroys it (even on success)
        if not destructive:
            test_data = self.fmf_tests.tests[finfo.test_name]
            destructive = test_data.get("extra-atex", {}).get("destructive", False)

        # if destroyed, release the remote
        if destructive:
            util.debug(f"{test_id} was destructive, releasing remote")
            finfo.remote.release()

        # if still not destroyed, run another test on it
        # (without running plan setup, re-using already set up remote)
        elif self.to_run:
            sinfo = self.SetupInfo(
                provisioner=finfo.provisioner,
                remote=finfo.remote,
                executor=finfo.executor,
            )
            util.debug(f"{test_id} was non-destructive, running next test")
            self._run_new_test(sinfo)

    def serve_once(self):
        """
        Run the orchestration logic, processing any outstanding requests
        (for provisioning, new test execution, etc.) and returning once these
        are taken care of.

        Returns True to indicate that it should be called again by the user
        (more work to be done), False once all testing is concluded.
        """
        util.debug(
            f"to_run: {len(self.to_run)} tests / "
            f"running: {len(self.running_tests)} tests, {len(self.running_setups)} setups",
        )
        # all done
        if not self.to_run and not self.running_tests:
            return False

        # process all finished tests, potentially reusing remotes for executing
        # further tests
        while True:
            try:
                finfo = self.test_queue.get(block=False)
            except util.ThreadQueue.Empty:
                break
            del self.running_tests[finfo.test_name]
            self._process_finished_test(finfo)

        # process any remotes with finished plan setup (uploaded tests,
        # plan-defined pkgs / prepare scripts), start executing tests on them
        while True:
            try:
                sinfo = self.setup_queue.get(block=False)
            except util.ThreadQueue.Empty:
                break
            util.debug(f"setup finished for '{sinfo.remote}', running first test")
            self.running_setups.remove(sinfo)
            self._run_new_test(sinfo)

        # try to get new remotes from Provisioners - if we get some, start
        # running setup on them
        for provisioner in self.provisioners:
            while (remote := provisioner.get_remote(block=False)) is not None:
                ex = executor.Executor(self.fmf_tests, remote)
                sinfo = self.SetupInfo(
                    provisioner=provisioner,
                    remote=remote,
                    executor=ex,
                )
                self.setup_queue.start_thread(
                    target=self._run_setup,
                    args=(sinfo,),
                )
                self.running_setups.append(sinfo)
                util.debug(f"got remote '{remote}' from '{provisioner}', running setup")

        return True

    def serve_forever(self):
        """
        Run the orchestration logic, blocking until all testing is concluded.
        """
        while self.serve_once():
            time.sleep(1)

    def __enter__(self):
        # start all provisioners
        for prov in self.provisioners:
            prov.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # cancel all running tests and wait for them to clean up (up to 0.1sec)
        for rinfo in self.running_tests.values():
            rinfo.executor.cancel()
        self.test_queue.join()  # also ignore any exceptions raised

        # stop all provisioners, also releasing all remotes
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            for provisioner in self.provisioners:
                for func in provisioner.stop_defer():
                    ex.submit(func)

    def next_test(self, tests, fmf_tests):  # noqa: ARG002, PLR6301
        """
        Return a test name (string) from a set of 'tests' (set of test name
        strings) to be run next.

        'fmf_tests' is a class FMFTests instance with additional test metadata.

        This method is user-overridable, ie. by subclassing Orchestrator:

            class CustomOrchestrator(Orchestrator):
                @staticmethod
                def next_test(tests):
                    ...
        """
        # TODO: more advanced algorithm
        #
        # simple:
        return next(iter(tests))
