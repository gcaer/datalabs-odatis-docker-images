# Makefile for convenience, (doesn't look for command outputs)
.PHONY: all
all: vreodatis

# Setting environment variables from .env file
# "-" == "if exists" , do not forget to copy .env.template to .env
-include .env

.PHONY: vreodatis
vreodatis : conda-lock apt docker

# Fast lock: pixi solve (rattler + uv) then conversion of vreodatis/pixi.lock to conda-lock.yml
conda-lock:
	pixi run lock vreodatis

# Former lock with conda-lock (slow), kept to compare results
conda-lock-legacy:
	cd vreodatis ; \
	conda-lock lock -f environment.yml -f ../.base_layer/base-notebook-environment.yml  -f ../.base_layer/pangeo-notebook-environment.yml  -p linux-64;
#	conda-lock render -k explicit -p linux-64; \
#	../generate-packages-list.py conda-linux-64.lock > packages.txt

apt:
	cd vreodatis ; \
	../merge-apt.sh ../.base_layer/base-notebook-apt.txt apt.txt ../.base_layer/pangeo-notebook-apt.txt  apt.txt

docker:
	cd vreodatis ; \
	docker build -t vre-odatis:master . --progress=plain --platform linux/amd64; \
	docker run -w $(TESTDIR) -v $(PWD):$(TESTDIR) vre-odatis:master ./run_tests.sh vreodatis


update:
	python update_base_layer.py

HARBOR_REGISTRY?=registry.hpc.ifremer.fr
HARBOR_OWNER?=hpc-jupyterhub-dev

build:
	cd vreodatis ; \
	docker build -t vre-odatis:master . --progress=plain --platform linux/amd64;
	
publish:
	docker tag \
	  vreodatis:master \
	  "$(HARBOR_REGISTRY)/$(HARBOR_OWNER)/vre-odatis:master"
	docker push "$(HARBOR_REGISTRY)/$(HARBOR_OWNER)/vre-odatis:master"
