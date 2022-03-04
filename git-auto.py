"""
Description: Generates include paths for eclipse project

Copyright (C) Okane Labs, Inc. - All rights reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

__author__ = "Anish Agarwal"
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

    def run_cmd(self, cmd):

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

            if "fatal" in str(stderroutput):
                print(f"Cmd: {cmd_str}| Repo: {repo_name} > {err}")
            else:
                print(f"Cmd: {cmd_str}| Repo: {repo_name} > Success")

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

if __name__ == '__main__':

    repos = \
    [
        {"name": "ronyn-os-boot_stm32h743vit", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit")},
        {"name": "ronyn-os-boot", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Core\\ronyn-os-boot")},
        {"name": "ronyn-os-gfx", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Core\\ronyn-os-gfx")},
        {"name": "ronyn-shogunate", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Core\\ronyn-shogunate")},
        {"name": "okane-crypt", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Core\\ronyn-shogunate\\okane-crypt")},
        {"name": "okane-safe-buf", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Core\\ronyn-shogunate\\okane-safe-buf")},
        {"name": "okane-se", "path": get_posix_path("C:\\ronyn-wallets\\ronyn-os-boot_stm32h743vit\\Middlewares\\Third_Party\\okane-labs\\okane-se")}
    ]

    config = dict()
    config["repos"] = repos

    ga = GitAuto(**config)

    release_branch = "rosb_v2022.03.02"

    # Create release
    # ga.checkout_new(release_branch)
    # ga.add()
    # ga.commit(f"New release branch: rosb_{release_branch}")
    # ga.push_new(release_branch)

    # Merge master and develop
    ga.checkout("develop")
    ga.pull()
    ga.checkout("master")
    ga.pull()
    ga.checkout(release_branch)
    ga.merge("develop")
    ga.merge("master")
    ga.commit("Merged master and develop")
    ga.add()
    ga.push()

    # Create tag
    # ga.tag(f"rosb_{release_branch}")
    # ga.push_tags()
