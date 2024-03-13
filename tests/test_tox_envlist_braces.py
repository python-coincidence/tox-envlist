# stdlib
import sys
import sysconfig
from typing import List

# 3rd party
import pytest
import tox  # type: ignore
import tox.reporter  # type: ignore
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus
from testing_tox import prepare_stdout, run_tox

example_tox = PathPlus(__file__).parent / "example_tox_braces.ini"


def _prepare_stdout(stdout: str, toxinidir: PathPlus) -> str:
	stdout = prepare_stdout(stdout, toxinidir)
	platbase = sysconfig.get_config_var("installed_platbase")
	if platbase:
		stdout = stdout.replace(platbase, "...")
	return stdout


@pytest.fixture()
def toxinidir(tmp_pathplus: PathPlus) -> PathPlus:
	(tmp_pathplus / "tox.ini").write_text(example_tox.read_text())
	return tmp_pathplus


manual_envs = f"py{sys.version_info[0]}{sys.version_info[1]}-attrs{19.3,20.2},mypy"


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
@pytest.mark.usefixtures("version", "os_sep")
def test_tox_envlist(
		capsys,
		command: List[str],
		toxinidir: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	try:
		run_tox(command, toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		advanced_file_regression.check(_prepare_stdout(capout.out, toxinidir))


@pytest.mark.usefixtures("os_sep")
def test_tox_envlist_no_command(capsys, toxinidir: PathPlus):
	# The output varies depending on the versions of python installed on the host
	tox.reporter._INSTANCE.tw._file = sys.stdout

	try:
		run_tox([], toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		assert capout.out


@pytest.mark.usefixtures("os_sep")
def test_tox_envlist_test(capsys, toxinidir: PathPlus):
	# The output varies depending on the versions of python installed on the host
	tox.reporter._INSTANCE.tw._file = sys.stdout

	try:
		run_tox(["-n", "test"], toxinidir)

	finally:
		capout = capsys.readouterr()
		assert not capout.err
		assert capout.out
