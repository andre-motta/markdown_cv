.PHONY: install test sample

install:
	python3 -m pip install -e .

test:
	python3 -m unittest discover -s tests

sample:
	markdown-cv build examples/sample_cv.md --output examples/sample_cv.pdf
