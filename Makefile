install:
	pip install -r requirements.txt

test:
	pytest

run:
	python run_pipeline.py