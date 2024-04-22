# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Perforce Database Task Functions.

In order for this database system to operate properly, the user must make sure that the
global login/connection in p4 is set to the project's server location.

1.      Open cmd prompt and enter the following command:
            p4 set
        Then run the next command:
            p4 info
2.      This gives us information about the global perforce connections. Next, we need
        to set some of the variables. First is P4PORT. So type in the following:
            p4 set P4PORT=<ip address of server>
3.      User should then set the P4USER variable like the following:
            p4 set P4USER=<username on server>
4.      Then the user needs to login with that username onto the server.
        Type in the following:
            p4 login <username>
        It should then ask for the user's password.
5.      Next we have to set the global workspace to the user's workspace for the
        current project. Type in the following:
            p4 set P4CLIENT=<name of user's workspace>
6.      User should now be set up to have the p4 commands here run properly.
        (still needs to be tested by another user)
"""

from datetime import datetime
import logging
import os
import subprocess as sp

from P4 import P4, P4Exception

from Core import core_paths as cpath

from src.tools.Core.util import file_util_tools as fut

LOG = logging.getLogger(__name__)

MODULE_PATH = f"{cpath.get_parent_directory(__file__, 1)}"

TASKS_DIRECTORY = f"{MODULE_PATH}/tasks"


def create_db_task():
    p4 = P4()
    p4.connect()

    LOG.info("client: %s", p4.client)

    changed_files = [
        (
            f"//{p4.client}/DCC/Pipe/src/tools/Perforce/DatabaseTasks/tasks/"
            "test_data.json"
        )
    ]
    change_msg = p4.save_change({"Change": "new", "Description": "test description"})[0]
    changelist_num = int(change_msg.split(" ")[1])

    add_perforce_files(changed_files, changelist_num)

    LOG.info("changelist_num: %s", changelist_num)

    fetched_change = p4.fetch_change(changelist_num)

    p4.run_submit(fetched_change)

    # p4_set_cmd = "p4 set"
    # sp_process = sp.Popen(
    #     p4_set_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, text=True
    # )

    # p4_set_output = ""
    # with sp_process as process:
    #     stdout, stderr = process.communicate()
    #     LOG.debug("P4 Set Errors: %s", stderr)
    #     p4_set_output = stdout.split("\n")

    # username = get_p4_user(p4_set_output)
    # print(f"output:\n{p4_set_output}")
    # print(f"username: {username}")

    # test_data = {"username": username}

    # send_db_task(test_data)


def add_perforce_files(files_to_add: list, changelist_num: int):
    for new_file in files_to_add:
        p4_add_cmd = f"p4 add -c {changelist_num} {new_file}"

        sp_process = sp.Popen(
            p4_add_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, text=True
        )
        with sp_process as process:
            stdout, stderr = process.communicate()
            LOG.debug("P4 Add Errors: %s", stderr)


def send_db_task(task_data: dict):
    LOG.info("Sending Database task...")
    create_new_changelist()


def create_new_changelist():
    p4_create_changelist_cmd = "p4 change -i"

    sp_process = sp.Popen(
        p4_create_changelist_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, text=True
    )
    change_output = ""
    with sp_process as process:
        stdout, stderr = process.communicate()
        LOG.debug("P4 Change Errors: %s", stderr)
        change_output = stdout

    print(change_output)


def get_p4_user(p4_set_output: list):
    """Get P4 Username of currently set user workspace.

    Args:
        p4_set_output (list): List of split lines of a p4 set command.

    Returns:
        str: Name of user in P4.
    """
    username = ""
    for line in p4_set_output:
        if "P4USER" not in line:
            continue
        username = line.split("=")[-1].split(" ")[0]

    return username


if __name__ == "__main__":
    create_db_task()
