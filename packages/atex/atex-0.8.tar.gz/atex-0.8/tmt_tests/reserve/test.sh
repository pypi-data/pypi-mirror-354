#!/bin/bash

set -e -x

# always reboot into the same OS entry (unless otherwise overriden)
#
# we're executing efibootmgr here instead of just checking its existence
# because some systems have the binary, but, when run, it fails with:
#   EFI variables are not supported on this system.
if efibootmgr &>/dev/null; then
    current=$(efibootmgr | sed -n 's/^BootCurrent: //p')
    efibootmgr -n "$current"
fi

# no-op on second/third/etc. execution
if [[ $TMT_TEST_RESTART_COUNT && $TMT_TEST_RESTART_COUNT -gt 0 ]]; then
    exec sleep inf
    exit 1
fi

# remove tmt-related commands
# (if running tmt via 'provision -h connect', tmt will upload its own)
rm -f /usr/local/bin/{tmt,rstrnt,rhts}-*

if [[ ! -e /run/ostree-booted ]]; then
    # remove useless daemons to free up RAM a bit
    dnf remove -y rng-tools irqbalance

    # clean up packages from extra repos, restoring original vanilla OS (sorta)
    rm -v -f \
        /etc/yum.repos.d/{tag-repository,*beakerlib*,rcmtools}.repo \
        /etc/yum.repos.d/beaker-{client,harness,tasks}.repo
    # downgrade any packages installed/upgraded from the extra package repos
    function list_foreign_rpms {
        dnf list --installed \
        | grep -e @koji-override -e @testing-farm -e @epel -e @copr: -e @rcmtools \
        | sed 's/ .*//'
    }
    rpms=$(list_foreign_rpms)
    [[ $rpms ]] && dnf downgrade -y --skip-broken $rpms || true
    rpms=$(list_foreign_rpms)
    [[ $rpms ]] && dnf remove -y --noautoremove $rpms
    dnf clean all
fi

# install SSH key
if [[ $RESERVE_SSH_PUBKEY ]]; then
    mkdir -p ~/.ssh
    chmod 0700 ~/.ssh
    echo "$RESERVE_SSH_PUBKEY" >> ~/.ssh/authorized_keys
    chmod 0600 ~/.ssh/authorized_keys
else
    echo "RESERVE_SSH_PUBKEY env var not defined" >&2
    exit 1
fi

exec sleep inf
exit 1  # fallback
