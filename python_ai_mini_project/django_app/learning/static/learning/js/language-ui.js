/* Client-side copy for the compact VI/EN interface switcher.
 * Lesson data is deliberately not machine-translated: technical lesson text
 * stays in its authored language until an editorial translation is supplied.
 */

const englishCopy = {
  ".roadmap-overview__header .eyebrow": "● Capability roadmap",
  ".roadmap-overview__header h2": "From Python foundations to an <em>ML Engineer portfolio.</em>",
  ".roadmap-overview__header p:not(.eyebrow)": "Six capability stages take you from code and math foundations to building, deploying, and operating AI products.",
  ".roadmap-overview__jump": "Browse all lessons ↓",
  ".lesson-body__label": "LESSON CONTENT",
  ".lesson-visual__eyebrow": "QUICK VISUAL",
  ".concept-map__header .eyebrow": "UNDERSTAND THE WHY",
  ".concept-map__header h2": "The mental model for this lesson",
  ".sidebar-card__heading h2": "Practice now",
};

function applyEnglishInterface() {
  if (document.documentElement.lang !== "en") {
    return;
  }

  Object.entries(englishCopy).forEach(([selector, value]) => {
    document.querySelectorAll(selector).forEach((element) => {
      element.innerHTML = value;
    });
  });

  document.querySelectorAll(".roadmap-stage__metric").forEach((element) => {
    element.textContent = element.textContent.replace(/bài/g, "lessons");
  });
}

document.addEventListener("DOMContentLoaded", applyEnglishInterface);
