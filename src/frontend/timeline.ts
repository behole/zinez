import { fetchTimeline, type TimelineEntry } from "./api";

export async function renderTimeline(): Promise<void> {
  const canvas = document.getElementById("timeline") as HTMLCanvasElement;
  if (!canvas) return;

  const data = await fetchTimeline();
  if (!data.length) return;

  const ctx = canvas.getContext("2d")!;
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.clientHeight);
  ctx.clearRect(0, 0, w, h);

  const years = data.map((d) => d.year);
  const minY = Math.min(...years);
  const maxY = Math.max(...years);
  const maxC = Math.max(...data.map((d) => d.count));
  const pad = 24;
  const bars = maxY - minY + 1;
  const bw = Math.max(1, (w - pad * 2) / bars);

  const countMap = new Map(data.map((d) => [d.year, d.count]));

  // Bars
  for (let y = minY; y <= maxY; y++) {
    const c = countMap.get(y) || 0;
    const x = pad + (y - minY) * bw;
    const bh = (h - 40) * (c / maxC);
    ctx.fillStyle = c ? "#ff0066" : "#222";
    ctx.fillRect(x, h - 22 - bh, bw - 1, bh);
  }

  // Decade ticks
  ctx.fillStyle = "#9aa0a6";
  ctx.font = "11px system-ui";
  ctx.strokeStyle = "#333";
  ctx.beginPath();
  ctx.moveTo(pad, h - 22);
  ctx.lineTo(w - pad, h - 22);
  ctx.stroke();

  const startDec = Math.floor(minY / 10) * 10;
  const endDec = Math.floor(maxY / 10) * 10;
  for (let d = startDec; d <= endDec; d += 10) {
    const x = pad + (d - minY) * bw;
    ctx.fillRect(x, h - 24, 1, 6);
    ctx.fillText(String(d), x + 2, h - 8);
  }
}
