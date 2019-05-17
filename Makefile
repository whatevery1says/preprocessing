check:
	-pycodestyle . > lint-pycodestyle.txt
	-pylint ../preprocessing >> lint-pylint.txt

docker-build:
	docker build -t jeremydouglass/preprocessing .

docker-run:
	docker run -p 8888:8888 jeremydouglass/preprocessing

setup:
	# sudo apt-get install libfuzzy-dev ssdeep 
	pip install spacy=2.1.3
	python -m spacy download en_core_web_sm
	python -m spacy download en_core_web_md
	python -m spacy download en_core_web_lg
	pip install -r requirements.txt

run:
	python zip_preprocess.py
