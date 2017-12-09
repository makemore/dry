from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import upload_template
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())




env.hosts = ['python.mkmrd.com']
env.user = 'dry'
env.passwords = {'dry@python.mkmrd.com:22': os.environ.get("SERVER_PASSWORD")}
outername = "dry" #or hemingwaybeta
repoName = "dry" #this is always the same, just on a different branch
project = "dry"
root_dir = '/webapps/'

def backup_database():
    code_dir = '/webapps/' + outername
    with cd(code_dir):
        run("pg_dump " + outername + " > env_dry/backups/" + outername + " --clean")


def download_database():
    code_dir = '/webapps/' + outername
    with cd(code_dir):
        get('env_dry/backups/' + outername, '../backups/' + outername)


def restore_local_database():
    local("dropdb " + repoName)
    local("createdb " + repoName)
    local("psql -U chris -d " + repoName + " -f ../backups/" + outername)


def download_db():
    backup_database()
    download_database()
    restore_local_database()