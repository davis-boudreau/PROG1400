import csv
import json
import time
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PriceScraper/1.0; +https://example.com/bot-info)"
}

# ---- Config ----
STORE_BASE = "https://facetofacegames.com/products"  # change if needed
COLLECTION_HANDLE = None  # e.g., "magic-the-gathering-singles" or None

REQUEST_DELAY = 0.7
MAX_RETRIES = 3
TIMEOUT = 30

OUTPUT_CSV = "shopify_products.csv"
OUTPUT_JSON = "shopify_products.json"

# New concise CSV with just titles and prices (per variant)
OUTPUT_TITLES_PRICES = "shopify_titles_prices.csv"
# Optional concise CSV per product-level min/max
OUTPUT_PRODUCT_MINMAX = "shopify_product_minmax_prices.csv"


def get_json(url: str, params: Optional[Dict] = None) -> Optional[Dict]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", "2"))
                time.sleep(retry_after + 1)
                continue
            resp.raise_for_status()
            ct = resp.headers.get("Content-Type", "")
            if "application/json" in ct or resp.text.strip().startswith(("{", "[")):
                return resp.json()
            return None
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                print(f"[!] Failed to fetch {url} after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                return None
            backoff = attempt * 1.5
            time.sleep(backoff)
    return None


def normalize_store_url(base: str) -> str:
    if not base.startswith("http"):
        base = "https://" + base
    return base.rstrip("/")


def product_list_endpoint(base: str, since_id: Optional[int] = None) -> str:
    url = urljoin(base, "/products.json")
    params = {"limit": 250}
    if since_id:
        params["since_id"] = since_id
    return requests.Request("GET", url, params=params).prepare().url


def collection_products_endpoint(base: str, collection_handle: str, page: int) -> str:
    path = f"/collections/{collection_handle}/products.json"
    url = urljoin(base, path)
    params = {"limit": 250, "page": page}
    return requests.Request("GET", url, params=params).prepare().url


def extract_rows(product: Dict, store_base: str) -> List[Dict]:
    rows = []
    product_id = product.get("id")
    handle = product.get("handle") or ""
    product_url = urljoin(store_base, f"/products/{handle}") if handle else ""
    title = product.get("title") or ""
    vendor = product.get("vendor") or ""
    ptype = product.get("product_type") or product.get("type") or ""
    tags = product.get("tags", [])
    if isinstance(tags, list):
        tags_str = ", ".join(tags)
    else:
        tags_str = str(tags or "")

    created_at = product.get("created_at") or ""
    published_at = product.get("published_at") or ""

    image_url = ""
    images = product.get("images") or []
    if images:
        image_url = images[0].get("src", "") or images[0].get("url", "")

    variants = product.get("variants") or []
    if not variants:
        rows.append({
            "product_id": product_id,
            "title": title,
            "handle": handle,
            "vendor": vendor,
            "product_type": ptype,
            "tags": tags_str,
            "created_at": created_at,
            "published_at": published_at,
            "product_url": product_url,
            "image_url": image_url,
            "variant_id": "",
            "variant_title": "",
            "sku": "",
            "option1": "",
            "option2": "",
            "option3": "",
            "price": "",
            "compare_at_price": "",
            "available": "",
            "inventory_management": "",
            "weight": ""
        })
        return rows

    for v in variants:
        rows.append({
            "product_id": product_id,
            "title": title,
            "handle": handle,
            "vendor": vendor,
            "product_type": ptype,
            "tags": tags_str,
            "created_at": created_at,
            "published_at": published_at,
            "product_url": product_url,
            "image_url": image_url,
            "variant_id": v.get("id", ""),
            "variant_title": v.get("title", ""),
            "sku": v.get("sku", ""),
            "option1": v.get("option1", ""),
            "option2": v.get("option2", ""),
            "option3": v.get("option3", ""),
            "price": v.get("price", ""),
            "compare_at_price": v.get("compare_at_price", ""),
            "available": v.get("available", ""),
            "inventory_management": v.get("inventory_management", ""),
            "weight": v.get("weight", "")
        })
    return rows


def crawl_all_products(store_base: str) -> List[Dict]:
    store_base = normalize_store_url(store_base)
    all_products: List[Dict] = []

    since_id = None
    total_fetched = 0

    while True:
        url = product_list_endpoint(store_base, since_id)
        data = get_json(url)
        time.sleep(REQUEST_DELAY)
        if not data or "products" not in data:
            break
        batch = data["products"]
        if not batch:
            break

        all_products.extend(batch)
        total_fetched += len(batch)

        max_id = max(p.get("id", 0) for p in batch)
        if not max_id or (since_id and max_id <= since_id):
            break
        since_id = max_id

    print(f"Fetched {total_fetched} products total.")
    return all_products


def crawl_collection(store_base: str, collection_handle: str) -> List[Dict]:
    store_base = normalize_store_url(store_base)
    page = 1
    all_products: List[Dict] = []
    total_fetched = 0
    seen_ids = set()

    while True:
        url = collection_products_endpoint(store_base, collection_handle, page)
        data = get_json(url)
        time.sleep(REQUEST_DELAY)
        if not data or "products" not in data:
            break
        batch = data["products"]
        new_batch = [p for p in batch if p.get("id") not in seen_ids]
        for p in new_batch:
            seen_ids.add(p.get("id"))
        if not new_batch:
            break

        all_products.extend(new_batch)
        total_fetched += len(new_batch)
        page += 1

    print(f"Fetched {total_fetched} products from collection '{collection_handle}'.")
    return all_products


def save_full_outputs(products: List[Dict], store_base: str):
    rows: List[Dict] = []
    for p in products:
        rows.extend(extract_rows(p, store_base))

    fieldnames = [
        "product_id", "title", "handle", "vendor", "product_type", "tags",
        "created_at", "published_at", "product_url", "image_url",
        "variant_id", "variant_title", "sku", "option1", "option2", "option3",
        "price", "compare_at_price", "available", "inventory_management", "weight"
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {OUTPUT_CSV}")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Saved raw product JSON to {OUTPUT_JSON}")


def save_titles_prices_csv(products: List[Dict]):
    """
    Creates a concise CSV with just title + price per variant.
    Columns: product_id, handle, title, variant_id, variant_title, price, compare_at_price
    """
    rows = []
    for p in products:
        product_id = p.get("id")
        title = p.get("title") or ""
        handle = p.get("handle") or ""
        variants = p.get("variants") or []
        if not variants:
            # emit a product-level row with blanks if there are no variants
            rows.append({
                "product_id": product_id,
                "handle": handle,
                "title": title,
                "variant_id": "",
                "variant_title": "",
                "price": p.get("price") or p.get("price_min") or "",
                "compare_at_price": p.get("compare_at_price") or ""
            })
            continue
        for v in variants:
            rows.append({
                "product_id": product_id,
                "handle": handle,
                "title": title,
                "variant_id": v.get("id", ""),
                "variant_title": v.get("title", ""),
                "price": v.get("price", ""),
                "compare_at_price": v.get("compare_at_price", "")
            })

    fieldnames = ["product_id", "handle", "title", "variant_id", "variant_title", "price", "compare_at_price"]
    with open(OUTPUT_TITLES_PRICES, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {OUTPUT_TITLES_PRICES}")


def save_product_minmax_csv(products: List[Dict]):
    """
    Optional: one row per product using product-level min/max when available.
    Columns: product_id, handle, title, price_min, price_max
    """
    rows = []
    for p in products:
        rows.append({
            "product_id": p.get("id", ""),
            "handle": p.get("handle") or "",
            "title": p.get("title") or "",
            "price_min": p.get("price_min") or "",
            "price_max": p.get("price_max") or ""
        })

    fieldnames = ["product_id", "handle", "title", "price_min", "price_max"]
    with open(OUTPUT_PRODUCT_MINMAX, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {OUTPUT_PRODUCT_MINMAX}")


def main():
    base = STORE_BASE
    if COLLECTION_HANDLE:
        products = crawl_collection(base, COLLECTION_HANDLE)
    else:
        products = crawl_all_products(base)

    if not products:
        print("No products found or endpoint not accessible.")
        return

    # Existing outputs (full detail + raw JSON)
    save_full_outputs(products, base)

    # New concise CSV: titles + prices per variant
    save_titles_prices_csv(products)

    # Optional: uncomment if you also want product-level min/max
    # save_product_minmax_csv(products)


if __name__ == "__main__":
    main()