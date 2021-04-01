# stdlib
import sys
from typing import List

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from tests.common import prepare_stdout, run_tox

example_tox = PathPlus(__file__).parent / "example_tox.ini"


@pytest.fixture()
def toxinidir(tmp_pathplus: PathPlus) -> PathPlus:
	(tmp_pathplus / "tox.ini").write_text(example_tox.read_text())
	return tmp_pathplus


manual_envs = f"py{sys.version_info[0]}{sys.version_info[1]},mypy"


@pytest.mark.parametrize(
		"command",
		[
				pytest.param(["-e", manual_envs], id="manual_envs"),
				pytest.param(["-e", manual_envs, "--", "--verbose"], id="manual_envs_posargs"),
				pytest.param(["-n", "qa"], id="qa_envlist"),
				pytest.param(["-n", "qa", "--", "--verbose"], id="envlist_posargs"),
				pytest.param(["-n", "qa", "-e", "mypy"], id="invalid_combo"),
				]
		)
def test_tox_envlist(
		capsys,
		command: List[str],
		toxinidir: PathPlus,
		version: str,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):

	try:
		run_tox(command, toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		advanced_file_regression.check(prepare_stdout(capout.out, toxinidir))


def test_tox_envlist_no_command(capsys, toxinidir: PathPlus):
	# The output varies depending on the versions of python installed on the host

	try:
		run_tox([], toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		assert capout.out


def test_tox_envlist_test(capsys, toxinidir: PathPlus):
	# The output varies depending on the versions of python installed on the host

	try:
		run_tox(["-n", "test"], toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		assert capout.out


def test_tox_envlist_unknown(capsys, toxinidir: PathPlus):
	# The output varies depending on the versions of python installed on the host

	try:
		run_tox(["-n", "cov"], toxinidir)
	finally:
		capout = capsys.readouterr()
		assert "tox: error: Unknown envlist 'cov'. (envlists are 'test' and 'qa')" in capout.err
