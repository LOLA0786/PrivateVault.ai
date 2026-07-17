from .graph_store import DB
import sqlite3

def record_intent(principal,action,normalized,risk):

    conn=sqlite3.connect(DB)

    conn.execute(
        """
        INSERT INTO intent_graph(
            principal,
            action,
            normalized_action,
            risk
        )
        VALUES(?,?,?,?)
        """,
        (
            principal,
            action,
            normalized,
            risk
        )
    )

    conn.commit()
    conn.close()
