"""
Projects API Router
Practical engineering capstone projects with automated verification harnesses.
"""

import json
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import User, XPTransaction, UserBadge, Badge
from backend.app.core.security import get_optional_current_user
from runner.runner import run_code_in_sandbox

router = APIRouter(prefix="/projects", tags=["projects"])

PROJECTS_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "proj-1",
        "slug": "cli-task-manager",
        "title": "CLI Task & Expense Tracker",
        "difficulty": "beginner",
        "description": "Build a persistent command-line task and expense manager supporting JSON serialization, priority tagging, and summary reporting.",
        "tech_stack": ["Python 3.11", "JSON", "File I/O", "Data Aggregation"],
        "estimated_hours": 3,
        "xp_reward": 200,
        "requirements": [
            "Implement `TaskManager` class with methods: `add_item(title, category, amount)`, `list_items(category=None)`, `get_total(category=None)`, and `delete_item(item_id)`.",
            "Each item must have an integer `id`, string `title`, string `category`, float `amount`, and boolean `completed`.",
            "Persist data to an in-memory or file-backed JSON store, maintaining correct ID sequencing."
        ],
        "starter_code": '''class TaskManager:
    def __init__(self):
        self.items = []
        self._next_id = 1

    def add_item(self, title: str, category: str, amount: float = 0.0) -> dict:
        item = {
            "id": self._next_id,
            "title": title,
            "category": category,
            "amount": float(amount),
            "completed": False
        }
        self.items.append(item)
        self._next_id += 1
        return item

    def list_items(self, category: str = None) -> list:
        if category is None:
            return list(self.items)
        return [i for i in self.items if i["category"] == category]

    def get_total(self, category: str = None) -> float:
        items = self.list_items(category)
        return round(sum(i["amount"] for i in items), 2)

    def delete_item(self, item_id: int) -> bool:
        for idx, item in enumerate(self.items):
            if item["id"] == item_id:
                del self.items[idx]
                return True
        return False
''',
        "verification_suite": '''
manager = TaskManager()
# Test 1: Add items
i1 = manager.add_item("Coffee", "food", 4.50)
i2 = manager.add_item("Server Hosting", "tech", 25.00)
i3 = manager.add_item("Lunch", "food", 12.75)
assert i1["id"] == 1 and i2["id"] == 2 and i3["id"] == 3, "ID auto-increment failed"

# Test 2: List by category
food_items = manager.list_items("food")
assert len(food_items) == 2, f"Expected 2 food items, got {len(food_items)}"

# Test 3: Total calculation
food_total = manager.get_total("food")
assert food_total == 17.25, f"Expected food total 17.25, got {food_total}"
overall_total = manager.get_total()
assert overall_total == 42.25, f"Expected overall total 42.25, got {overall_total}"

# Test 4: Delete item
deleted = manager.delete_item(2)
assert deleted is True, "Expected delete_item(2) to return True"
assert manager.get_total() == 17.25, "Total after deletion incorrect"
print("All Project 1 assertions passed!")
'''
    },
    {
        "id": "proj-2",
        "slug": "async-web-scraper",
        "title": "Resilient Web Scraper & Rate-Limited Client",
        "difficulty": "intermediate",
        "description": "Build a fault-tolerant web crawler client with sliding-window rate limiting, exponential backoff retries, and regex metadata extraction.",
        "tech_stack": ["Python 3.11", "Regex", "Rate Limiting", "Exponential Backoff"],
        "estimated_hours": 5,
        "xp_reward": 350,
        "requirements": [
            "Implement `ResilientScraper` class with `extract_links(html: str) -> list[str]` extracting href attributes.",
            "Implement `extract_metadata(html: str) -> dict` returning `title` and word count.",
            "Implement `simulate_fetch(url: str, fail_count: int) -> dict` that retries with exponential backoff on simulated failures."
        ],
        "starter_code": '''import re

class ResilientScraper:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def extract_links(self, html: str) -> list[str]:
        # Extract all href URLs matching href="..."
        pattern = r'href=[\"\\\']([^\"\\\']+)[\"\\\']'
        return re.findall(pattern, html)

    def extract_metadata(self, html: str) -> dict:
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        text = re.sub(r'<[^>]+>', ' ', html)
        words = text.split()
        return {
            "title": title,
            "word_count": len(words)
        }

    def simulate_fetch(self, url: str, fail_count: int = 0) -> dict:
        attempts = 0
        while attempts <= self.max_retries:
            attempts += 1
            if attempts <= fail_count:
                continue
            return {"url": url, "status": 200, "attempts": attempts}
        raise RuntimeError(f"Failed to fetch {url} after {self.max_retries} retries")
''',
        "verification_suite": '''
scraper = ResilientScraper(max_retries=3)

# Test 1: Link extraction
sample_html = '<p>Check <a href="https://python.org">Python</a> and <a href="/docs/guide.html">Docs</a></p>'
links = scraper.extract_links(sample_html)
assert "https://python.org" in links and "/docs/guide.html" in links, "Link extraction failed"

# Test 2: Metadata extraction
doc_html = '<html><head><title>Python Mastery</title></head><body><h1>Hello World</h1><p>Learn fast.</p></body></html>'
meta = scraper.extract_metadata(doc_html)
assert meta["title"] == "Python Mastery", f"Expected title 'Python Mastery', got {meta['title']}"
assert meta["word_count"] >= 4, f"Word count expected >= 4, got {meta['word_count']}"

# Test 3: Simulated retry
res = scraper.simulate_fetch("https://example.com/api", fail_count=2)
assert res["status"] == 200 and res["attempts"] == 3, f"Retry logic failed: {res}"
print("All Project 2 assertions passed!")
'''
    },
    {
        "id": "proj-3",
        "slug": "fastapi-microservice",
        "title": "RESTful Inventory Microservice",
        "difficulty": "intermediate",
        "description": "Develop an in-memory inventory management engine simulating RESTful endpoints with Pydantic validation, filtering, pagination, and RFC error responses.",
        "tech_stack": ["FastAPI Patterns", "Validation", "Pagination", "Data Modeling"],
        "estimated_hours": 6,
        "xp_reward": 450,
        "requirements": [
            "Implement `InventoryEngine` class simulating REST CRUD operations.",
            "`create_product(name, price, category, stock)`: validates `price > 0`, `stock >= 0`, and assigns unique ID.",
            "`list_products(skip=0, limit=10, category=None)`: returns paginated subset with total count.",
            "`update_stock(product_id, delta)`: updates stock or raises ValueError if stock falls below zero."
        ],
        "starter_code": '''class InventoryEngine:
    def __init__(self):
        self._products = {}
        self._next_id = 1

    def create_product(self, name: str, price: float, category: str, stock: int = 0) -> dict:
        if price <= 0:
            raise ValueError("Price must be positive")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        prod = {
            "id": self._next_id,
            "name": name,
            "price": float(price),
            "category": category,
            "stock": int(stock)
        }
        self._products[self._next_id] = prod
        self._next_id += 1
        return prod

    def get_product(self, product_id: int) -> dict:
        if product_id not in self._products:
            raise KeyError(f"Product {product_id} not found")
        return self._products[product_id]

    def list_products(self, skip: int = 0, limit: int = 10, category: str = None) -> dict:
        all_items = list(self._products.values())
        if category:
            all_items = [p for p in all_items if p["category"] == category]
        total = len(all_items)
        items = all_items[skip : skip + limit]
        return {"total": total, "items": items, "skip": skip, "limit": limit}

    def update_stock(self, product_id: int, delta: int) -> dict:
        prod = self.get_product(product_id)
        new_stock = prod["stock"] + delta
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        prod["stock"] = new_stock
        return prod
''',
        "verification_suite": '''
engine = InventoryEngine()

# Test 1: Product creation
p1 = engine.create_product("Laptop", 1200.0, "electronics", 10)
p2 = engine.create_product("Mouse", 25.0, "electronics", 50)
p3 = engine.create_product("Notebook", 5.0, "stationery", 100)
assert p1["id"] == 1 and p2["id"] == 2 and p3["id"] == 3, "Product ID sequencing failed"

# Test 2: Validation
try:
    engine.create_product("Invalid", -10.0, "electronics")
    assert False, "Should reject negative price"
except ValueError:
    pass

# Test 3: Pagination & Category filter
page = engine.list_products(skip=0, limit=2, category="electronics")
assert page["total"] == 2 and len(page["items"]) == 2, "Pagination failed"

# Test 4: Stock update
updated = engine.update_stock(1, -3)
assert updated["stock"] == 7, f"Expected stock 7, got {updated['stock']}"

try:
    engine.update_stock(1, -10)
    assert False, "Should reject stock below zero"
except ValueError:
    pass

print("All Project 3 assertions passed!")
'''
    },
    {
        "id": "proj-4",
        "slug": "etl-data-pipeline",
        "title": "High-Throughput ETL Pipeline",
        "difficulty": "advanced",
        "description": "Architect an end-to-end data processing pipeline that streams CSV records, normalizes schemas, filters corrupted rows, and calculates summary metrics.",
        "tech_stack": ["Python 3.11", "Generators", "Data Cleaning", "Aggregations"],
        "estimated_hours": 8,
        "xp_reward": 600,
        "requirements": [
            "Implement `ETLPipeline` class with `parse_records(raw_rows: list[dict]) -> list[dict]`.",
            "Clean and normalize records: trim whitespace, parse prices to float, cast quantities to int.",
            "Drop rows with invalid numbers or missing required keys (`id`, `amount`, `quantity`).",
            "Calculate summary metrics: `total_revenue`, `average_order_value`, and `category_breakdown`."
        ],
        "starter_code": '''class ETLPipeline:
    def __init__(self, required_keys=("id", "category", "amount", "quantity")):
        self.required_keys = required_keys

    def clean_record(self, raw: dict) -> dict:
        for k in self.required_keys:
            if k not in raw or raw[k] is None or str(raw[k]).strip() == "":
                return None
        try:
            return {
                "id": str(raw["id"]).strip(),
                "category": str(raw["category"]).strip().lower(),
                "amount": float(raw["amount"]),
                "quantity": int(raw["quantity"])
            }
        except (ValueError, TypeError):
            return None

    def process_records(self, raw_rows: list[dict]) -> dict:
        valid_records = []
        for r in raw_rows:
            cleaned = self.clean_record(r)
            if cleaned is not None:
                valid_records.append(cleaned)

        total_revenue = sum(r["amount"] * r["quantity"] for r in valid_records)
        order_count = len(valid_records)
        avg_order = round(total_revenue / order_count, 2) if order_count > 0 else 0.0

        categories = {}
        for r in valid_records:
            cat = r["category"]
            categories[cat] = categories.get(cat, 0.0) + (r["amount"] * r["quantity"])

        return {
            "processed_count": order_count,
            "dropped_count": len(raw_rows) - order_count,
            "total_revenue": round(total_revenue, 2),
            "average_order_value": avg_order,
            "category_revenue": {k: round(v, 2) for k, v in categories.items()}
        }
''',
        "verification_suite": '''
pipeline = ETLPipeline()

sample_data = [
    {"id": "1", "category": "Books", "amount": "15.50", "quantity": "2"},
    {"id": "2", "category": "Tech", "amount": "120.00", "quantity": "1"},
    {"id": "3", "category": "Books", "amount": "invalid_num", "quantity": "1"}, # Corrupted
    {"id": "4", "category": "", "amount": "50.00", "quantity": "1"},            # Missing category
    {"id": "5", "category": "tech", "amount": "30.00", "quantity": "3"},
]

result = pipeline.process_records(sample_data)
assert result["processed_count"] == 3, f"Expected 3 valid, got {result['processed_count']}"
assert result["dropped_count"] == 2, f"Expected 2 dropped, got {result['dropped_count']}"
# Revenue: (15.50*2) + (120*1) + (30*3) = 31 + 120 + 90 = 241.0
assert result["total_revenue"] == 241.0, f"Expected total 241.0, got {result['total_revenue']}"
assert result["category_revenue"]["books"] == 31.0, "Category calculation failed"
assert result["category_revenue"]["tech"] == 210.0, "Category calculation failed"

print("All Project 4 assertions passed!")
'''
    }
]


class ProjectVerificationPayload(BaseModel):
    project_id: str
    code: str


@router.get("", response_model=List[Dict[str, Any]])
async def list_projects():
    """Returns the list of 4 real-world software engineering capstones."""
    return [
        {
            "id": p["id"],
            "slug": p["slug"],
            "title": p["title"],
            "difficulty": p["difficulty"],
            "description": p["description"],
            "tech_stack": p["tech_stack"],
            "estimated_hours": p["estimated_hours"],
            "status": "available",
            "xp_reward": p["xp_reward"],
            "requirements": p["requirements"],
            "starter_code": p["starter_code"]
        }
        for p in PROJECTS_DATABASE
    ]


@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_project_details(project_id: str):
    """Returns full project requirements, starter code, and tech stack details."""
    for p in PROJECTS_DATABASE:
        if p["id"] == project_id or p["slug"] == project_id:
            return {
                "id": p["id"],
                "slug": p["slug"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "description": p["description"],
                "tech_stack": p["tech_stack"],
                "estimated_hours": p["estimated_hours"],
                "status": "available",
                "xp_reward": p["xp_reward"],
                "requirements": p["requirements"],
                "starter_code": p["starter_code"]
            }
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/{project_id}/verify")
async def verify_project_submission(
    project_id: str,
    payload: ProjectVerificationPayload,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes learner project code against backend verification suite in the isolated sandbox.
    """
    project = next((p for p in PROJECTS_DATABASE if p["id"] == project_id or p["slug"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    full_code = f"{payload.code}\n\n# --- Project Verification Harness ---\n{project['verification_suite']}"

    runner_result = run_code_in_sandbox(full_code, timeout_seconds=10.0)

    is_passed = runner_result.get("passed", False)
    xp_earned = 0

    if is_passed and current_user:
        # Check if already rewarded
        existing_tx = db.query(XPTransaction).filter(
            XPTransaction.user_id == current_user.id,
            XPTransaction.challenge_id == project["id"],
            XPTransaction.source == "project_completion"
        ).first()

        if not existing_tx:
            xp_earned = project["xp_reward"]
            tx = XPTransaction(
                user_id=current_user.id,
                challenge_id=project["id"],
                amount=xp_earned,
                source="project_completion"
            )
            db.add(tx)
            if current_user.profile:
                current_user.profile.total_xp += xp_earned
                current_user.profile.current_level = 1 + (current_user.profile.total_xp // 100)
            db.commit()

    return {
        "submission_id": f"proj-sub-{project['id']}",
        "passed": is_passed,
        "stdout": runner_result.get("stdout", ""),
        "stderr": runner_result.get("stderr", ""),
        "execution_time_ms": runner_result.get("execution_time_ms", 0),
        "attempt_duration_seconds": 1,
        "test_results": [
            {
                "test_index": 1,
                "description": f"Verification Suite: {project['title']}",
                "is_hidden": False,
                "passed": is_passed,
                "input": "Automated Project Harness",
                "expected": "All assertions pass without exception",
                "actual": "Pass" if is_passed else (runner_result.get("stderr") or "Failed assertions")
            }
        ],
        "status": "completed" if is_passed else "failed",
        "xp_earned": xp_earned,
        "total_xp": current_user.profile.total_xp if (current_user and current_user.profile) else 0,
        "current_level": current_user.profile.current_level if (current_user and current_user.profile) else 1,
        "unlocked_next": True,
        "badges_awarded": []
    }
