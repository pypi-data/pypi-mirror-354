import requests
import time
import json
import argparse

class DataGovFetcher:
    def __init__(self, base_url=\"https://catalog.data.gov/api/3/action/package_search\", rows_per_request=1000):
        self.base_url = base_url
        self.rows = rows_per_request

    def fetch_all_datasets(self, max_pages=None, delay=1):
        start = 0
        all_results = []
        page_count = 0

        while True:
            params = {\"rows\": self.rows, \"start\": start}
            response = requests.get(self.base_url, params=params)
            if response.status_code != 200:
                print(f\"Failed to fetch data at start={start}. Status: {response.status_code}\")
                break

            data = response.json()
            results = data.get(\"result\", {}).get(\"results\", [])
            if not results:
                break

            all_results.extend(results)
            start += self.rows
            page_count += 1
            print(f\"Fetched {len(results)} records (Total: {len(all_results)})\")

            if max_pages and page_count >= max_pages:
                break

            time.sleep(delay)

        return all_results

    def save_to_file(self, data, filename=\"datasets.json\"):
        with open(filename, \"w\", encoding=\"utf-8\") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f\"Saved {len(data)} datasets to {filename}\")

def main():
    parser = argparse.ArgumentParser(description=\"Fetch dataset metadata from Data.gov\")
    parser.add_argument(\"--output\", type=str, default=\"datasets.json\", help=\"Output file name\")
    parser.add_argument(\"--pages\", type=int, default=None, help=\"Maximum number of pages to fetch\")
    parser.add_argument(\"--delay\", type=float, default=1.0, help=\"Delay in seconds between requests\")
    args = parser.parse_args()

    fetcher = DataGovFetcher()
    datasets = fetcher.fetch_all_datasets(max_pages=args.pages, delay=args.delay)
    fetcher.save_to_file(datasets, filename=args.output)

    for ds in datasets[:10]:
        print(f\"- {ds.get('title')}\")

def run():
    main()
