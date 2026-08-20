/** Keep compact navigation popovers mutually exclusive and easy to dismiss. */

document.addEventListener("DOMContentLoaded", () => {
  const menus = [...document.querySelectorAll(".nav-menu")];

  menus.forEach((menu) => {
    menu.addEventListener("toggle", () => {
      if (!menu.open) {
        return;
      }
      menus.forEach((otherMenu) => {
        if (otherMenu !== menu) {
          otherMenu.open = false;
        }
      });
    });
  });

  document.addEventListener("pointerdown", (event) => {
    if (menus.some((menu) => menu.contains(event.target))) {
      return;
    }
    menus.forEach((menu) => {
      menu.open = false;
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    menus.forEach((menu) => {
      menu.open = false;
    });
  });
});
