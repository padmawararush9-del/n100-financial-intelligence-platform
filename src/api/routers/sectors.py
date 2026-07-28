from fastapi import APIRouter
from ..database import get_connection

router = APIRouter()


@router.get("/sectors")
def get_sector_summary():

    conn = get_connection()

    query = """
    SELECT
        s.broad_sector,
        COUNT(DISTINCT c.id) AS company_count,
        ROUND(AVG(fr.return_on_equity_pct), 2) AS avg_roe,
        ROUND(AVG(fr.composite_quality_score), 2) AS avg_quality_score,
        ROUND(AVG(fr.revenue_cagr_5yr), 2) AS avg_revenue_cagr
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE fr.year = (
        SELECT MAX(f2.year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )
    GROUP BY s.broad_sector
    ORDER BY avg_quality_score DESC
    """

    rows = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in rows]