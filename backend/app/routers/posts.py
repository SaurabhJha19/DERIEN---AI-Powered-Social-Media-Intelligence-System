from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/high-risk")
def get_high_risk_posts(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT entity_id, total_score, risk_level
        FROM risk_scores
        WHERE entity_type = 'post'
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
            "post_id": r[0],
            "score": r[1],
            "risk_level": r[2]
        }
        for r in rows
    ]


@router.get("/{post_id}/explain")
def explain_post(post_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT indicator_type, indicator_value, weight
        FROM post_indicators
        WHERE post_id = %s;
        """,
        (post_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "indicator_type": r[0],
            "indicator_value": r[1],
            "weight": r[2]
        }
        for r in rows
    ]
