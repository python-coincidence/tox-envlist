#!/usr/bin/env python3
#
#  __init__.py
"""
Allows selection of a different tox envlist.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  "expand_section_names" from tox
#  https://github.com/tox-dev/tox
#  MIT Licensed
#

# stdlib
import itertools
import re
from itertools import chain
from typing import TYPE_CHECKING, Dict, List

# 3rd party
import pluggy  # type: ignore
from braceexpand import braceexpand  # type: ignore
from domdf_python_tools.words import word_join
from tox import config, reporter  # type: ignore

if TYPE_CHECKING:
	# 3rd party
	from iniconfig import IniConfig

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.3.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["option_names", "tox_addoption", "tox_configure"]

hookimpl = pluggy.HookimplMarker("tox")

#: The names of the options which may be passed on the command line to select the envlist to use.
option_names = ["-n", "--envlist-name"]


@hookimpl
def tox_addoption(parser: config.Parser):
	"""
	Add a command line option to choose a different envlist.
	"""

	parser.add_argument(
			*option_names,
			help="The name of the envlist to use.",
			default=None,
			type=str,
			nargs=1,
			)


# The permitted delimiters between elements of an envlist
DELIMITERS = re.compile(r"[,; \n]\s*(?![^{}]*})")

# Unlike the default one in tox this one allows full stops / periods / decimal points
# Important for version numbers
factor_re = re.compile(r"{\s*([\w\s.,-]+)\s*}")
split_re = re.compile(r"\s*,\s*")


@hookimpl
def tox_configure(config: config.Config):
	"""
	Parse the command line and ini options.
	"""

	args: List[List[str]] = [[]]

	while config.args:
		val: str = config.args.pop(0)
		if val == "--":
			break
		elif val.startswith('-'):
			args.append([val])
		else:
			args[-1].append(val)

	envlist_set = False
	envlist_name_set = False

	# Parse envlists
	ini_config: "IniConfig" = config._cfg
	envlists: Dict[str, List[str]] = {}

	for envlist_name, envlist in ini_config.sections.get("envlists", {}).items():
		envlist_elements = DELIMITERS.split(envlist)
		expanded_envlist = list(chain.from_iterable(map(braceexpand, envlist_elements)))
		envlists[envlist_name] = list(filter(None, expanded_envlist))

	for idx, arg in enumerate(args):
		if arg and arg[0] in {"-e", "--envlist"}:
			envlist_set = True
		elif arg and arg[0] in option_names:
			envlist_name_set = True

	for idx, arg in enumerate(args):
		if arg and arg[0] in option_names:
			if envlist_name_set and envlist_set:
				reporter.warning(
						f"Ignoring '{' '.join(args.pop(idx))}' option as '-e / --envlist' option given.",
						)

			elif envlist_name_set and arg[1] in envlists:
				config.envlist = envlists[arg[1]]

			elif envlist_name_set:
				config._parser.argparser.error(
						f"Unknown envlist {arg[1]!r}. (envlists are {word_join(envlists, use_repr=True)})"
						)

	config.args = list(chain.from_iterable(args))

	return config


def expand_section_names(self, config):  # noqa: D103
	# Unlike the default one in tox this one allows full stops / periods / decimal points
	# Important for version numbers

	to_remove = set()

	for section in list(config.sections):
		split_section = factor_re.split(section)

		for parts in itertools.product(*map(split_re.split, split_section)):
			section_name = ''.join(parts)
			if section_name not in config.sections:  # pragma: no cover
				config.sections[section_name] = config.sections[section]
				to_remove.add(section)

	for section in to_remove:  # pragma: no cover
		del config.sections[section]


config.ParseIni.expand_section_names = expand_section_names
