#!/usr/bin/python3

import time
import sys
import logging
import concurrent.futures
from atex.provision.testingfarm import TestingFarmProvisioner


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

p = TestingFarmProvisioner("CentOS-Stream-9", arch="s390x", max_systems=2, max_retries=1)

try:
    p.start()
    print(f"first get_remote; reserving={p.reserving} ; remotes={p.remotes}")
    #while True:
    #    time.sleep(10)
    #    print("trying get_remote()")
    #    rem = p.get_remote(block=False)
    #    if rem:
    #        break
    rem = p.get_remote()
    rem.cmd(["touch", "/foo"], check=True)
    rem.cmd(["ls", "/"], check=True)
    #p.relinquish(rem)
    print(f"second get_remote; reserving={p.reserving} ; remotes={p.remotes}")
    rem2 = p.get_remote()
    rem2.cmd(["ls", "/"], check=True)
    rem.release()
    rem2.release()
    print(f"third get_remote; reserving={p.reserving} ; remotes={p.remotes}")
    rem3 = p.get_remote()
    rem3.cmd(["ls", "/"], check=True)
    rem3.release()
    print("\n\nsleep 30\n\n")
    time.sleep(30)
    raise AssertionError("foobar")
    #p.relinquish(rem)
    print("fourth get_remote")
    rem4 = p.get_remote()
    rem4.cmd(["ls", "/"], check=True)
finally:
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        for f in p.stop_defer():
            ex.submit(f)
