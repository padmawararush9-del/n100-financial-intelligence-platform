import sqlite3
import traceback
import pandas as pd
from tearsheet import generate_pdf

DB_PATH = "data/nifty100.db"


def get_company_ids():
    conn = sqlite3.connect(DB_PATH)

    try:
        companies = pd.read_sql(
            "SELECT id FROM companies ORDER BY id",
            conn
        )
    finally:
        conn.close()

    return companies["id"].tolist()


def main():

    try:
        company_ids = get_company_ids()

    except Exception:
        print("Unable to read company list.")
        traceback.print_exc()
        return

    total = len(company_ids)

    if total == 0:
        print("No companies found in database.")
        return

    print("=" * 60)
    print(f"Generating PDFs for {total} companies")
    print("=" * 60)

    success = 0
    failed = 0
    failed_ids = []

    for index, company_id in enumerate(company_ids, start=1):

        print(f"[{index}/{total}] Company ID: {company_id}")

        try:
            generate_pdf(company_id)
            success += 1
            print("✓ Success\n")

        except Exception:
            failed += 1
            failed_ids.append(company_id)

            print(f"\n{'='*70}")
            print(f"ERROR FOR COMPANY: {company_id}")
            print(f"{'='*70}")

            traceback.print_exc()

            print(f"{'='*70}\n")

    print("=" * 60)
    print("Batch PDF Generation Completed")
    print("=" * 60)
    print(f"Total Companies : {total}")
    print(f"Successful      : {success}")
    print(f"Failed          : {failed}")

    if failed_ids:
        print("\nFailed Company IDs:")
        print(", ".join(map(str, failed_ids)))

    print("=" * 60)


if __name__ == "__main__":
    main()