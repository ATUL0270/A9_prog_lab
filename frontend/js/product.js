// Product details page: reads ?id= from the URL and calls the API.

const detail = document.getElementById("detail");

async function loadProduct() {
  const id = new URLSearchParams(window.location.search).get("id");
  if (!id) {
    setStatus("No product specified.", true);
    return;
  }

  setStatus("Loading...");
  try {
    const p = await apiGet("/api/products/" + encodeURIComponent(id));
    document.title = p.name + " - ShopEasy";
    setStatus("");
    detail.innerHTML = `
      <img src="${esc(p.image_url)}" alt="${esc(p.name)}">
      <div>
        <span class="tag">${esc(p.category)}</span>
        <h1>${esc(p.name)}</h1>
        <p>${esc(p.description)}</p>
        <div class="price">${formatPrice(p.price)}</div>
        <p class="${p.stock > 0 ? "stock-in" : "stock-out"}">
          ${p.stock > 0 ? `In stock (${p.stock} available)` : "Out of stock"}
        </p>
      </div>
    `;
  } catch (e) {
    detail.innerHTML = "";
    setStatus(e.status === 404 ? "Product not found." : "Error: " + e.message, true);
  }
}

loadProduct();
