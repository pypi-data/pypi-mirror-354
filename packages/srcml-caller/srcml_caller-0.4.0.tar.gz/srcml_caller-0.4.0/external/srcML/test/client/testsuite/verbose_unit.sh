#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-only
#
# @file verbose_unit.sh
#
# @copyright Copyright (C) 2013-2024 srcML, LLC. (www.srcML.org)

# test framework
source $(dirname "$0")/framework_test.sh

# testing for verbose
defineXML fsrcml <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C++" filename="sub/a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt></unit>
STDOUT

define output <<- 'STDERR'
	XML encoding:  UTF-8
	    1 C++      1 sub/a.cpp

	Source Files: 1	Other Files: 0	Errors: 0	Total Files: 1
STDERR

createfile sub/a.cpp "a;"
createfile sub/a.cpp.xml "$fsrcml"

# from a file
srcml sub/a.cpp --verbose
check "$fsrcml" "$output"

srcml --verbose sub/a.cpp
check "$fsrcml" "$output"

srcml sub/a.cpp --verbose -o sub/c.cpp.xml
check sub/c.cpp.xml "$fsrcml" "$output"

srcml --verbose sub/a.cpp -o sub/c.cpp.xml
check sub/c.cpp.xml "$fsrcml" "$output"

# from standard in
defineXML srcml <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt></unit>
STDOUT

define output <<- 'STDERR'
	XML encoding:  UTF-8
	    1 C++      1

	Source Files: 1	Other Files: 0	Errors: 0	Total Files: 1
STDERR

srcml --verbose -l C++ < sub/a.cpp
check "$srcml" "$output"

srcml --verbose -l C++ -o sub/c.cpp.xml < sub/a.cpp
check sub/c.cpp.xml "$srcml" "$output"

# srcml to src
srcml --verbose sub/a.cpp.xml -o sub/c.cpp
check

srcml --verbose -l C++ -o sub/c.cpp < sub/a.cpp.xml
check

srcml --verbose --quiet
check_exit 1

srcml --quiet --verbose
check_exit 1
