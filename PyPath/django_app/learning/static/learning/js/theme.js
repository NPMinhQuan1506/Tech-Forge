/** Persist a light/dark presentation preference without changing lesson data. */

const themeStorageKey = "pypath-theme";

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelectorAll("[data-theme-value]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.themeValue === theme));
  });
  document.querySelectorAll("[data-theme-icon]").forEach((icon) => {
    icon.textContent = theme === "dark" ? "☾" : "☀";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem(themeStorageKey);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

  document.querySelectorAll("[data-theme-value]").forEach((button) => {
    button.addEventListener("click", () => {
      const theme = button.dataset.themeValue;
      localStorage.setItem(themeStorageKey, theme);
      applyTheme(theme);
      button.closest("details").open = false;
    });
  });
});
