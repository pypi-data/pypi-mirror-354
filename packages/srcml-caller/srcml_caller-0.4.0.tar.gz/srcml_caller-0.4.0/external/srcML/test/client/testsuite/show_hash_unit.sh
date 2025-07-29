#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-only
#
# @file show_hash_unit.sh
#
# @copyright Copyright (C) 2013-2024 srcML, LLC. (www.srcML.org)

# test framework
source $(dirname "$0")/framework_test.sh

# test hash on single unit
defineXML input <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C" directory="sub" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>
STDOUT

createfile sub/a.cpp.xml "$input"

message "hash provided"

srcml --show-hash sub/a.cpp.xml
check "1a2c5d67e6f651ae10b7673c53e8c502c97316d6\n"

srcml --show-hash < sub/a.cpp.xml
check "1a2c5d67e6f651ae10b7673c53e8c502c97316d6\n"

# test hash on unit with no hash provided
defineXML none <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C" directory="sub" filename="a.cpp"><expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>
STDOUT

# test hash on archive of one unit
defineXML archive <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION">

	<unit revision="REVISION" language="C++" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
STDOUT

# test hash on empty archive
defineXML empty <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION"/>
STDOUT

createfile sub/a.cpp.xml "$none"
createfile sub/archive.cpp.xml "$archive"
createfile sub/emptyarchive.cpp.xml "$empty"

message "hash missing"

srcml --show-hash sub/a.cpp.xml
check

srcml --show-hash < sub/a.cpp.xml
check

srcml --show-hash sub/archive.cpp.xml
check "1a2c5d67e6f651ae10b7673c53e8c502c97316d6\n"

srcml --show-hash < sub/archive.cpp.xml
check "1a2c5d67e6f651ae10b7673c53e8c502c97316d6\n"

srcml --show-hash sub/emptyarchive.cpp.xml
check

srcml --show-hash < sub/emptyarchive.cpp.xml
check
