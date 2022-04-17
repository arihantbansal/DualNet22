clean:
	black .
	isort . --profile black
	flake8 . --ignore=F401,E501,E402

install:
	pip install black isort flake8
	pip install -r requirements.txt

clear:
	find . -name '__pycache__' | xargs rm -r -f
	find . -name 'DS_Store' | xargs rm -f
	rm logs/*.log

freeze:
	pip freeze > requirements.txt