from fastapi import APIRouter, Query
from ..database import get_connection

router = APIRouter()


@router.get("/screener")
def stock_screener(
    sector: str | None = Query(default=None),
    min_roe: float | None = Query(default=None),
    max_debt_to_equity: float | None = Query(default=None),
    min_quality_score: float | None = Query(default=None),
    min_revenue_cagr: float | None = Query(default=None),
):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        fr.year,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.composite_quality_score
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE fr.year = (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )
    """

    params = []

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    if min_roe is not None:
        query += " AND fr.return_on_equity_pct >= ?"
        params.append(min_roe)

    if max_debt_to_equity is not None:
        query += " AND fr.debt_to_equity <= ?"
        params.append(max_debt_to_equity)

    if min_quality_score is not None:
        query += " AND fr.composite_quality_score >= ?"
        params.append(min_quality_score)

    if min_revenue_cagr is not None:
        query += " AND fr.revenue_cagr_5yr >= ?"
        params.append(min_revenue_cagr)

    query += """
    ORDER BY
        fr.composite_quality_score DESC,
        fr.return_on_equity_pct DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]