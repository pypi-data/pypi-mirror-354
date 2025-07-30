# actinia-rest-lib

This is the rest library for [actinia-core](https://github.com/mundialis/actinia_core).

It is a requirement of actinia-core and some actinia plugins and not meant to be used standalone.


## DEV setup
For a DEV setup integrated with other actinia components, see [here](https://github.com/actinia-org/actinia-docker#local-dev-setup-for-actinia-core-plugins-with-vscode).


### Running tests
You can run the tests in the actinia test docker:

```bash
docker build -f docker/actinia-rest-lib-test/Dockerfile -t actinia-rest-lib-test .
docker run -it actinia-rest-lib-test -i

cd /src/actinia-rest-lib/

# run all tests
make test

# run only unittests
make unittest

# run only tests which are marked for development with the decorator '@pytest.mark.dev'
make devtest
```
