#!/usr/bin/python -tt

import os
import sys
import argparse
import json
import logging
import logging.handlers
import git
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


WEBHOOK_NAME = 'repocopy'
TEMP_DIR_ROOT = '/tmp/'
REPO_FROM = ''
REPO_TO = ''


class Webhook(BaseHTTPRequestHandler):

    def _get_tmp_repo(self):
        """
        Returns the temporary repository to copy from one side to another
        """

        repo_path = os.path.join(TEMP_DIR_ROOT, 'repocopy_' + self.data['repository']['name'])
        if os.path.exists(repo_path):
            return git.Repo(repo_path)
        else:
            os.mkdir(repo_path)
            return git.Repo.init(repo_path)

    def _ensure_remotes(self, repo):
        """
        Checks if git remotes are configured for this repository
        """

        remote_names = [r.name for r in repo.remotes]
        if 'origin' not in remote_names:
            repo.create_remote('origin', REPO_FROM)

        if 'destiny' not in remote_names:
            repo.create_remote('destiny', REPO_TO)

    def do_POST(self):
        """
        Handle POST data
        """

        message = 'OK'
        self.rfile._sock.settimeout(5)
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.send_header("Content-length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)

        # parse data
        self.data = json.loads(data_string)

        # Processes only posts from REPO_FROM
        if self.data['repository']['url'] == REPO_FROM:

            # Get git repo instance
            tmp_repo = self._get_tmp_repo()
            self._ensure_remotes(tmp_repo)

            # The name of the current branch involved in the "push"
            commit_branch = self.data['ref'].rsplit('/', 1)[1]

            # Update remote branches
            tmp_repo.git.fetch(all=True)

            if commit_branch in tmp_repo.remote().stale_refs:
                # Branch deleted, we need to remove it both locally and remote (in "destiny" remote)
                head_to_delete = ([e for e in tmp_repo.heads if e.name == commit_branch] or [None])[0]
                eligible_heads = set(tmp_repo.heads) - set([head_to_delete])
                if head_to_delete:
                    if tmp_repo.active_branch == head_to_delete:
                        tmp_repo.git.checkout(eligible_heads.pop())

                    log.info('Deleting local branch ({})'.format(head_to_delete.name))
                    tmp_repo.delete_head(head_to_delete, force=True)

                    log.info('Deleting remote branch ({}) in destiny'.format(head_to_delete.name))
                    tmp_repo.git.push('destiny', commit_branch, delete=True)
            else:
                # Branch pushed normal (create local branch if needed)
                if commit_branch not in [b.name for b in tmp_repo.branches]:
                    tmp_repo.git.checkout(b=commit_branch)
                else:
                    tmp_repo.git.checkout(commit_branch)
                log.info('Copying {} commits ({} branch) from {} to {}'.format(self.data['total_commits_count'],
                                                                               commit_branch, REPO_FROM, REPO_TO))
                tmp_repo.git.pull('origin', commit_branch)
                tmp_repo.git.push('destiny', commit_branch, force=True)

    def log_message(self, formate, *args):
        """
        Disable printing to stdout/stderr for every post
        """
        return


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='{} Webhook'.format(WEBHOOK_NAME))

    # Prepare settings
    default_port = 8000  # Webhook server port
    default_log_max_size = 50 * 1048576  # 50 MB
    default_backup_count = 4  # Number of historical data logs

    parser.add_argument('-p', '--port', help='Server port ({} will be used by default)'.format(default_port), default=default_port, type=int)
    parser.add_argument('-l', '--log', help='Specify a log file otherwise stdout will be used', required=False)
    parser.add_argument('--tmp-dir-root', help='Path where temporary repository will be created', required=False, default=TEMP_DIR_ROOT)
    parser.add_argument('--repo-from', help='Repo URL to copy from', required=True)
    parser.add_argument('--repo-to', help='Repo URL to copy to', required=True)
    parser.add_argument('--log-level', help='Logging level (INFO by default)', default=logging.INFO)
    parser.add_argument('--log-max-size', help='Log max size ({} bytes by default)'.format(default_log_max_size), default=default_log_max_size)
    parser.add_argument('--log-backup-count', help='Number of historical data logs ({} by default)'.format(default_backup_count), default=default_backup_count)

    args = parser.parse_args()

    TEMP_DIR_ROOT = args.tmp_dir_root
    REPO_FROM = args.repo_from
    REPO_TO = args.repo_to

    log = logging.getLogger('webhook_log')
    log.setLevel(args.log_level)
    if args.log:
        log_handler = logging.handlers.RotatingFileHandler(args.log,
                                                           maxBytes=args.log_max_size,
                                                           backupCount=args.backup_count)
    else:
        log_handler = logging.StreamHandler(sys.stdout)
    f = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(message)s",
                          "%B %d %H:%M:%S")
    log_handler.setFormatter(f)
    log.addHandler(log_handler)

    # Launch server
    try:
        server = HTTPServer(('', args.port), Webhook)
        log.info('Starting webhook server ({}) on port {}...'.format(WEBHOOK_NAME, args.port))
        server.serve_forever()
    except KeyboardInterrupt:
        log.info('CTRL-C pressed, closing webhook...')
        server.socket.close()
