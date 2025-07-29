#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "srcML::libsrcml_shared" for configuration "Release"
set_property(TARGET srcML::libsrcml_shared APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(srcML::libsrcml_shared PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsrcml.1.0.0.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libsrcml.1.dylib"
  )

list(APPEND _cmake_import_check_targets srcML::libsrcml_shared )
list(APPEND _cmake_import_check_files_for_srcML::libsrcml_shared "${_IMPORT_PREFIX}/lib/libsrcml.1.0.0.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
