/**
 * Progressive visual enhancements for PyPath's home page.
 *
 * The lesson platform remains fully usable without JavaScript, WebGL, or a
 * network connection to the pinned Three.js module. The scene is decorative
 * only, and every motion enhancement honours reduced-motion preferences.
 */

const THREE_MODULE_URL =
    "https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.min.js";
const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
const isEnglish = document.documentElement.lang === "en";


function prefersReducedMotion() {
    return reducedMotionQuery.matches;
}


function shouldSkipThreeScene(canvas) {
    const connection = navigator.connection || navigator.mozConnection;
    const supportsWebGL2 =
        typeof WebGL2RenderingContext !== "undefined" &&
        canvas.getContext("webgl2") !== null;

    return (
        prefersReducedMotion() ||
        window.matchMedia("(max-width: 600px)").matches ||
        Boolean(connection?.saveData) ||
        !supportsWebGL2
    );
}


function normalizeSearchText(value) {
    return value
        .normalize("NFD")
        .replace(/\p{Diacritic}/gu, "")
        .toLowerCase()
        .replace(/đ/gu, "d");
}


function setupCurriculumExplorer() {
    const explorer = document.querySelector("[data-curriculum]");

    if (!explorer) {
        return;
    }

    const searchInput = explorer.querySelector("[data-curriculum-search]");
    const status = explorer.querySelector("[data-curriculum-status]");
    const emptyState = explorer.querySelector("[data-curriculum-empty]");
    const filters = [...explorer.querySelectorAll("[data-track-filter]")];
    const sections = [...document.querySelectorAll("[data-track-section]")];
    const totalLessons = document.querySelectorAll("[data-lesson-card]").length;
    let activeTrack = "all";
    let searchTimer;

    document.documentElement.classList.add("has-curriculum-js");

    const applyFilters = () => {
        const query = normalizeSearchText(searchInput.value.trim());
        let visibleLessons = 0;

        sections.forEach((section) => {
            const matchesTrack =
                activeTrack === "all" || section.dataset.track === activeTrack;
            let visibleInSection = 0;

            section.querySelectorAll("[data-lesson-card]").forEach((card) => {
                const matchesQuery = normalizeSearchText(
                    card.dataset.search || "",
                ).includes(query);
                const isVisible = matchesTrack && matchesQuery;
                card.hidden = !isVisible;
                if (isVisible) {
                    visibleInSection += 1;
                    visibleLessons += 1;
                }
            });

            section.hidden = visibleInSection === 0;
            if (visibleInSection && (query || activeTrack !== "all")) {
                section.open = true;
            }
        });

        filters.forEach((filter) => {
            filter.setAttribute(
                "aria-pressed",
                String(filter.dataset.trackFilter === activeTrack),
            );
        });
        status.textContent = isEnglish
            ? `Showing ${visibleLessons} / ${totalLessons} lessons`
            : `Hiển thị ${visibleLessons} / ${totalLessons} bài học`;
        emptyState.hidden = visibleLessons !== 0;
    };

    filters.forEach((filter) => {
        filter.addEventListener("click", () => {
            activeTrack = filter.dataset.trackFilter || "all";
            applyFilters();
        });
    });

    searchInput.addEventListener("input", () => {
        window.clearTimeout(searchTimer);
        searchTimer = window.setTimeout(applyFilters, 80);
    });

    document.querySelectorAll("[data-roadmap-track]").forEach((trackLink) => {
        trackLink.addEventListener("click", () => {
            const trackKey = trackLink.dataset.roadmapTrack;
            const target = sections.find((section) => section.id === trackKey);

            if (!target) {
                return;
            }

            activeTrack = "all";
            searchInput.value = "";
            applyFilters();
            target.hidden = false;
            target.open = true;
        });
    });

    const openHashTarget = () => {
        const key = decodeURIComponent(window.location.hash.slice(1));
        if (!key) {
            return;
        }

        const target = sections.find((section) => section.id === key);
        if (target) {
            target.hidden = false;
            target.open = true;
        }
    };

    window.addEventListener("hashchange", openHashTarget);
    openHashTarget();
    applyFilters();
}


function setupRevealAnimations() {
    const revealItems = [...document.querySelectorAll("[data-reveal]")];

    if (!revealItems.length) {
        return;
    }

    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
        return;
    }

    document.documentElement.classList.add("motion-ready");
    const observer = new IntersectionObserver(
        (entries, activeObserver) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                const position = revealItems.indexOf(entry.target) % 6;
                window.setTimeout(
                    () => entry.target.classList.add("is-visible"),
                    Math.max(position, 0) * 70,
                );
                activeObserver.unobserve(entry.target);
            });
        },
        { threshold: 0.12 },
    );

    revealItems.forEach((item) => observer.observe(item));
}


function setupTerminalTilt() {
    const stage = document.querySelector("[data-three-stage]");
    const terminal = document.querySelector("[data-terminal-card]");

    if (!stage || !terminal || prefersReducedMotion()) {
        return;
    }

    let resetTimer;
    stage.addEventListener("pointermove", (event) => {
        const bounds = stage.getBoundingClientRect();
        const horizontal = (event.clientX - bounds.left) / bounds.width - 0.5;
        const vertical = (event.clientY - bounds.top) / bounds.height - 0.5;

        terminal.style.setProperty("--terminal-rotate-x", `${-vertical * 4}deg`);
        terminal.style.setProperty("--terminal-rotate-y", `${horizontal * 5}deg`);
        window.clearTimeout(resetTimer);
        resetTimer = window.setTimeout(() => {
            terminal.style.setProperty("--terminal-rotate-x", "0deg");
            terminal.style.setProperty("--terminal-rotate-y", "0deg");
        }, 220);
    });

    stage.addEventListener("pointerleave", () => {
        terminal.style.setProperty("--terminal-rotate-x", "0deg");
        terminal.style.setProperty("--terminal-rotate-y", "0deg");
    });
}


function randomBetween(minimum, maximum) {
    return minimum + Math.random() * (maximum - minimum);
}


async function setupThreeHero() {
    const stage = document.querySelector("[data-three-stage]");
    const canvas = document.querySelector("[data-three-hero]");

    if (!stage || !canvas || shouldSkipThreeScene(canvas)) {
        return;
    }

    let THREE;
    try {
        THREE = await import(THREE_MODULE_URL);
    } catch (error) {
        stage.dataset.threeState = "fallback";
        return;
    }

    let renderer;
    try {
        renderer = new THREE.WebGLRenderer({
            alpha: true,
            antialias: false,
            canvas,
            powerPreference: "low-power",
        });
        renderer.setClearColor(0x000000, 0);
    } catch (error) {
        stage.dataset.threeState = "fallback";
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
    camera.position.set(0, 0, 8);

    const constellation = new THREE.Group();
    constellation.position.set(0.45, -0.05, 0);
    scene.add(constellation);

    const nodeGeometry = new THREE.IcosahedronGeometry(0.11, 1);
    const nodeMaterials = [
        new THREE.MeshBasicMaterial({
            color: 0x8c73ff,
            opacity: 0.9,
            transparent: true,
        }),
        new THREE.MeshBasicMaterial({
            color: 0x55d9c6,
            opacity: 0.85,
            transparent: true,
        }),
        new THREE.MeshBasicMaterial({
            color: 0xa7a1ff,
            opacity: 0.78,
            transparent: true,
        }),
    ];
    const nodes = [];
    const linePoints = [];

    for (let index = 0; index < 15; index += 1) {
        const angle = (index / 15) * Math.PI * 2 + randomBetween(-0.13, 0.13);
        const radius = randomBetween(1.25, 2.45);
        const node = new THREE.Mesh(
            nodeGeometry,
            nodeMaterials[index % nodeMaterials.length],
        );
        const position = new THREE.Vector3(
            Math.cos(angle) * radius,
            Math.sin(angle) * radius * 0.72,
            randomBetween(-0.25, 0.25),
        );

        node.position.copy(position);
        node.userData = {
            baseX: position.x,
            baseY: position.y,
            phase: randomBetween(0, Math.PI * 2),
            speed: randomBetween(0.38, 0.72),
        };
        nodes.push(node);
        linePoints.push(position);
        constellation.add(node);
    }

    const lineGeometry = new THREE.BufferGeometry().setFromPoints(linePoints);
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x9086f5,
        opacity: 0.28,
        transparent: true,
    });
    constellation.add(new THREE.LineLoop(lineGeometry, lineMaterial));

    const ring = new THREE.Mesh(
        new THREE.TorusGeometry(2.25, 0.012, 6, 100),
        new THREE.MeshBasicMaterial({
            color: 0x5cdbc6,
            opacity: 0.32,
            transparent: true,
        }),
    );
    ring.rotation.set(0.66, -0.33, -0.38);
    constellation.add(ring);

    const particlesGeometry = new THREE.BufferGeometry();
    const particles = new Float32Array(72 * 3);
    for (let index = 0; index < particles.length; index += 3) {
        particles[index] = randomBetween(-3.35, 3.35);
        particles[index + 1] = randomBetween(-2.6, 2.6);
        particles[index + 2] = randomBetween(-1.4, 0.4);
    }
    particlesGeometry.setAttribute(
        "position",
        new THREE.BufferAttribute(particles, 3),
    );
    const particleMaterial = new THREE.PointsMaterial({
        color: 0x9d94ff,
        opacity: 0.6,
        size: 0.025,
        sizeAttenuation: true,
        transparent: true,
    });
    const particleCloud = new THREE.Points(particlesGeometry, particleMaterial);
    scene.add(particleCloud);

    const pointerTarget = new THREE.Vector2();
    const pointerCurrent = new THREE.Vector2();
    stage.addEventListener("pointermove", (event) => {
        const bounds = stage.getBoundingClientRect();
        pointerTarget.set(
            ((event.clientX - bounds.left) / bounds.width - 0.5) * 0.54,
            -((event.clientY - bounds.top) / bounds.height - 0.5) * 0.38,
        );
    });
    stage.addEventListener("pointerleave", () => pointerTarget.set(0, 0));

    const resizeScene = () => {
        const { height, width } = stage.getBoundingClientRect();
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    };

    resizeScene();
    const resizeObserver = new ResizeObserver(resizeScene);
    resizeObserver.observe(stage);
    stage.dataset.threeState = "ready";
    stage.classList.add("is-three-ready");

    let animationFrame;
    let sceneIsVisible = true;
    let lastTimestamp = performance.now();

    const renderFrame = (timestamp) => {
        if (!sceneIsVisible || document.hidden) {
            animationFrame = undefined;
            return;
        }

        const elapsed = timestamp * 0.001;
        const delta = Math.min((timestamp - lastTimestamp) * 0.001, 0.05);
        lastTimestamp = timestamp;
        pointerCurrent.lerp(pointerTarget, Math.min(delta * 5, 1));
        constellation.rotation.y += delta * 0.12;
        constellation.rotation.x =
            pointerCurrent.y * 0.45 + Math.sin(elapsed * 0.35) * 0.08;
        constellation.rotation.z = pointerCurrent.x * 0.28;
        constellation.position.x = 0.45 + pointerCurrent.x * 0.82;
        constellation.position.y = -0.05 + pointerCurrent.y * 0.62;
        ring.rotation.z += delta * 0.12;
        particleCloud.rotation.z -= delta * 0.015;

        nodes.forEach((node) => {
            const { baseX, baseY, phase, speed } = node.userData;
            node.position.x = baseX + Math.cos(elapsed * speed + phase) * 0.05;
            node.position.y = baseY + Math.sin(elapsed * speed + phase) * 0.08;
            node.rotation.x += delta * speed;
            node.rotation.y += delta * (speed * 0.7);
        });

        renderer.render(scene, camera);
        animationFrame = window.requestAnimationFrame(renderFrame);
    };

    const resumeScene = () => {
        if (sceneIsVisible && !document.hidden && !animationFrame) {
            lastTimestamp = performance.now();
            animationFrame = window.requestAnimationFrame(renderFrame);
        }
    };

    const visibilityObserver = new IntersectionObserver(
        ([entry]) => {
            sceneIsVisible = entry.isIntersecting;
            resumeScene();
        },
        { threshold: 0.02 },
    );
    visibilityObserver.observe(stage);
    document.addEventListener("visibilitychange", resumeScene);
    resumeScene();

    window.addEventListener(
        "pagehide",
        () => {
            if (animationFrame) {
                window.cancelAnimationFrame(animationFrame);
            }
            visibilityObserver.disconnect();
            resizeObserver.disconnect();
            nodeGeometry.dispose();
            nodeMaterials.forEach((material) => material.dispose());
            lineGeometry.dispose();
            lineMaterial.dispose();
            ring.geometry.dispose();
            ring.material.dispose();
            particlesGeometry.dispose();
            particleMaterial.dispose();
            renderer.dispose();
        },
        { once: true },
    );
}


function startEnhancements() {
    setupCurriculumExplorer();
    setupRevealAnimations();
    setupTerminalTilt();
    void setupThreeHero();
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startEnhancements, { once: true });
} else {
    startEnhancements();
}
