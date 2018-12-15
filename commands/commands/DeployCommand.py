# !/usr/bin/env python
import os
import zipfile

from core.eme import loadConfig


def zipdir(ziph, path, loc=None, skip=None):
    nlist = ziph.namelist()

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            name = root.replace('\\', '/') + '/' + file
            if '__pycache__' in name or '.log' in name or (skip and skip in name):
                continue

            if loc:
                lname = loc + '/' + file
                if lname not in nlist:
                    ziph.write(name, lname)
            else:
                if name not in nlist:
                    ziph.write(name)


class DeployCommand():
    def __init__(self, server):
        self.server = server

        self.conf = loadConfig('commands/deploy/ssh.json')

    def run(self, *args):
        import paramiko

        zipf = zipfile.ZipFile('deployment.zip', 'w', zipfile.ZIP_DEFLATED)

        # write production config
        zipf.write('commands/deploy/website.json', 'website/config.json')
        zipf.write('commands/deploy/server.json', 'server/config.json')

        # main game
        zipdir(zipf, 'website/', skip='config.json')
        zipdir(zipf, 'core/')
        zipdir(zipf, 'server', skip='config.json')
        zipdir(zipf, 'commands')

        # write app core & utils
        zipf.write('game.py')
        zipf.write('cli.py')

        zipf.close()

        if not '-y' in args:
            print("Publish to server? y/n")
            if not input() == 'y':
                return

        print('Connecting to server...')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(self.conf['host'], username=self.conf['username'], password=self.conf['password'])
        sftp = ssh.open_sftp()
        print('Uploading file...')
        sftp.put('deployment.zip', self.conf['remotepath'] + '/deployment.zip')
        sftp.close()

        if not '-y' in args:
            print("Install geopoly? y/n")
            if not input() == 'y':
                ssh.close()
                return

        print('Installing...')
        stdin, stdout, stderr = ssh.exec_command("unzip -o {0}/deployment.zip -d {0}".format(self.conf['remotepath']))
        err = stderr.readlines()
        if err:
            print(err)
            ssh.close()
            return

        stdin, stdout, stderr = ssh.exec_command("rm -rf {0}/deployment.zip".format(self.conf['remotepath']))
        if err:
            print(err)
            ssh.close()
            return

        stdin, stdout, stderr = ssh.exec_command("systemctl restart gunicorn")
        if err:
            print(err)
            ssh.close()
            return

        stdin, stdout, stderr = ssh.exec_command("systemctl restart gameserver")
        if err:
            print(err)
            ssh.close()
            return

        stdin, stdout, stderr = ssh.exec_command("systemctl status gunicorn")
        print(stdout.readlines())

        ssh.close()
