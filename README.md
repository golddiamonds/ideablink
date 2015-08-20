# ideablink
Link sharing and commenting.

I wrote the bulk of this almost two years ago. It's not really meant for primetime; but, it can be used as a fun learning experience. It uses Python Flask and MySQL.

All code is free for any use, reuse, and modification. The name "hashsquid" and "hashsquid.com" are, however, owned by me.

###Requirements###
- Python 2.6+
- MySQL
- Flask
- MySQLdb (module for connecting b/w Python and MySQL)

###Setup###
- Run the "create" scripts in /DB followed by the "alter" script.
- Update config.py (at the very least DBPWD)

###Running###
Type
```
python ideablink.py
```

###Considerations###
- Don't use "root" for MySQL database user.
- Change SECRET_KEY in config.py
- Use a stronger hash than MD5 for passwords.
- Be careful using "debug=True" in ideablink.py.
