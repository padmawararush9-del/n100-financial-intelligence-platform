from fastapi import APIRouter, HTTPException, Query
from ..database import get_connection

router = APIRouter()


@router.get("/companies")
def get_companies(
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None),
):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        c.roe_percentage,
        c.roce_percentage
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    WHERE 1=1
    """

    params = []

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    if market_cap_category:
        query += " AND s.market_cap_category = ?"
        params.append(market_cap_category)

    if search:
        query += """
        AND (
            c.company_name LIKE ?
            OR c.id LIKE ?
        )
        """
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY c.company_name"

    companies = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in companies]


@router.get("/companies/{ticker}")
def get_company(ticker: str):
    conn = get_connection()

    company = conn.execute(
        """
        SELECT
            c.*,
            s.broad_sector,
            s.sub_sector,
            s.market_cap_category
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        WHERE c.id = ?
        """,
        (ticker.upper(),),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    ratios = conn.execute(
    """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    AND year != 'TTM'
    ORDER BY SUBSTR(year, -4) DESC
    """,
    (ticker.upper(),),
).fetchall()

    conn.close()

    return {
    "company": dict(company),
    "ratios": [dict(r) for r in ratios],
}