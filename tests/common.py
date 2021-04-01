# stdlib
import re
import sys
from typing import Iterable

# 3rd party
import pytest
import tox.reporter  # type: ignore
from domdf_python_tools.paths import PathPlus, in_directory


def run_tox(args: Iterable[str], toxinidir: PathPlus):
	tox.reporter._INSTANCE.tw._file = sys.stdout

	with pytest.raises(SystemExit), in_directory(toxinidir):
		tox.cmdline(list(args))


def prepare_stdout(stdout: str, toxinidir: PathPlus):
	stdout = stdout.replace(str(toxinidir), "...")
	stdout = re.sub(
			r"\.\.\./\.tox/.*/lib/python3\.\d/site-packages/pip/_vendor/packaging/version\.py:\d*: "
			r"DeprecationWarning: Creating a LegacyVersion has been deprecated and will be removed "
			r"in the next major release, {2}(warnings\.warn\(|DeprecationWarning,)",
			'',
			stdout,
			)

	return stdout
