export interface FilterState {
  q: string;
  decade: string;
  sort: string;
  page: number;
}

export function createFilterState(): FilterState {
  return { q: "", decade: "all", sort: "name_asc", page: 1 };
}

export function initFilters(
  state: FilterState,
  onChange: () => void
): void {
  const input = document.getElementById("q") as HTMLInputElement;
  const sortSelect = document.getElementById("sort") as HTMLSelectElement;
  const decadeButtons = document.querySelectorAll<HTMLButtonElement>("[data-decade]");

  let debounceTimer: ReturnType<typeof setTimeout>;

  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      state.q = input.value.trim();
      state.page = 1;
      onChange();
    }, 300);
  });

  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    state.page = 1;
    onChange();
  });

  decadeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      decadeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.decade = btn.dataset.decade || "all";
      state.page = 1;
      onChange();
    });
  });
}
