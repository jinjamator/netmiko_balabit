"""Balabit SCB driver."""
from typing import Any
import logging
import paramiko
from netmiko.linux import LinuxSSH

from typing import (
    Optional,
    Callable,
    Any,
    List,
    Dict,
    TypeVar,
    cast,
    Type,
    Sequence,
    Iterator,
    TextIO,
    Union,
    Tuple,
    Deque,
)


class SecretsFilter(logging.Filter):
    def __init__(self, no_log: Optional[Dict[Any, str]] = None) -> None:
        self.no_log = no_log

    def filter(self, record: logging.LogRecord) -> bool:
        """Removes secrets (no_log) from messages"""
        if self.no_log:
            for hidden_data in self.no_log.values():
                if isinstance(hidden_data, list):
                    for item in hidden_data:
                        record.msg = record.msg.replace(item, "********")
                else:
                    record.msg = record.msg.replace(hidden_data, "********")
        return True


import netmiko

netmiko.base_connection.SecretsFilter = SecretsFilter


class BalabitGWClient(paramiko.SSHClient):
    def _auth(
        self,
        username,
        password,
        pkey,
        key_filenames,
        allow_agent,
        look_for_keys,
        gss_auth,
        gss_kex,
        gss_deleg_creds,
        gss_host,
        passphrase,
    ):
        def balabit_gw_pw_handler(title, instructions, prompt_list):
            resp = []
            for pr in prompt_list:
                if str(pr[0]).strip() == "Gateway password:":
                    resp.append(password[0])
            return tuple(resp)

        self._transport.auth_interactive_dumb(username, balabit_gw_pw_handler)
        self._transport.auth_password(username, password[1])
        return


class BalabitSCB(LinuxSSH):
    pass


class BalabitSCBSSH(BalabitSCB):
    def _build_ssh_client(self):
        """Prepare for Paramiko SSH connection."""
        # Create instance of SSHClient object
        remote_conn_pre = BalabitGWClient()

        # Load host_keys for better SSH security
        if self.system_host_keys:
            remote_conn_pre.load_system_host_keys()
        if self.alt_host_keys and os.path.isfile(self.alt_key_file):
            remote_conn_pre.load_host_keys(self.alt_key_file)

        # Default is to automatically add untrusted hosts (make sure appropriate for your env)
        remote_conn_pre.set_missing_host_key_policy(self.key_policy)
        return remote_conn_pre

    def _open(self) -> None:
        """Decouple connection creation from __init__ for mocking."""
        self._modify_connection_params()
        self.establish_connection(511, 511)
        self._try_session_preparation()


import netmiko
from netmiko.ssh_dispatcher import CLASS_MAPPER

netmiko.platforms.append("balabit_scb")
CLASS_MAPPER["balabit_scb"] = BalabitSCBSSH
