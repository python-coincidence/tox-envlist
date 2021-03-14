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

# stdlib
import itertools
import re
import warnings
from itertools import chain
from typing import Dict, List

# 3rd party
import pluggy  # type: ignore
from braceexpand import braceexpand  # type: ignore
from tox.config import Config, ParseIni, Parser  # type: ignore

try:
	# 3rd party
	from py._vendored_packages.iniconfig import IniConfig
except ImportError:
	# 3rd party
	from iniconfig import IniConfig  # type: ignore

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.2"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["option_names", "tox_addoption", "tox_configure"]

hookimpl = pluggy.HookimplMarker("tox")

option_names = ["-n", "--envlist-name"]


@hookimpl
def tox_addoption(parser: Parser):
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


DELIMITERS = re.compile(r"[,; \n]\s*(?![^{}]*})")


@hookimpl
def tox_configure(config: Config):
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
	ini_config: IniConfig = config._cfg
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
				warnings.warn(f"Ignoring '{' '.join(args.pop(idx))}' option as '-e / --envlist' option given.")
			elif envlist_name_set:
				if arg[1] in envlists:
					config.envlist = envlists[arg[1]]
				else:
					config._parser.argparser.error(
							f"Unknown envlist '{arg[1]}'. (envlists are '{', '.join(envlists)}')"
							)

	config.args = list(chain.from_iterable(args))

	return config


def expand_section_names(self, config):  # noqa: D103
	# From tox
	# https://github.com/tox-dev

	factor_re = re.compile(r"\{\s*([\w\s.,-]+)\s*\}")
	split_re = re.compile(r"\s*,\s*")

	to_remove = set()

	for section in list(config.sections):
		split_section = factor_re.split(section)

		for parts in itertools.product(*map(split_re.split, split_section)):
			section_name = ''.join(parts)
			if section_name not in config.sections:
				config.sections[section_name] = config.sections[section]
				to_remove.add(section)

	for section in to_remove:
		del config.sections[section]


ParseIni.expand_section_names = expand_section_names
