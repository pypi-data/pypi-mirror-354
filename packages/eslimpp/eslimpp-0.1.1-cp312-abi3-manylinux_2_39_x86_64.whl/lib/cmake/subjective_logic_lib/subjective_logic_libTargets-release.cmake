#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "subjective_logic_lib::subjective_logic_test" for configuration "Release"
set_property(TARGET subjective_logic_lib::subjective_logic_test APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(subjective_logic_lib::subjective_logic_test PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/subjective_logic_test"
  )

list(APPEND _cmake_import_check_targets subjective_logic_lib::subjective_logic_test )
list(APPEND _cmake_import_check_files_for_subjective_logic_lib::subjective_logic_test "${_IMPORT_PREFIX}/bin/subjective_logic_test" )

# Import target "subjective_logic_lib::operator_test" for configuration "Release"
set_property(TARGET subjective_logic_lib::operator_test APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(subjective_logic_lib::operator_test PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/operator_test"
  )

list(APPEND _cmake_import_check_targets subjective_logic_lib::operator_test )
list(APPEND _cmake_import_check_files_for_subjective_logic_lib::operator_test "${_IMPORT_PREFIX}/bin/operator_test" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
