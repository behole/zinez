import "./style.css";
import { fetchZines, type Zine, type ZineListResponse } from "./api";
import { createFilterState, initFilters } from "./filters";
import { renderTimeline } from "./timeline";
import { initLightbox, openLightbox, getThumbUrl } from "./lightbox";

const state = createFilterState();
let currentData: ZineListResponse | null = null;
let loading = false;

async function sync(): Promise<void> {
  if (loading) return;
  loading = true;

  const loader = document.getElementById("loader")!;
  loader.hidden = false;

  try {
    clearError();
    currentData = await fetchZines({
      q: state.q,
      decade: state.decade,
      sort: state.sort,
      page: state.page,
      limit: 50,
    });

    renderStats(currentData);
    renderGrid(currentData.zines);
  } catch (err) {
    showError(`Failed to load: ${err instanceof Error ? err.message : "Unknown error"}. Tap to retry.`);
  } finally {
    loading = false;
    loader.hidden = true;
  }
}

function renderStats(data: ZineListResponse): void {
  const el = document.getElementById("stats")!;
  el.textContent = `${data.total} zines found · page ${data.page} of ${data.pages}`;
}


function renderCard(z: Zine): string {
  const thumb = getThumbUrl(z);
  const title = [z.zine_name, z.issue_number && `#${z.issue_number}`].filter(Boolean).join(" ");
  const locyr = [z.location, z.year].filter(Boolean).join(" · ");
  const tags = z.tags.slice(0, 4).map((t) => `<span class="tag">${t}</span>`).join("");

  return `<article class="card" data-id="${z.id}">
    <div class="thumb">${
      thumb
        ? `<img data-src="${thumb}" alt="${title}" />`
        : `<div class="ph">No image</div>`
    }</div>
    <div class="meta">
      <div class="title">${title}</div>
      <div class="small">${locyr}</div>
      ${tags ? `<div class="tags">${tags}</div>` : ""}
    </div>
  </article>`;
}

function attachCardClickHandlers(container: HTMLElement, ids?: Set<string>): void {
  container.querySelectorAll<HTMLElement>(".card").forEach((card) => {
    if (ids && !ids.has(card.dataset.id!)) return;
    card.addEventListener("click", () => {
      if (!currentData) return;
      const id = card.dataset.id;
      const idx = currentData.zines.findIndex((z) => z.id === id);
      if (idx >= 0) openLightbox(currentData.zines, idx);
    });
  });
}

function showError(msg: string): void {
  const el = document.getElementById("error")!;
  el.textContent = msg;
  el.hidden = false;
}

function clearError(): void {
  const el = document.getElementById("error");
  if (el) el.hidden = true;
}
function renderGrid(zines: Zine[]): void {
  const grid = document.getElementById("grid")!;
  grid.innerHTML = zines.map(renderCard).join("");

  observeImages(grid);
  attachCardClickHandlers(grid);
  setupInfiniteScroll();
}

function observeImages(container: HTMLElement): void {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          const src = img.dataset.src;
          if (src) {
            img.src = src;
            img.onload = () => img.classList.add("loaded");
            img.onerror = () => {
              img.removeAttribute("src");
              img.closest(".thumb")!.innerHTML = `<div class="ph">No image</div>`;
            };
          }
          observer.unobserve(img);
        }
      });
    },
    { rootMargin: "200px" }
  );

  container.querySelectorAll<HTMLImageElement>("img[data-src]").forEach((img) => {
    observer.observe(img);
  });
}

function setupInfiniteScroll(): void {
  // Remove existing listener to avoid duplicates
  window.removeEventListener("scroll", handleScroll);
  window.addEventListener("scroll", handleScroll);
}

async function handleScroll(): Promise<void> {
  if (!currentData || loading) return;
  if (state.page >= currentData.pages) return;

  const scrollBottom = window.innerHeight + window.scrollY;
  const docHeight = document.documentElement.scrollHeight;

  if (docHeight - scrollBottom < 400) {
    state.page++;
    loading = true;
    const loader = document.getElementById("loader")!;
    loader.hidden = false;

    try {
      const more = await fetchZines({
        q: state.q,
        decade: state.decade,
        sort: state.sort,
        page: state.page,
        limit: 50,
      });

      currentData.page = more.page;
      currentData.zines = [...currentData.zines, ...more.zines];
      const grid = document.getElementById("grid")!;
      const fragment = document.createElement("div");
      fragment.innerHTML = more.zines.map(renderCard).join("");
      const newIds = new Set(more.zines.map((z) => z.id));

      while (fragment.firstElementChild) {
        grid.appendChild(fragment.firstElementChild);
      }

      observeImages(grid);
      attachCardClickHandlers(grid, newIds);
      renderStats(currentData);
    } catch (err) {
      state.page--;
      showError(`Failed to load more: ${err instanceof Error ? err.message : "Unknown error"}. Scroll to retry.`);
    } finally {
      loading = false;
      loader.hidden = true;
    }
  }
}

// Boot
document.addEventListener("DOMContentLoaded", () => {
  initFilters(state, () => sync());
  initLightbox();
  renderTimeline();
  sync();

  document.getElementById("error")?.addEventListener("click", () => sync());
});
