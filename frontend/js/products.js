// Product listing page: search, filter, sort, paginate.

const state = { search: "", category: "", sort: "newest", page: 1, limit: 8 };

const grid = document.getElementById("grid");
const pager = document.getElementById("pager");

async function loadCategories() {
  try {
    const cats = await apiGet("/api/categories");
    const select = document.getElementById("category");
    cats.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      select.appendChild(opt);
    });
  } catch (e) {
    setStatus("Could not load categories: " + e.message, true);
  }
}

async function loadProducts() {
  const params = new URLSearchParams({
    sort: state.sort, page: state.page, limit: state.limit,
  });
  if (state.search) params.set("search", state.search);
  if (state.category) params.set("category", state.category);

  setStatus("Loading...");
  try {
    const data = await apiGet("/api/products?" + params.toString());
    renderProducts(data.items);
    renderPager(data.total);
    setStatus(data.total === 0 ? "No products found." : `${data.total} product(s) found`);
  } catch (e) {
    grid.innerHTML = "";
    pager.innerHTML = "";
    setStatus("Error: " + e.message, true);
  }
}

function renderProducts(items) {
  grid.innerHTML = items.map(p => `
    <a class="card" href="/product?id=${p.id}">
      <img src="${esc(p.image_url)}" alt="${esc(p.name)}" loading="lazy">
      <div class="card-body">
        <span class="tag">${esc(p.category)}</span>
        <h3 class="card-title">${esc(p.name)}</h3>
        <p class="card-desc">${esc(p.description)}</p>
        <div class="price">${formatPrice(p.price)}</div>
      </div>
    </a>
  `).join("");
}

function renderPager(total) {
  const pages = Math.ceil(total / state.limit);
  pager.innerHTML = "";
  if (pages <= 1) return;
  for (let i = 1; i <= pages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    if (i === state.page) btn.classList.add("active");
    btn.addEventListener("click", () => { state.page = i; loadProducts(); });
    pager.appendChild(btn);
  }
}

function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

document.getElementById("search").addEventListener("input", debounce(e => {
  state.search = e.target.value.trim();
  state.page = 1;
  loadProducts();
}, 300));

document.getElementById("category").addEventListener("change", e => {
  state.category = e.target.value;
  state.page = 1;
  loadProducts();
});

document.getElementById("sort").addEventListener("change", e => {
  state.sort = e.target.value;
  state.page = 1;
  loadProducts();
});

loadCategories();
loadProducts();
