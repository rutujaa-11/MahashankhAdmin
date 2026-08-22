/* ============================================================
   MAHASHANKH ADMIN THEME TOGGLE & UI FIXES (COMPLETE JS)
   ============================================================ */

(function () {
    "use strict";

    const STORAGE_KEY = "mahashankh_admin_theme";

    function getTheme() {
        return localStorage.getItem(STORAGE_KEY) || "light";
    }

    function updateButton() {
        const button = document.getElementById("mh-theme-toggle");
        if (!button) return;

        const icon = button.querySelector("i");
        if (!icon) return;

        const dark = document.documentElement.classList.contains("mh-dark");
        if (dark) {
            icon.className = "fa-solid fa-sun";
            button.title = "Switch to Light Mode";
        } else {
            icon.className = "fa-solid fa-moon";
            button.title = "Switch to Dark Mode";
        }
    }

    /* 1. Force Pure White Color on Sidebar Elements */
    function forceSidebarWhiteText() {
        const sidebarElements = document.querySelectorAll(`
            .main-sidebar, .main-sidebar *, 
            .sidebar, .sidebar *, 
            .user-panel, .user-panel *,
            .nav-sidebar, .nav-sidebar *, 
            .nav-link, .nav-link *, 
            .nav-header, .mah-section-heading,
            .brand-link, .brand-link *
        `);

        sidebarElements.forEach(el => {
            el.style.setProperty('color', '#ffffff', 'important');
            el.style.setProperty('opacity', '1', 'important');
            
            if (el.tagName === 'I' || el.tagName === 'SVG' || el.tagName === 'PATH') {
                el.style.setProperty('fill', '#ffffff', 'important');
            }
        });
    }

    /* 2. Target Top Right Navbar Icons & Force Dark Brown in Light Mode / White in Dark Mode */
    function forceNavbarIconsVisible() {
        const dark = document.documentElement.classList.contains("mh-dark");
        const targetColor = dark ? "#ffffff" : "#3f281c";

        const navElements = document.querySelectorAll(`
            .main-header i, 
            .main-header svg, 
            .main-header path, 
            .main-header a, 
            .main-header span,
            .main-header .nav-link,
            .main-header .navbar-nav.ml-auto *,
            .main-header .navbar-custom-menu *,
            .main-header .user-menu *
        `);

        navElements.forEach(el => {
            el.style.setProperty('color', targetColor, 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('visibility', 'visible', 'important');

            if (el.tagName === 'I' || el.tagName === 'SVG' || el.tagName === 'PATH') {
                el.style.setProperty('fill', targetColor, 'important');
            }
        });

        /* Handle avatar/image icon if used by admin framework */
        const imgs = document.querySelectorAll('.main-header img');
        imgs.forEach(img => {
            if (dark) {
                img.style.removeProperty('filter');
            } else {
                img.style.setProperty('filter', 'brightness(0.2)', 'important');
            }
        });
    }

    /* 3. Fix Overlapping Titles & Chart Headers */
    function fixChartTitleOverlap() {
        const headers = document.querySelectorAll('.card-header, div[class*="header"], .dashboard-card-header');
        headers.forEach(header => {
            header.style.setProperty('display', 'flex', 'important');
            header.style.setProperty('flex-direction', 'column', 'important');
            header.style.setProperty('align-items', 'flex-start', 'important');
        });

        const subtitles = document.querySelectorAll('.card-header small, .card-header .text-muted, .dashboard-card-header span, .card-title + small');
        subtitles.forEach(sub => {
            sub.style.setProperty('display', 'block', 'important');
            sub.style.setProperty('margin-top', '4px', 'important');
            sub.style.setProperty('position', 'relative', 'important');
            sub.style.setProperty('clear', 'both', 'important');
        });
    }

    /* 4. Force Dark Background on Inline Elements and Headers */
    function forceDarkElements() {
        const dark = document.documentElement.classList.contains("mh-dark");
        const targets = document.querySelectorAll(`
            .content-header, .dashboard-header, header, div[class*="header"], 
            .card-header, .stat-icon, .icon-box, .stat-card span, 
            .stat-card div, div[class*="icon"], div[class*="box"]
        `);

        targets.forEach(el => {
            if (dark) {
                const computed = window.getComputedStyle(el);
                if (computed.backgroundColor === "rgb(255, 255, 255)" || computed.backgroundColor === "rgba(0, 0, 0, 0)" || computed.backgroundColor === "rgb(248, 249, 250)") {
                    el.style.setProperty('background-color', '#2c2520', 'important');
                    el.style.setProperty('background', '#2c2520', 'important');
                    el.style.setProperty('border-color', '#40352d', 'important');
                }
            } else {
                el.style.removeProperty('background-color');
                el.style.removeProperty('background');
                el.style.removeProperty('border-color');
            }
        });

        forceSidebarWhiteText();
        forceNavbarIconsVisible();
        fixChartTitleOverlap();
    }

    /* 5. Update Chart Theme Colors */
    function updateChartsTheme(dark) {
        const textColor = dark ? "#f2ebe4" : "#666666";
        const gridColor = dark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";

        if (window.Chart) {
            if (window.Chart.defaults) {
                if (window.Chart.defaults.color !== undefined) {
                    window.Chart.defaults.color = textColor;
                }
                if (window.Chart.defaults.scale && window.Chart.defaults.scale.grid) {
                    window.Chart.defaults.scale.grid.color = gridColor;
                }
            }
            
            if (window.Chart.instances) {
                Object.keys(window.Chart.instances).forEach(id => {
                    const chart = window.Chart.instances[id];
                    if (chart.options && chart.options.scales) {
                        Object.keys(chart.options.scales).forEach(scaleKey => {
                            const scale = chart.options.scales[scaleKey];
                            if (scale.ticks) scale.ticks.color = textColor;
                            if (scale.grid) scale.grid.color = gridColor;
                        });
                    }
                    chart.update();
                });
            }
        }
    }

    function applyTheme(theme) {
        const dark = (theme === "dark");
        const html = document.documentElement;

        if (dark) {
            html.classList.add("mh-dark");
        } else {
            html.classList.remove("mh-dark");
        }

        updateButton();
        forceDarkElements();
        updateChartsTheme(dark);
    }

    function createButton() {
        if (document.getElementById("mh-theme-toggle")) return;

        const button = document.createElement("button");
        button.id = "mh-theme-toggle";
        button.type = "button";
        button.innerHTML = '<i class="fa-solid fa-moon"></i>';
        button.setAttribute("aria-label", "Toggle dark mode");

        button.addEventListener("click", function () {
            const dark = document.documentElement.classList.contains("mh-dark");
            const newTheme = dark ? "light" : "dark";
            localStorage.setItem(STORAGE_KEY, newTheme);
            applyTheme(newTheme);
        });

        document.body.appendChild(button);
        updateButton();
    }

    function initTheme() {
        const theme = getTheme();
        applyTheme(theme);
        createButton();

        const observer = new MutationObserver(() => {
            forceSidebarWhiteText();
            forceNavbarIconsVisible();
            fixChartTitleOverlap();
        });
        
        const headerNode = document.querySelector(".main-header") || document.body;
        if (headerNode) {
            observer.observe(headerNode, { childList: true, subtree: true });
        }

        /* Periodic checks for dynamically loaded dashboard widgets */
        setInterval(() => {
            forceNavbarIconsVisible();
            fixChartTitleOverlap();
        }, 1500);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initTheme);
    } else {
        initTheme();
    }
})();