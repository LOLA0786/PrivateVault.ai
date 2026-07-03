from tool_authorization import authorize_tool_call

def test_reject_never_reports_execution():
    result = authorize_tool_call(
        user_id="agent_001",
        tool_name="process_payment",
        declared_intent={"action":"process_payment"},
        executed_intent={"action":"process_payment"},
        approval={"intent_hash":"bad"},
        capability_token="fake",
        evidence={},
    )

    assert result["authorized"] is False
    assert result["executed"] is False
    assert "signature" not in result
