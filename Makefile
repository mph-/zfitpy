.PHONY: install
install:
	#python3 setup.py install
	pip3 install -e .

.PHONY: install-extras
install-extras:

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
	# pytest -s --pdb -o cache_dir=test/.pytest_cache
	# pytest --pdb zfitpy/tests

.PHONY: cover
cover: zfitpy/*.py
	coverage run -m pytest -s --pdb --pyargs zfitpy -o cache_dir="./testing/.pytest_cache"
	coverage html

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
	-rm -rf build zfitpy.egg-info dist testing
	cd doc; make clean
