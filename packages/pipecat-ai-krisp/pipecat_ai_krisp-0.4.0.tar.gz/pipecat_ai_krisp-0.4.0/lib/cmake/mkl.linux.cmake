target_link_libraries(
    ${PYMODNAME_NC}
    PRIVATE
    "$<LINK_GROUP:RESCAN,${MKL_LIB_LIST}>"
    pthread
    m
    dl
)