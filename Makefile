# Top-level control of the building/installation/cleaning of various targets

# python virtual environment

build:
	@docker build -t dls_challenge .

run_container: build
	@docker run -e PYTHONUNBUFFERED=0 -d -p 5000:5000 dls_challenge
