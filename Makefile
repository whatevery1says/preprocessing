check:
	-pycodestyle . > lint-pycodestyle.txt
	-pylint ../preprocessing >> lint-pylint.txt

docker-build:
	docker build -t jeremydouglass/preprocessing .

docker-run:
	docker run -p 8888:8888 jeremydouglass/preprocessing

run:
	python zip_preprocess.py
