
import os
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "pros_cons_generated.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def latest_rows(df):
    if "year" in df.columns:
        return df.sort_values("year").groupby("company_id").tail(1)
    return df

def load_data():
    conn = sqlite3.connect(DB_PATH)

    fr = latest_rows(pd.read_sql("SELECT * FROM financial_ratios", conn))
    pl = latest_rows(pd.read_sql("SELECT * FROM profitandloss", conn))
    cf = latest_rows(pd.read_sql("SELECT * FROM cashflow", conn))
    bs = latest_rows(pd.read_sql("SELECT * FROM balancesheet", conn))
    comp = pd.read_sql("SELECT company_name,id as company_id FROM companies", conn)

    conn.close()

    df = comp.merge(fr, on="company_id", how="left", suffixes=("","_fr"))
    df = df.merge(pl, on="company_id", how="left", suffixes=("","_pl"))
    df = df.merge(cf, on="company_id", how="left", suffixes=("","_cf"))
    df = df.merge(bs, on="company_id", how="left", suffixes=("","_bs"))

    return df

def confidence(val, low, high):
    if pd.isna(val):
        return 0
    if val >= high:
        return 95
    if val >= low:
        return 75
    return 0

def evaluate(df):
    rows=[]

    for _,r in df.iterrows():
        cid=r["company_id"]

        pros=[]
        cons=[]

        # PRO 1
        c=confidence(r.get("return_on_equity_pct"),20,25)
        if c>60:
            pros.append(("PRO_01","Consistently high return on equity above 20% demonstrates exceptional capital efficiency",c))

        # PRO 2
        if r.get("free_cash_flow_cr",0)>0:
            pros.append(("PRO_02","Strong free cash flow generation indicates healthy business fundamentals",80))

        # PRO 3
        if r.get("debt_to_equity",99)==0:
            pros.append(("PRO_03","Debt-free balance sheet provides financial flexibility and eliminates interest burden",95))

        # PRO 4
        c=confidence(r.get("revenue_cagr_5yr"),15,20)
        if c>60:
            pros.append(("PRO_04","Revenue growing above 15% CAGR reflects strong business momentum",c))

        # PRO 5
        if r.get("operating_profit_margin_pct",0)>25:
            pros.append(("PRO_05","Operating profit margin above 25% indicates strong pricing power and cost discipline",90))

        # PRO 6
        if r.get("pat_cagr_5yr",0)>20:
            pros.append(("PRO_06","Net profit compounding above 20% creates significant shareholder value",90))

        # PRO 7
        if r.get("interest_coverage",0)>10 or r.get("debt_to_equity",1)==0:
            pros.append(("PRO_07","Very high interest coverage reflects negligible financial stress",90))

        # PRO 8
        if r.get("dividend_yield_pct",0)>2 and r.get("free_cash_flow_cr",0)>0:
            pros.append(("PRO_08","Dividend yield backed by positive free cash flow",85))

        # PRO 9
        if r.get("eps_cagr_5yr",0)>15:
            pros.append(("PRO_09","EPS growing above 15% CAGR indicates strong earnings quality",88))

        # CON 1
        if r.get("debt_to_equity",0)>2:
            cons.append(("CON_01",f"Debt-to-equity ratio of {r['debt_to_equity']:.2f} is elevated.",95))

        # CON 2
        if r.get("free_cash_flow_cr",1)<0:
            cons.append(("CON_02","Negative free cash flow raises concern about cash generation quality",85))

        # CON 3
        if r.get("operating_profit_margin_pct",100)<10:
            cons.append(("CON_03","Low operating margin suggests pricing or cost pressure",80))

        # CON 4
        if r.get("net_profit",1)<0:
            cons.append(("CON_04","Company reported a net loss in the latest financial year",95))

        # CON 5
        if r.get("interest_coverage",99)<1.5:
            cons.append(("CON_06","Interest coverage below 1.5x indicates debt servicing risk",90))

        # CON 6
        if r.get("revenue_cagr_5yr",100)<5:
            cons.append(("CON_12","Revenue CAGR below 5% suggests limited business momentum",75))

        if not pros:
            pros.append(("PRO_DEFAULT","Stable business fundamentals require further qualitative review",65))

        if not cons:
            cons.append(("CON_DEFAULT","No major financial weaknesses detected; monitor sector-specific risks",65))

        for rid,text,c in pros:
            rows.append([cid,"pro",rid,text,c])
        for rid,text,c in cons:
            rows.append([cid,"con",rid,text,c])

    return pd.DataFrame(rows,columns=[
        "company_id","type","rule_id","text","confidence_pct"
    ])

def main():
    df=load_data()
    out=evaluate(df)
    out.to_csv(OUTPUT_FILE,index=False)
    print(out.head())
    print(f"Generated {len(out)} insights")
    print(f"Saved to {OUTPUT_FILE}")

if __name__=="__main__":
    main()
