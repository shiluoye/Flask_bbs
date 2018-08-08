## My BBS

This is a practical project, based on Python, Flask, SQLAlchemy, MySQL and etc.

[DEMO](http://118.25.101.182/)

![image](https://github.com/yim7/yim-club/blob/master/bbs.gif)

## Config
```
git@github.com:yim7/yim-club.git
```
You need to create `yim-club/secret.py` and `yim-club/database_secret.conf`
```
# secret.py
secret_key = 'test'
database_password = 'test'
database_name = 'test'
test_mail = 'test@gmail.com'
admin_mail = 'admin@yim7.com'
```
```
# database_secret.conf
mysql-server mysql-server/root_password password test
mysql-server mysql-server/root_password_again password test
```
## Run
```
# reset database
python3 reset.py
#
python3 app.py
```
You can click http://localhost:2000 to visit bbs.

## Deploy
```
bash deploy.sh
```