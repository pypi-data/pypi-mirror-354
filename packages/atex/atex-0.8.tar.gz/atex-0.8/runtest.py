#!/usr/bin/python3

import sys
import logging
from pathlib import Path
import tempfile
#import shutil
#import concurrent.futures

from atex import executor, connection, fmf


logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr,
    format="%(asctime)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

fmf_tests = fmf.FMFTests(
#    "/home/jjaburek/gitit/tmt-experiments",
#    "/plans/friday-demo",
    "/home/jjaburek/gitit/contest",
    "/plans/daily",
    context={"distro": "centos-stream-9", "arch": "x86_64"},
)

ssh_options = {
    "User": "root",
    "Hostname": "3.22.208.16",
    "IdentityFile": "/tmp/tmpgwyf9nvn/key_rsa",
}

with connection.ssh.ManagedSSHConn(options=ssh_options) as conn:
    with executor.Executor(fmf_tests, conn) as ex:
        ex.upload_tests()
        ex.setup_plan()
        #for test_name in fmf_tests.tests:
        for test_name in ['/hardening/host-os/oscap/hipaa']:
            tmpdir = tempfile.TemporaryDirectory(dir="/tmp", delete=False)
            files_dir = Path(tmpdir.name) / "files"
            json_file = Path(tmpdir.name) / "json"
            ex.run_test(test_name, json_file, files_dir)


#shutil.rmtree("/tmp/testme")
#Path("/tmp/testme").mkdir()
##print("\n\n------------------\n\n")
#
#with connection.ssh.ManagedSSHConn(options=ssh_options) as conn:
#    conn.cmd(["mkdir", "/var/myatex"])
#    with executor.Executor(fmf_tests, conn, state_dir="/var/myatex") as ex:
#        ex.upload_tests("/home/jjaburek/gitit/tmt-experiments")
#        ex.setup_plan()
#
#
#def run_one():
#    with connection.ssh.ManagedSSHConn(options=ssh_options) as conn:
#        with executor.Executor(fmf_tests, conn, state_dir="/var/myatex") as ex:
#            for test_name in fmf_tests.tests:
#                tmpdir = tempfile.TemporaryDirectory(delete=False, dir="/tmp/testme")
#                files_dir = Path(tmpdir.name) / "files"
#                json_file = Path(tmpdir.name) / "json"
#                ex.run_test(test_name, json_file, files_dir)
#
##print("\n\n------------------\n\n")
#
#with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
#    for _ in range(1):
#        ex.submit(run_one)
#
#with connection.ssh.ManagedSSHConn(options=ssh_options) as conn:
#    conn.cmd(["rm", "-rf", "/var/myatex"])
