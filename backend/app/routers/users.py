from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/high-risk")
def get_high_risk_users(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT entity_id, total_score, risk_level
        FROM risk_scores
        WHERE entity_type = 'user'
        ORDER BY total_score DESC
        LIMIT %s;
        """,
        (limit,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "user_id": r[0],
            "score": round(r[1], 3),
            "risk_level": r[2],
        }
        for r in rows
    ]

@router.get("/{user_id}/detail")
def get_user_detail(user_id: str):
    conn = get_connection()
    cur = conn.cursor()

    # Risk scores
    cur.execute("""
        SELECT content_score,
               behaviour_score,
               network_score,
               total_score,
               risk_level
        FROM risk_scores
        WHERE entity_type = 'user'
          AND entity_id = %s
        ORDER BY total_score DESC
        LIMIT 1;
    """, (user_id,))

    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return {"error": "User not found"}

    content, behaviour, network, total, level = row

    # Related posts
    cur.execute("""
        SELECT post_id
        FROM posts
        WHERE user_id = %s
        LIMIT 10;
    """, (user_id,))

    posts = [r[0] for r in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "user_id": user_id,
        "content_score": content,
        "behaviour_score": behaviour,
        "network_score": network,
        "total_score": total,
        "risk_level": level,
        "posts": posts
    }
