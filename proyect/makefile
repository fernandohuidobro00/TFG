export PGDATABASE := yelp_database
export PGUSER := fernando
export PGPASSWORD := fernando
export PGCLIENTENCODING := LATIN9
export PGHOST := localhost
PSQL = psql

CMD = python3 manage.py
HEROKU = heroku run export SQLITE=1 &


run:
	$(CMD) runserver

reset_db: clear_db update_db 

clear_db:
	@echo Clear Database
	dropdb --if-exists $(PGDATABASE)
	createdb -U fernando -h localhost yelp_database

shell:
	@echo create psql shell
	@$(PSQL)

populate:
	@echo populate database
	python3 ./populate.py

update_db:
	$(CMD) makemigrations
	$(CMD) migrate

create_super_user:
	$(CMD) shell -c "from app.models import Student; Student.objects.create_superuser('fernando', 'fernando@fernando.es', 'fernando')"

clear_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	python3 ./manage.py makemigrations app
	python3 ./manage.py migrate


test_datamodel:
	$(CMD) test app.tests_models

test_services:
	$(CMD) test app.tests_services

#test_heroku:
#	$(HEROKU) $(CMD) test datamodel.tests_models.GameModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.MoveModelTests --keepdb & wait
#	$(HEROKU) $(CMD) test datamodel.tests_models.my_tests --keepdb & wait
#
test_query:
	$(CMD) test app.test_query
#
#test_query_heroku:
#	$(HEROKU) python3 test_query.py
#
git:
	git add * && git commit && git push
#
config_heroku:
	heroku login
	heroku git:remote protected-bastion-43256
#
push_heroku:
	git push heroku master