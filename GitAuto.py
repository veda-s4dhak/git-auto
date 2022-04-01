"""
Description: Generates include paths for eclipse project

Copyright (C) Okane Labs, Inc. - All rights reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

__author__ = "Veda Sadhak"
__copyright__ = "Copyright 2021, Ronyn Wallets"
__version__ = "0.0.2"

import os
import pathlib
import subprocess

PIPE = subprocess.PIPE

def get_posix_path(path):
    return str(pathlib.PureWindowsPath(path).as_posix())

class GitAuto:

    def __init__(self, **kwargs):

        self.repos = kwargs["repos"]

    def run_cmd(self, cmd, print_output=False):

        for repo in self.repos:

            repo_name = repo["name"]
            repo_path = repo["path"]

            os.chdir(repo_path)

            cmd_str = ""
            for param in cmd:
                cmd_str += param + " "

            process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            out = str(stdoutput).replace('b"', '').replace('\\n"', '')
            err = str(stderroutput).replace('b"', '').replace('\\n"', '')

            if "fatal" in str(stderroutput) or "warning" in str(stderroutput):
                print(f"Cmd: {cmd_str}| Repo: {repo_name} > {err}")
            elif print_output:
                print(f"Cmd: {cmd_str}| Repo: {repo_name} > {out}")
            else:
                print(f"Cmd: {cmd_str}| Repo: {repo_name} > Success")

    def status(self):
        self.run_cmd(["git", "status"], print_output=True)

    def branch(self):
        self.run_cmd(["git", "branch", "--show-current"], print_output=True)

    def pull(self):
        self.run_cmd(["git", "pull"])

    def add(self):
        self.run_cmd(["git", "add", "."])

    def commit(self, msg):
        self.run_cmd(["git", "commit", "-m", msg])

    def push(self):
        self.run_cmd(["git", "push"])

    def push_new(self, branch_name):
        self.run_cmd(["git", "push", "--set-upstream", "origin", branch_name])

    def checkout_new(self, branch_name):
        self.run_cmd(["git", "checkout", "-b", branch_name])

    def checkout(self, branch_name):
        self.run_cmd(["git", "checkout", branch_name])

    def tag(self, tag_name):
        self.run_cmd(["git", "tag", tag_name])

    def push_tags(self):
        self.run_cmd(["git", "push", "--tags"])

    def merge(self, branch_src):
        self.run_cmd(["git", "merge", branch_src])