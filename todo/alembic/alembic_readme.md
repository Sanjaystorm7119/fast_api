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
-------------------------------------------------------------

alembic revision :
this is how we create a new alembic file where we can add some type of database upgrade / downgrade

eg: alembic revision -m "create phone number cols on user table"
creates a new file where we can write the upgrade code
each new revision will have a revsion id (data migration specific)

eg : alembic code

def upgrade():
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=True))

def downgrade():
    op.drop_column('users', 'email')
