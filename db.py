from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

#MySQL Configuration
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "test"
app.config["MYSQL_DATABASE_DB"] = "testdb"#"roytuts"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)