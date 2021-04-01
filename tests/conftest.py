# stdlib
import os

# 3rd party
import pytest
from coincidence.selectors import only_version

pytest_plugins = ("coincidence", )


@pytest.fixture(
		params=[
				pytest.param("3.7", marks=only_version(3.7, "Output differs on each version.")),
				pytest.param("3.8", marks=only_version(3.8, "Output differs on each version.")),
				pytest.param("3.9", marks=only_version(3.9, "Output differs on each version.")),
				pytest.param("3.10", marks=only_version("3.10", "Output differs on each version.")),
				]
		)
def version(request):
	return request.param


@pytest.fixture(
		params=[
				pytest.param(
						"forward",
						marks=pytest.mark.skipif(
								os.sep == '\\', reason=r"Output differs on platforms where os.sep == '\\'"
								)
						),
				pytest.param(
						"backward",
						marks=pytest.mark.skipif(
								os.sep == '/', reason="Output differs on platforms where os.sep == '/'"
								)
						),
				]
		)
def os_sep(request):
	return request.param
