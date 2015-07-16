

all:
	python3 -m tia

clear:
	- rm tia/*.pyc tia/__pycache__

freeze:
	pip3 freeze > requirements
