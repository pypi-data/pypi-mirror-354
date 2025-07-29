find_library(LIBKRISP_ABSPATH NAMES krisp-audio-sdk-static PATHS ${KRISP_LIB_DIR})
if (NOT LIBKRISP_ABSPATH) 
	message(FATAL_ERROR "Can't find krisp-audio-sdk in the " ${KRISP_LIB_DIR})
endif()

# Debug message to verify the platform
message(STATUS "Linux on ARM64 02: ${IS_LINUX_ARM64}")

if(APPLE)
	if(${CMAKE_SYSTEM_PROCESSOR} MATCHES ".*(arm|ARM).*")
		include(krisp.third.party.mac.arm.cmake)
	else()
		include(krisp.third.party.mac.x64.cmake)
	endif()
elseif(UNIX AND NOT IS_LINUX_ARM64)
	include(krisp.third.party.linux.x64.cmake)
elseif(UNIX AND IS_LINUX_ARM64)
    include(krisp.third.party.linux.arm64.cmake)
elseif(WIN32)
	include(krisp.third.party.windows.x64.cmake)
endif()

set(KRISP_LIBS 
	${LIBKRISP_ABSPATH}
	${KRISP_THIRDPARTY_LIBS}
)
