#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-only
#
# @file show_timestamp_unit.sh
#
# @copyright Copyright (C) 2013-2024 srcML, LLC. (www.srcML.org)

# test framework
source $(dirname "$0")/framework_test.sh

# test get timestamp
defineXML input <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C" directory="sub" filename="a.cpp" timestamp="Sun Jan 11 18:39:22 2015"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>
STDOUT

createfile sub/a.cpp.xml "$input"
message "timestamp provided"

srcml --show-timestamp sub/a.cpp.xml
check "Sun Jan 11 18:39:22 2015\n"

srcml --show-timestamp < sub/a.cpp.xml
check "Sun Jan 11 18:39:22 2015\n"

defineXML none <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C" directory="sub" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>
STDOUT

createfile sub/a.cpp.xml "$none"

# timestamp missing

srcml --show-timestamp sub/a.cpp.xml
check

srcml --show-timestamp < sub/a.cpp.xml
check
