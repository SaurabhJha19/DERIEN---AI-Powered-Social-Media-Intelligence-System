from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/network", tags=["Network"])


@router.get("/graph")
def get_network_graph(limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()

    # Nodes with risk
    cur.execute("""
        SELECT u.user_id,
               COALESCE(rs.total_score, 0),
               COALESCE(rs.risk_level, 'Low')
        FROM users u
        LEFT JOIN risk_scores rs
          ON rs.entity_id = u.user_id
         AND rs.entity_type = 'user'
        LIMIT %s;
    """, (limit,))

    nodes = [
        {
            "id": r[0],
            "risk": float(r[1]),
            "level": r[2]
        }
        for r in cur.fetchall()
    ]

    # Edges from interactions
    cur.execute("""
        SELECT source_user, target_user
        FROM interactions
        WHERE source_user IS NOT NULL
          AND target_user IS NOT NULL
        LIMIT %s;
    """, (limit * 2,))

    edges = [
        {"from": r[0], "to": r[1]}
        for r in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return {"nodes": nodes, "edges": edges}
