#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "srcML::libsrcml_static" for configuration "Release"
set_property(TARGET srcML::libsrcml_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(srcML::libsrcml_static PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsrcml.a"
  )

list(APPEND _cmake_import_check_targets srcML::libsrcml_static )
list(APPEND _cmake_import_check_files_for_srcML::libsrcml_static "${_IMPORT_PREFIX}/lib/libsrcml.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
