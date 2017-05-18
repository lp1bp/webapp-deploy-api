#!./env/bin/python3

from flask import Flask, jsonify
from subprocess import call
from os import chdir, path, getcwd, listdir
from shutil import rmtree

host = "0.0.0.0"
port = "8000"
repo = "git@github.com:bepatient-fr/app-ionic.git"
pwd = getcwd()
print(pwd)

app = Flask(__name__)

def clone_branch(branch_name):
    if not path.exists("static/%s" %branch_name):
        call(["git", "clone", repo, "-b", branch_name, "static/%s" %branch_name])
    else:
        chdir("static/%s/bepatient-app/" %branch_name)
        call(["git", "pull"])
    chdir(pwd)

def build_project(branch_name):
    try:
        chdir("static/%s/bepatient-app/" %branch_name)
    except FileNotFoundError as e:
        return jsonify(error="This branch doesn't seems to exist on this repository"), 404
    call(["npm", "install"])
    call(["gulp", "project"])
    chdir(pwd)
    return jsonify(message="Branch cloned",
                   url="http://vm-crashtest.bepatient.mobi/bpapp/%s/bepatient-app/www-dev/" %branch)


def delete_dir(branch_name):
    if path.exists("static/%s" %branch_name):
        rmtree("static/%s" %branch_name)
    return jsonify(message='branch removed')

def list_branches():
    branches = {}
    for branch in listdir("static"):
        branches[branch] = "http://vm-crashtest.bepatient.mobi/bpapp/%s/bepatient-app/www-dev/" %branch
    return branches

@app.route("/")
def index():
    return jsonify(list_branches())

@app.route("/<branch>", methods=['PUT', 'POST'])
def put_branch(branch):
    clone_branch(branch)
    return build_project(branch)

@app.route("/<branch>", methods=['DELETE'])
def delete_branch(branch):
    return delete_dir(branch)

@app.route("/<branch>", methods=['GET'])
def branch(branch):
    return app.send_static_file('%s/bepatient-app/www-dev/index.html' %branch)

def main():
    app.run(host=host, port=port, threaded=True)
    return

if __name__ == '__main__':
    main()
