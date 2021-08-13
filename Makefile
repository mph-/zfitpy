.PHONY: install
install:
	python3 setup.py install

.PHONY: package
package:
	python3 setup.py sdist bdist_wheel

.PHONY: upload-test
upload-test: package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: package
	python3 -m twine upload dist/*

.PHONY: test
test: zfitpy/*.py
	nosetests3 -s --pdb

.PHONY: cover
cover: zfitpy/*.py
	nosetests3 --pdb --with-coverage --cover-package=zfitpy --cover-html

.PHONY: doc-install
doc-install: doc
	scp -r doc/_build/html/* zfitpy.elec.canterbury.ac.nz:/var/www/zfitpy/

.PHONY: doc
release: doc push
	cd /tmp; rm -rf zfitpy; git clone git@github.com:mph-/zfitpy.git; cd zfitpy; make test; make upload

.PHONY: release-test
release-test: doc push
	cd /tmp; rm -rf zfitpy; git clone git@github.com:mph-/zfitpy.git; cd zfitpy; make test

.PHONY: style-check
style-check:
	flake8 zfitpy
	flake8 doc

.PHONY: flake8
flake8:
	flake8 zfitpy
	flake8 doc

.PHONY: check
check: style-check test

.PHONY: push
push: check
	git push
	git push --tags

.PHONY: doc
doc:
	cd doc; make html

.PHONY: clean
clean:
	-rm -rf build zfitpy.egg-info dist
	cd doc; make clean
