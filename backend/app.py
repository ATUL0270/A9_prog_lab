"""Flask backend for the product listing website.

Serves:
  * REST API under /api/...
  * the static frontend (HTML/CSS/JS) from ../frontend

The frontend never touches the database; it only calls the API.
"""
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "shop.db"
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=None)

MAX_PAGE_SIZE = 50
SORT_OPTIONS = {
    "name_asc": "p.name ASC",
    "name_desc": "p.name DESC",
    "price_asc": "p.price ASC",
    "price_desc": "p.price DESC",
    "newest": "p.id DESC",
}


# ---------- database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def error(message, status):
    return jsonify({"error": message}), status


def row_to_product(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "price": row["price"],
        "image_url": row["image_url"],
        "stock": row["stock"],
        "category": row["category"],
        "category_id": row["category_id"],
    }


# ---------- API ----------
@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/categories")
def list_categories():
    rows = get_db().execute("SELECT id, name FROM categories ORDER BY name").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/products")
def list_products():
    args = request.args
    where, params = [], []

    # search (name or description)
    search = args.get("search", "").strip()
    if len(search) > 100:
        return error("'search' must be at most 100 characters", 400)
    if search:
        where.append("(p.name LIKE ? OR p.description LIKE ?)")
        like = f"%{search}%"
        params += [like, like]

    # category filter
    if "category" in args:
        try:
            category_id = int(args["category"])
        except ValueError:
            return error("'category' must be an integer", 400)
        where.append("p.category_id = ?")
        params.append(category_id)

    # price range
    for key, op in (("min_price", ">="), ("max_price", "<=")):
        if key in args:
            try:
                value = float(args[key])
            except ValueError:
                return error(f"'{key}' must be a number", 400)
            if value < 0:
                return error(f"'{key}' must be non-negative", 400)
            where.append(f"p.price {op} ?")
            params.append(value)

    # sorting
    sort = args.get("sort", "newest")
    if sort not in SORT_OPTIONS:
        return error(f"'sort' must be one of: {', '.join(SORT_OPTIONS)}", 400)

    # pagination
    try:
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 12))
    except ValueError:
        return error("'page' and 'limit' must be integers", 400)
    if page < 1 or limit < 1 or limit > MAX_PAGE_SIZE:
        return error(f"'page' must be >= 1 and 'limit' between 1 and {MAX_PAGE_SIZE}", 400)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    db = get_db()

    total = db.execute(
        f"SELECT COUNT(*) FROM products p {where_sql}", params
    ).fetchone()[0]

    rows = db.execute(
        f"""SELECT p.*, c.name AS category
            FROM products p JOIN categories c ON c.id = p.category_id
            {where_sql}
            ORDER BY {SORT_OPTIONS[sort]}
            LIMIT ? OFFSET ?""",
        params + [limit, (page - 1) * limit],
    ).fetchall()

    return jsonify({
        "items": [row_to_product(r) for r in rows],
        "total": total,
        "page": page,
        "limit": limit,
    })


@app.get("/api/products/<product_id>")
def get_product(product_id):
    try:
        pid = int(product_id)
    except ValueError:
        return error("Product id must be an integer", 400)

    row = get_db().execute(
        """SELECT p.*, c.name AS category
           FROM products p JOIN categories c ON c.id = p.category_id
           WHERE p.id = ?""",
        (pid,),
    ).fetchone()
    if row is None:
        return error(f"Product {pid} not found", 404)
    return jsonify(row_to_product(row))


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith("/api/"):
        return error("Resource not found", 404)
    return send_from_directory(FRONTEND_DIR, "index.html"), 404


@app.errorhandler(405)
def method_not_allowed(_e):
    return error("Method not allowed", 405)


# ---------- frontend ----------
@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/product")
def product_page():
    return send_from_directory(FRONTEND_DIR, "product.html")


@app.get("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    if not DB_PATH.exists():
        raise SystemExit("Database not found. Run: python database/init_db.py")
    app.run(host="127.0.0.1", port=5000, debug=True)
