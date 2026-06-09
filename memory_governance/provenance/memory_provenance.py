VALID_SOURCES = {
    "user_input",
    "retrieval",
    "agent_generated",
    "tool_generated",
    "human_approved",
    "external_api",
}


def verify_provenance(
    source
):
    return source in VALID_SOURCES


def assert_provenance(
    source
):
    if not verify_provenance(source):
        raise Exception(
            "INVALID_MEMORY_PROVENANCE"
        )

    return True
