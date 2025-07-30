set(subjective_logic_lib_VERSION "0.0.0")

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################
if (1)
    set_and_check(subjective_logic_lib_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include/")
    #Comment the following line if you have a header-only library (INTERFACE library)
    set_and_check(subjective_logic_lib_LIB_DIR "${PACKAGE_PREFIX_DIR}/lib/")
    #Uncomment the following line if your library installs binaries
    #set_and_check(subjective_logic_lib_BIN_DIR "${PACKAGE_PREFIX_DIR}/bin/")
endif()

set(subjective_logic_lib_LIBRARIES subjective_logic_lib::subjective_logic_lib )


if (1)
    check_required_components(subjective_logic_lib)
endif()

#Include exported targets
get_filename_component(SELF_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(${SELF_DIR}/subjective_logic_libTargets.cmake)
