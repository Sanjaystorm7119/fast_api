Alembic :

lightweight datamigration tool when using sqlalchemy
plan transfer upgrade resourses within databases
allows to change a sqlalchemy database table after it is created

##sqlalchemy can only create new database tables , it cannot enhance

alembic allows us to add columns to table (enhance it)
allows to create migration environment


--------------------------------------------------------
alembic init <foldername> : inits a new generic env
alembic revision -m <message> : creates a new revision of env
alembic upgrade <revision id> : run upgrade migration to our db
alembic downgrade -1 : run downgrade migration to our db

------------------------------------------------------------
automatically created when a project is init with alembic

alembic.ini : this is the file alembiclooks for when invoked : contains config info that we are able to change to match our proj 


alembic directory :
has all env properties for alembic
holds all revisions
where you call migrations to upgrade / downgrade
