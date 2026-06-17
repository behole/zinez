import type { Zine } from "./api";

let lbZines: Zine[] = [];
let lbIdx = 0;
let zoom = 1;
let panX = 0;
let panY = 0;
let dragging = false;
let dragStartX = 0;
let dragStartY = 0;

const $ = (id: string) => document.getElementById(id);

function applyTransform(): void {
  const img = $("lb-image") as HTMLImageElement;
  if (img) img.style.transform = `scale(${zoom}) translate(${panX}px, ${panY}px)`;
}

function resetZoom(): void {
  zoom = 1;
  panX = 0;
  panY = 0;
  applyTransform();
}

function show(zines: Zine[], idx: number): void {
  lbZines = zines;
  lbIdx = idx;
  const z = zines[idx];
  if (!z) return;

  const title = [z.zine_name, z.issue_number && `#${z.issue_number}`].filter(Boolean).join(" ");
  const titleEl = $("lb-title");
  if (titleEl) titleEl.textContent = title;

  const img = $("lb-image") as HTMLImageElement;
  if (img) {
    const thumb = z.ia_thumb || z.image_url || "";
    let highRes = "";
    if (z.ia_item_url) {
      const match = z.ia_item_url.match(/\/details\/([^/?]+)/);
      if (match) highRes = `https://archive.org/download/${match[1]}/page/n0_w1600.jpg`;
    }

    img.onerror = null;
    img.alt = title;
    img.classList.remove("lb-loading");

    if (thumb) {
      img.src = thumb;
      if (highRes && highRes !== thumb) {
        img.classList.add("lb-loading");
        const preload = new Image();
        preload.onload = () => {
          img.src = highRes;
          img.classList.remove("lb-loading");
        };
        preload.onerror = () => img.classList.remove("lb-loading");
        preload.src = highRes;
      }
    } else if (highRes) {
      img.src = highRes;
    } else {
      img.removeAttribute("src");
    }
  }

  const link = $("lb-origin") as HTMLAnchorElement;
  if (link) link.href = z.ia_item_url ? `${z.ia_item_url}/mode/2up` : z.image_url || "#";

  const idVal = $("lb-idval");
  if (idVal) idVal.textContent = z.id;

  resetZoom();
  const lb = $("lightbox");
  if (lb) lb.hidden = false;
}

function close(): void {
  const lb = $("lightbox");
  if (lb) lb.hidden = true;
  resetZoom();
}

function nav(dir: number): void {
  if (!lbZines.length) return;
  lbIdx = (lbIdx + dir + lbZines.length) % lbZines.length;
  show(lbZines, lbIdx);
}

export function initLightbox(): void {
  $("lb-close")?.addEventListener("click", close);
  $("lb-prev")?.addEventListener("click", () => nav(-1));
  $("lb-next")?.addEventListener("click", () => nav(1));
  $("lb-zoom-in")?.addEventListener("click", () => {
    zoom = Math.min(zoom * 1.3, 10);
    applyTransform();
  });
  $("lb-zoom-out")?.addEventListener("click", () => {
    zoom = Math.max(zoom / 1.3, 1);
    if (zoom === 1) { panX = 0; panY = 0; }
    applyTransform();
  });
  $("lb-reset")?.addEventListener("click", resetZoom);


  // Close on backdrop click
  $("lightbox")?.addEventListener("click", (e) => {
    if ((e.target as HTMLElement).id === "lightbox") close();
  });
  // Pan/drag (mouse + touch)
  const container = $("lb-img-container");
  if (container) {
    const startDrag = (cx: number, cy: number) => {
      if (zoom > 1) {
        dragging = true;
        dragStartX = cx - panX;
        dragStartY = cy - panY;
        container.classList.add("dragging");
      }
    };

    container.addEventListener("mousedown", (e) => {
      startDrag(e.clientX, e.clientY);
      if (dragging) e.preventDefault();
    });

    container.addEventListener("touchstart", (e) => {
      if (e.touches.length === 1) {
        startDrag(e.touches[0].clientX, e.touches[0].clientY);
        if (dragging) e.preventDefault();
      }
    }, { passive: false });

    const moveDrag = (cx: number, cy: number) => {
      if (dragging) {
        panX = cx - dragStartX;
        panY = cy - dragStartY;
        applyTransform();
      }
    };

    document.addEventListener("mousemove", (e) => moveDrag(e.clientX, e.clientY));

    document.addEventListener("touchmove", (e) => {
      if (e.touches.length === 1) moveDrag(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: false });

    const endDrag = () => {
      if (dragging) {
        dragging = false;
        container.classList.remove("dragging");
      }
    };

    document.addEventListener("mouseup", endDrag);
    document.addEventListener("touchend", endDrag);
  }

  // Keyboard
  document.addEventListener("keydown", (e) => {
    const lb = $("lightbox");
    if (!lb || lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") nav(1);
    if (e.key === "ArrowLeft") nav(-1);
  });
}

export function openLightbox(zines: Zine[], idx: number): void {
  show(zines, idx);
}
