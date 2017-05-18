## Bepatient WebApp deploy api

### Requirements

- python3.X
- Flask

### Routes

> GET / : Get all the available branches (and their URL(s) on the server)
    
> POST/PUT /{branch} : Clone (or pull if existing) and deploy a new branch on the server
    
> DELETE /{branch} : Remove a branch on the server

### Example CLI Usage with shell aliases

#### Deploy
    
> *alias deploy='function _deploy(){ curl -X PUT "http://vm-crashtest.bepatient.mobi:8000/$1" };_deploy'*

Example :

> $ deploy dev

> { "message": "Branch cloned", "url": "http://vm-crashtest.bepatient.mobi/bpapp/<function branch at 0x7fe324aec7b8>/bepatient-app/www-dev/"}


#### Delete
    
> *alias delbranch='function _del(){ curl -X DELETE "http://vm-crashtest.bepatient.mobi:8000/$1" };_del'*

Example :

> $ delbranch dev
    
> {"message": "branch removed"}

### List

> alias listbranch="curl 'http://vm-crashtest.bepatient.mobi:8000/'"

Example :

> $ listbranch

> {"dev": "http://vm-crashtest.bepatient.mobi/bpapp/dev/bepatient-app/www-dev/"}
