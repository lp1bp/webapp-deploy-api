#!./env/bin/python3

from flask import Flask, jsonify, send_from_directory, redirect
from subprocess import call
from os import chdir, path, getcwd, listdir
from shutil import rmtree

host = "127.0.0.1"
port = "8001"
repo = "git@github.com:bepatient-fr/app-ionic.git"
pwd = getcwd()

app = Flask(__name__)

def clone_branch(branch_name):
    if not path.exists("static/%s" %branch_name):
        call(["git", "clone", repo, "-b", branch_name, "static/%s" %branch_name])
    else:
        chdir("static/%s/bepatient-app/" %branch_name)
        call(["git", "stash"])
        call(["git", "pull"])
    chdir(pwd)

def build_project(branch_name):
    try:
        chdir("static/%s/bepatient-app/" %branch_name)
    except FileNotFoundError as e:
        chdir(pwd)
        return jsonify(error="This branch doesn't seems to exist on this repository"), 404
    call(["npm", "install"])
    call(["gulp", "project"])
    chdir(pwd)
    return jsonify(message="Branch cloned",
                   url="/view/%s" %branch_name)


def delete_dir(branch_name):
    if path.exists("static/%s" %branch_name) and branch_name != 'client':
        rmtree("static/%s" %branch_name)
    return jsonify(message='branch removed')

def list_branches():
    chdir(pwd)
    branches = {}
    for branch in listdir("static"):
        if branch != 'client':
            branches[branch] = "/view/%s" %branch
    return branches

@app.route("/")
def redirect_index():
    return redirect("/client", code=302)

@app.route("/client")
def client():
    return app.send_static_file('client/index.html')

@app.route('/client/<path:path>')
def send_js(path):
    print("rendering from client %s" %path)
    return send_from_directory('static/client', path)

@app.route("/branch", methods=['GET'])
def get_branches():
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
    return redirect('/view/%s' %branch, code=302)

@app.route("/view/<branch>/", methods=['GET'])
def view_index(branch):
    print("VIEW INDEX")
    return app.send_static_file('%s/bepatient-app/www/index.html' %branch)

@app.route("/view/<branch>/<path:path>", methods=['GET'])
def view(branch, path):
    return send_from_directory('static/%s/bepatient-app/www/' %branch, path)

def main():
    app.run(host=host, port=port, threaded=True)
    return

if __name__ == '__main__':
    main()
