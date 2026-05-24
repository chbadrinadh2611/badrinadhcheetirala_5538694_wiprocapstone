import csv
import os
from utils.logger import get_logger

logger = get_logger("CSVReader")

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testdata", "testdata.csv")


def read_testdata(filepath=CSV_PATH):
    logger.info(f"Reading CSV: {filepath}")
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    logger.info(f"Loaded {len(rows)} rows from CSV")
    return rows


def get_brands():
    rows = read_testdata()
    brands = [row["brand"] for row in rows]
    logger.info(f"Brands: {brands}")
    return brands


def get_ratings():
    rows = read_testdata()
    ratings = [row["rating"] for row in rows]
    logger.info(f"Ratings: {ratings}")
    return ratings
