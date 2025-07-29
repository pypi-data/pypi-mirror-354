#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-only
#
# @file show_src-version_unit.sh
#
# @copyright Copyright (C) 2013-2024 srcML, LLC. (www.srcML.org)

# test framework
source $(dirname "$0")/framework_test.sh

# test on single unit
defineXML input <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="C++" directory="bar" filename="foo" version="1.0"/>
STDOUT

# test on archive of one unit
defineXML archive <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" version="1.0">

	<unit revision="REVISION" version="1.0" language="C++" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
STDOUT

createfile sub/a.cpp.xml "$input"
createfile sub/archive.cpp.xml "$archive"

srcml --show-src-version sub/a.cpp.xml
check "1.0\n"

srcml --show-src-version < sub/a.cpp.xml
check "1.0\n"

srcml --show-src-version sub/archive.cpp.xml
check "1.0\n"

srcml --show-src-version < sub/archive.cpp.xml
check "1.0\n"

# test src version on single unit with empty version
defineXML empty <<- 'STDIN'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" language="" directory="" filename="" version=""/>
STDIN

# test on archive of one unit with an empty version
defineXML emptyarchive <<- 'STDOUT'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION" version="">

	<unit revision="REVISION" version="" language="C++" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
STDOUT

createfile sub/a.cpp.xml "$empty"
createfile sub/archive.cpp.xml "$emptyarchive"

srcml --show-src-version sub/a.cpp.xml
check "\n"

srcml --show-src-version < sub/a.cpp.xml
check "\n"

srcml --show-src-version sub/archive.cpp.xml
check "\n"

srcml --show-src-version < sub/archive.cpp.xml
check "\n"

# test on empty archive with no version
defineXML noneempty <<- 'STDIN'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" xmlns:cpp="http://www.srcML.org/srcML/cpp"/>
STDIN

# test on archive of one unit with no version
defineXML none <<- 'STDIN'
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<unit xmlns="http://www.srcML.org/srcML/src" revision="REVISION">

	<unit revision="REVISION" language="C++" filename="a.cpp" hash="1a2c5d67e6f651ae10b7673c53e8c502c97316d6">
	<expr_stmt><expr><name>a</name></expr>;</expr_stmt>
	</unit>

	</unit>
STDIN

createfile sub/a.cpp.xml "$noneempty"
createfile sub/archive.cpp.xml "$none"

srcml --show-src-version sub/a.cpp.xml
check

srcml --show-src-version < sub/a.cpp.xml
check

srcml --show-src-version sub/archive.cpp.xml
check

srcml --show-src-version < sub/archive.cpp.xml
check
