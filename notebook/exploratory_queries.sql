-- 1. Total Companies
SELECT COUNT(*) FROM companies;

-- 2. Top 10 Companies by Market Cap
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 3. Highest ROE
SELECT company_id, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- 4. Top Sales
SELECT company_id, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 5. Highest Net Profit
SELECT company_id, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 6. Companies by Sector
SELECT broad_sector, COUNT(*)
FROM sectors
GROUP BY broad_sector;

-- 7. Latest Stock Prices
SELECT company_id, close_price
FROM stock_prices
ORDER BY date DESC
LIMIT 20;

-- 8. Companies with Debt
SELECT company_id, total_debt_cr
FROM financial_ratios
WHERE total_debt_cr > 0;

-- 9. Companies with Highest Dividend Payout
SELECT company_id, dividend_payout
FROM profitandloss
ORDER BY dividend_payout DESC
LIMIT 10;

-- 10. Annual Reports Count
SELECT company_id, COUNT(*)
FROM documents
GROUP BY company_id
ORDER BY COUNT(*) DESC;