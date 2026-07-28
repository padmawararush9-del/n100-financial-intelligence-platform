from fastapi import APIRouter, HTTPException
from ..database import get_connection

router = APIRouter()


@router.get("/peers/{ticker}")
def get_peers(ticker: str):

    conn = get_connection()

    # Find sector of requested company
    sector = conn.execute(
        """
        SELECT broad_sector
        FROM sectors
        WHERE company_id = ?
        """,
        (ticker.upper(),),
    ).fetchone()

    if sector is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    broad_sector = sector["broad_sector"]

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.composite_quality_score,
        fr.revenue_cagr_5yr
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE
        s.broad_sector = ?
        AND c.id != ?
        AND fr.year = (
            SELECT MAX(f2.year)
            FROM financial_ratios f2
            WHERE f2.company_id = fr.company_id
        )
    ORDER BY fr.composite_quality_score DESC
    """

    peers = conn.execute(
        query,
        (broad_sector, ticker.upper())
    ).fetchall()

    conn.close()

    return {
        "ticker": ticker.upper(),
        "sector": broad_sector,
        "peer_count": len(peers),
        "peers": [dict(row) for row in peers]
    }