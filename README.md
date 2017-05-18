## Bepatient WebApp deploy api

### Requirements

- python3.X
- Flask

### Routes

> GET / : Get all the available branches (and their URL(s) on the server)
    
> POST/PUT /{branch} : Clone (or pull if existing) and deploy a new branch on the server
    
> DELETE /{branch} : Remove a branch on the server