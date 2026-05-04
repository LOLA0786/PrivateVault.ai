from pv_cost_layer.audit.replay import by_request_id

rid = input("request_id: ").strip()
entries = by_request_id(rid)
for e in entries:
    print(e)
