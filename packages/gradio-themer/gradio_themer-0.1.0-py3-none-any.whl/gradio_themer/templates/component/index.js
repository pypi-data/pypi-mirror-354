const { SvelteComponent: tt, init: ot, safe_not_equal: rt } = window.__gradio__svelte__internal, { createEventDispatcher: et, onMount: nt } = window.__gradio__svelte__internal;
function at(T, A, g) {
  const $ = "", _ = [];
  let { value: s = null } = A, { gradio: y = void 0 } = A;
  const C = et(), Y = [
    {
      name: "Inter",
      family: "Inter, sans-serif"
    },
    {
      name: "System",
      family: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    },
    {
      name: "Roboto",
      family: "Roboto, sans-serif"
    },
    {
      name: "Open Sans",
      family: "'Open Sans', sans-serif"
    },
    { name: "Lato", family: "Lato, sans-serif" },
    {
      name: "Poppins",
      family: "Poppins, sans-serif"
    },
    {
      name: "Montserrat",
      family: "Montserrat, sans-serif"
    },
    {
      name: "Source Sans Pro",
      family: "'Source Sans Pro', sans-serif"
    },
    {
      name: "Ubuntu",
      family: "Ubuntu, sans-serif"
    },
    {
      name: "Nunito",
      family: "Nunito, sans-serif"
    }
  ];
  let f = "light", h = {}, v = [], I = !1;
  function n(r, a) {
    console.log(`[Gradio Themer] ${r}`, a || ""), y && y.dispatch("log", { message: r, data: a });
  }
  function j(r) {
    n(`Loading Stable Font: ${r.name || r.family}`, r);
    const a = r.family, i = r.name || a;
    n(`Using stable font: ${a}`), V(a, i);
  }
  function V(r, a) {
    n(`Applying stable system font: ${a}`), W();
    const i = `
      /* COMPLETE FONT OVERRIDE - NO GRADIO FONT LOADING */
      
      /* Override all possible font CSS variables */
      :root, html, body, .gradio-container {
        --font: ${a}, sans-serif !important;
        --font-family: ${a}, sans-serif !important;
        --theme-font-family: ${a}, sans-serif !important;
        --font-sans: ${a}, sans-serif !important;
        --font-mono: monospace !important;
        --body-font-family: ${a}, sans-serif !important;
        --text-font-family: ${a}, sans-serif !important;
      }
      
      /* Block any @font-face rules */
      @media all {
        @font-face {
          font-family: 'ui-sans-serif';
          src: local('${a}');
        }
        @font-face {
          font-family: 'system-ui';
          src: local('${a}');
        }
      }
      
      /* Universal font application with maximum specificity */
      html, body,
      html *, body *,
      .gradio-container,
      .gradio-container *,
      [class*="gr-"],
      [class*="svelte-"],
      input, button, textarea, select, label, span, div, p, h1, h2, h3, h4, h5, h6,
      * {
        font-family: ${a}, sans-serif !important;
        font-size: inherit !important;
      }
    `, c = document.getElementById("gradio-font-stable");
    c && c.remove();
    const l = document.createElement("style");
    l.id = "gradio-font-stable", l.textContent = i, document.head.appendChild(l), n(`✅ Stable system font ${a} applied (no font loading conflicts)`);
  }
  function W() {
    if (document.querySelectorAll('link[href*="/static/fonts/"]').forEach((a) => a.remove()), !window.gradioFontBlocked) {
      const a = document.head.appendChild;
      document.head.appendChild = function(i) {
        return i instanceof HTMLLinkElement && i.href && i.href.includes("/static/fonts/") ? (n(`🚫 BLOCKED Gradio font loading: ${i.href}`), i) : a.call(this, i);
      }, window.gradioFontBlocked = !0, n("🚫 Gradio font loading blocked");
    }
  }
  function M(r) {
    if (n(`Switching to theme: ${r}`), g(4, f = r), h && h[r]) {
      n(`Applying user theme: ${r}`, h[r]), z(h[r]);
      return;
    }
    n(`Applying basic theme: ${r} (no custom configuration found)`), K(r);
  }
  function z(r) {
    n(`Applying theme colors for: ${r.name}`);
    const a = document.getElementById("gradio-custom-theme");
    a && a.remove(), r.font && j(r.font);
    let i = `:root {
`;
    for (const [p, b] of Object.entries(r.colors))
      i += `  --color-${p}: ${b};
`;
    if (r.font) {
      const p = r.font.family, b = `"${p}", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"`;
      i += `  --font-family: ${b};
`, i += `  --font: ${b};
`, i += `  --theme-font-family: "${p}";
`, n(`Setting font CSS variables to: "${p}" with comprehensive fallbacks`);
    } else
      n("No font configuration found in theme config");
    i += `}
`;
    const c = i + `
      /* ===== DYNAMIC THEME APPLICATION ===== */
      
      /* ULTRA HIGH SPECIFICITY - FORCE THEME BACKGROUND */
      html body,
      html body .gradio-container,
      html body .gradio-container .app,
      html body .gradio-container #root,
      html body .gradio-app,
      html body .gradio-interface,
      html body main,
      body,
      html,
      #root,
      .gradio-container,
      .app,
      .gradio-app,
      .gradio-interface,
      main {
        background: ${r.background} !important;
        background-color: ${r.background} !important;
        color: var(--color-base-content) !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }
      
      /* ULTRA HIGH SPECIFICITY TABS */
      html body .gradio-container .gr-tab-nav,
      html body .gradio-container [role="tablist"],
      .gr-tab-nav,
      [role="tablist"] {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
        border: none !important;
        margin-bottom: 0 !important;
      }
      
      html body .gradio-container button[role="tab"],
      html body button[role="tab"],
      button[role="tab"] {
        background: transparent !important;
        background-color: transparent !important;
        color: var(--color-base-content) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0.25rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        opacity: 0.7 !important;
      }
      
      html body .gradio-container button[role="tab"]:hover,
      html body button[role="tab"]:hover,
      button[role="tab"]:hover {
        background: var(--color-base-200) !important;
        background-color: var(--color-base-200) !important;
        opacity: 1 !important;
      }
      
      html body .gradio-container button[role="tab"][aria-selected="true"],
      html body button[role="tab"][aria-selected="true"],
      button[role="tab"][aria-selected="true"] {
        background: var(--color-primary) !important;
        background-color: var(--color-primary) !important;
        color: var(--color-primary-content) !important;
        opacity: 1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
      }
      
      /* ULTRA HIGH SPECIFICITY CONTENT */
      html body .gradio-container .gr-tabitem,
      html body .gr-tabitem,
      .gr-tabitem {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
        border: none !important;
        margin-top: 0 !important;
      }
      
      /* ULTRA HIGH SPECIFICITY INPUTS */
      html body .gradio-container input,
      html body .gradio-container textarea,
      html body .gradio-container select,
      html body input,
      html body textarea,
      html body select,
      input,
      textarea,
      select {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        border: 1px solid var(--color-base-300) !important;
        color: var(--color-base-content) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
      }
      
      /* ULTRA HIGH SPECIFICITY BUTTONS */
      html body .gradio-container button,
      html body .gradio-container .gr-button,
      html body button,
      html body .gr-button,
      button,
      .gr-button {
        background: var(--color-primary) !important;
        background-color: var(--color-primary) !important;
        color: var(--color-primary-content) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
        cursor: pointer !important;
      }
      
      html body .gradio-container button:hover,
      html body .gradio-container .gr-button:hover,
      html body button:hover,
      html body .gr-button:hover,
      button:hover,
      .gr-button:hover {
        background: var(--color-accent) !important;
        background-color: var(--color-accent) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
      }
      
      /* ULTRA HIGH SPECIFICITY HEADERS */
      html body .gradio-container h1,
      html body .gradio-container h2,
      html body .gradio-container h3,
      html body .gradio-container h4,
      html body .gradio-container h5,
      html body .gradio-container h6,
      html body h1,
      html body h2,
      html body h3,
      html body h4,
      html body h5,
      h6 {
        color: var(--color-base-content) !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - BLOCK CLASS ELEMENTS */
      html body .gradio-container .block,
      html body .block,
      .block {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        color: var(--color-base-content) !important;
        border: 1px solid var(--color-base-300) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
      }
      
      /* REMOVE MARKER HIGHLIGHTING */
      html body ::marker,
      ::marker {
        color: transparent !important;
        background: transparent !important;
        content: none !important;
      }
      
      /* REMOVE LIST MARKERS ENTIRELY */
      html body ul,
      html body ol,
      html body li,
      ul,
      ol,
      li {
        list-style: none !important;
        list-style-type: none !important;
        list-style-image: none !important;
        list-style-position: outside !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - FORM CLASS ELEMENTS */
      html body .gradio-container .form,
      html body .form,
      .form {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        color: var(--color-base-content) !important;
        border: 1px solid var(--color-base-300) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - LABELS */
      html body .gradio-container label,
      html body .gradio-container [data-testid*="label"],
      html body .gradio-container .label,
      html body label,
      html body [data-testid*="label"],
      html body .label,
      label,
      [data-testid*="label"],
      .label {
        color: var(--color-base-content) !important;
        background: transparent !important;
        background-color: transparent !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - CODE ELEMENTS */
      html body .gradio-container code,
      html body .gradio-container pre,
      html body .gradio-container .code,
      html body code,
      html body pre,
      html body .code,
      code,
      pre,
      .code {
        background: var(--color-base-200) !important;
        background-color: var(--color-base-200) !important;
        color: var(--color-base-content) !important;
        border: 1px solid var(--color-base-300) !important;
        border-radius: 4px !important;
        padding: 0.25rem 0.5rem !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-size: 0.875rem !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - STRONG/BOLD ELEMENTS */
      html body .gradio-container strong,
      html body .gradio-container b,
      html body strong,
      html body b,
      strong,
      b {
        color: var(--color-base-content) !important;
        font-weight: 700 !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - SPANS AND TEXT ELEMENTS */
      html body .gradio-container span,
      html body .gradio-container p,
      html body .gradio-container div,
      html body span,
      html body p,
      html body div,
      span,
      p,
      div {
        color: var(--color-base-content) !important;
        font-family: var(--theme-font-family, "Inter"), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - SVG ICONS */
      html body .gradio-container svg,
      html body svg,
      svg {
        color: var(--color-base-content) !important;
        fill: currentColor !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - GRADIO SPECIFIC CLASSES */
      html body .gradio-container .gr-textbox,
      html body .gradio-container .gr-dropdown,
      html body .gradio-container .gr-slider,
      html body .gradio-container .gr-checkbox,
      html body .gradio-container .gr-radio,
      html body .gradio-container .gr-number,
      html body .gradio-container .gr-file,
      html body .gradio-container .gr-image,
      html body .gradio-container .gr-audio,
      html body .gradio-container .gr-video,
      html body .gradio-container .gr-dataframe,
      html body .gradio-container .gr-plot,
      html body .gradio-container .gr-json,
      html body .gradio-container .gr-html,
      html body .gradio-container .gr-markdown,
      html body .gradio-container .gr-code,
      .gr-textbox,
      .gr-dropdown,
      .gr-slider,
      .gr-checkbox,
      .gr-radio,
      .gr-number,
      .gr-file,
      .gr-image,
      .gr-audio,
      .gr-video,
      .gr-dataframe,
      .gr-plot,
      .gr-json,
      .gr-html,
      .gr-markdown,
      .gr-code {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        color: var(--color-base-content) !important;
        border: 1px solid var(--color-base-300) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - SVELTE COMPONENT WRAPPERS (EXCLUDE DROPDOWNS) */
      html body .gradio-container .wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .gradio-container .wrap-inner:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .gradio-container .secondary-wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .gradio-container .reference:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .wrap-inner:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .secondary-wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      html body .reference:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      .wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      .wrap-inner:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      .secondary-wrap:not(.svelte-1hfxrpf):not([class*="dropdown"]),
      .reference:not(.svelte-1hfxrpf):not([class*="dropdown"]) {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        color: var(--color-base-content) !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - INPUT ELEMENTS IN DROPDOWNS */
      html body .gradio-container input[role="listbox"],
      html body .gradio-container input.border-none,
      html body .gradio-container .wrap input,
      html body .gradio-container .wrap-inner input,
      html body .gradio-container .secondary-wrap input,
      html body input[role="listbox"],
      html body input.border-none,
      html body .wrap input,
      html body .wrap-inner input,
      html body .secondary-wrap input,
      input[role="listbox"],
      input.border-none,
      .wrap input,
      .wrap-inner input,
      .secondary-wrap input {
        background: var(--color-base-100) !important;
        background-color: var(--color-base-100) !important;
        color: var(--color-base-content) !important;
        border: 1px solid var(--color-base-300) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
      }
      
      /* ULTRA HIGH SPECIFICITY - ALL SVELTE GENERATED CLASSES */
      html body .gradio-container [class*="svelte-"],
      html body [class*="svelte-"],
      [class*="svelte-"] {
        color: var(--color-base-content) !important;
        font-family: var(--theme-font-family), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }
      
      /* ENSURE ALL GRADIO ELEMENTS GET THEME COLORS AND FONTS */
      html body .gradio-container *,
      html body .gr-form *,
      html body .gradio-interface *,
      .gradio-container *,
      .gr-form *,
      .gradio-interface * {
        color: var(--color-base-content) !important;
        font-family: var(--theme-font-family), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }
      
      /* NUCLEAR OPTION - APPLY FONT TO EVERYTHING */
      * {
        font-family: var(--font-family, var(--font, var(--theme-font-family, "Inter"))), -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif !important;
      }
    `, l = document.createElement("style");
    if (l.id = "gradio-custom-theme", l.textContent = c, document.head.appendChild(l), r.font) {
      const p = r.font.family, b = `"${p}", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"`;
      document.documentElement.style.setProperty("--font-family", b), document.documentElement.style.setProperty("--font", b), document.documentElement.style.setProperty("--theme-font-family", `"${p}"`), n(`Backup: Set comprehensive font CSS variables directly on document root: "${p}"`);
    }
    const d = document.documentElement, x = document.body;
    d.setAttribute("data-theme", f), x.setAttribute("data-theme", f), setTimeout(
      () => {
        n("Applying inline styles with maximum priority"), document.querySelectorAll("body, html, .gradio-container, .app, #root, .gradio-app, .gradio-interface, main").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("background", r.background, "important"), t.style.setProperty("background-color", r.background, "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("font-family", "var(--theme-font-family), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "important"));
        }), document.querySelectorAll(".block").forEach((t) => {
          t && t instanceof HTMLElement && (t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "8px", "important"), t.style.setProperty("padding", "1rem", "important"), t.style.setProperty("margin", "0.5rem 0", "important"), t.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important")));
        }), document.querySelectorAll(".form").forEach((t) => {
          t && t instanceof HTMLElement && (t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "8px", "important"), t.style.setProperty("padding", "1rem", "important"), t.style.setProperty("margin", "0.5rem 0", "important"), t.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important")));
        }), document.querySelectorAll("label, [data-testid*='label'], .label, span, p, div, strong, b, h1, h2, h3, h4, h5, h6").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("font-family", "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "important"));
        }), document.querySelectorAll("code, pre, .code").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("background", "var(--color-base-200)", "important"), t.style.setProperty("background-color", "var(--color-base-200)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "4px", "important"), t.style.setProperty("padding", "0.25rem 0.5rem", "important"));
        }), document.querySelectorAll("svg").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("fill", "currentColor", "important"));
        }), document.querySelectorAll("button, input, textarea, select").forEach((t) => {
          t && t instanceof HTMLElement && t.style.setProperty("font-family", "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "important");
        }), document.querySelectorAll(".gr-textbox, .gr-dropdown, .gr-slider, .gr-checkbox, .gr-radio, .gr-number, .gr-file, .gr-image, .gr-audio, .gr-video, .gr-dataframe, .gr-plot, .gr-json, .gr-html, .gr-markdown, .gr-code").forEach((t) => {
          t && t instanceof HTMLElement && (t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "8px", "important")));
        }), document.querySelectorAll(".wrap, .wrap-inner, .secondary-wrap, .reference").forEach((t) => {
          t && t instanceof HTMLElement && (t.classList.contains("svelte-1hfxrpf") || t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important")));
        }), document.querySelectorAll("input[role='listbox'], input.border-none, .wrap input, .wrap-inner input, .secondary-wrap input").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "8px", "important"), t.style.setProperty("padding", "0.75rem", "important"));
        }), document.querySelectorAll("[class*='svelte-']").forEach((t) => {
          t && t instanceof HTMLElement && (t.classList.contains("svelte-1hfxrpf") || t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || t.style.setProperty("color", "var(--color-base-content)", "important"));
        }), document.querySelectorAll("ul, ol, li").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("list-style", "none", "important"), t.style.setProperty("list-style-type", "none", "important"), t.style.setProperty("list-style-image", "none", "important"), t.style.setProperty("list-style-position", "outside", "important"));
        }), document.querySelectorAll(".codemirror-wrapper, .cm-editor, .cm-content, .cm-focused").forEach((t) => {
          t && t instanceof HTMLElement && (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important"), t.style.setProperty("border-radius", "8px", "important"));
        }), document.querySelectorAll(".icon-button-wrapper, .top-panel, .hide-top-corner, [class*='svelte-9lsba8'], [class*='icon-button']").forEach((t) => {
          t && t instanceof HTMLElement && (t.classList.contains("svelte-1hfxrpf") || t.closest(".svelte-1hfxrpf") || t.querySelector(".svelte-1hfxrpf") || t.querySelector('input[role="listbox"]') || t.closest('[class*="dropdown"]') || (t.style.setProperty("background", "var(--color-base-100)", "important"), t.style.setProperty("background-color", "var(--color-base-100)", "important"), t.style.setProperty("color", "var(--color-base-content)", "important"), t.style.setProperty("border", "1px solid var(--color-base-300)", "important")));
        }), n("Inline styles applied with maximum priority"), setTimeout(
          () => {
            if (r.font) {
              const u = {
                Inter: '"Times New Roman", "Georgia", serif',
                Poppins: '"Arial Black", "Impact", "Helvetica", sans-serif',
                Roboto: '"Courier New", "Monaco", "Consolas", monospace',
                "Open Sans": '"Comic Sans MS", "Trebuchet MS", cursive',
                Lato: '"Palatino", "Book Antiqua", "Times", serif'
              }[r.font.family] || '"Georgia", "Times New Roman", serif', S = `"${r.font.family}", ${u}`;
              n(`Using VISUALLY DISTINCT font stack: ${S}`);
              const e = document.querySelectorAll("*");
              e.forEach((E) => {
                E instanceof HTMLElement && (E.style.setProperty("font-family", S, "important"), E.style.fontWeight || E.style.setProperty("font-weight", "500", "important"));
              });
              const L = document.createElement("style");
              L.id = "extreme-font-override", L.textContent = `
            html * {
              font-family: ${S} !important;
              font-weight: 500 !important;
            }
            
            html body * {
              font-family: ${S} !important;
              font-weight: 500 !important;
            }
            
            html body .gradio-container * {
              font-family: ${S} !important;
              font-weight: 500 !important;
            }
          `;
              const q = document.getElementById("extreme-font-override");
              q && q.remove(), document.head.appendChild(L), n(`Nuclear font application: ${r.font.family} applied to ${e.length} elements`);
            }
          },
          200
        ), new MutationObserver((t) => {
          t.forEach((u) => {
            u.addedNodes.forEach((S) => {
              if (S.nodeType === Node.ELEMENT_NODE) {
                const e = S;
                if (e.classList.contains("svelte-1hfxrpf") || e.closest(".svelte-1hfxrpf") || e.querySelector(".svelte-1hfxrpf") || e.querySelector('input[role="listbox"]') || e.closest('[class*="dropdown"]'))
                  return;
                e.classList.contains("block") && (e.style.setProperty("background", "var(--color-base-100)", "important"), e.style.setProperty("background-color", "var(--color-base-100)", "important"), e.style.setProperty("color", "var(--color-base-content)", "important"), e.style.setProperty("border", "1px solid var(--color-base-300)", "important"), e.style.setProperty("border-radius", "8px", "important"), e.style.setProperty("padding", "1rem", "important"), e.style.setProperty("margin", "0.5rem 0", "important"), e.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important")), e.querySelectorAll(".block").forEach((o) => {
                  o instanceof HTMLElement && (o.closest('[data-testid*="dropdown"]') || o.closest(".gr-dropdown") || o.querySelector('input[role="listbox"]') || o.classList.contains("svelte-1hfxrpf") || o.closest(".svelte-1hfxrpf") || o.querySelector(".svelte-1hfxrpf") || (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "8px", "important"), o.style.setProperty("padding", "1rem", "important"), o.style.setProperty("margin", "0.5rem 0", "important"), o.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important")));
                }), e.classList.contains("form") && (e.closest('[data-testid*="dropdown"]') || e.closest(".gr-dropdown") || e.querySelector('input[role="listbox"]') || e.classList.contains("svelte-1hfxrpf") || e.closest(".svelte-1hfxrpf") || e.querySelector(".svelte-1hfxrpf") || (e.style.setProperty("background", "var(--color-base-100)", "important"), e.style.setProperty("background-color", "var(--color-base-100)", "important"), e.style.setProperty("color", "var(--color-base-content)", "important"), e.style.setProperty("border", "1px solid var(--color-base-300)", "important"), e.style.setProperty("border-radius", "8px", "important"), e.style.setProperty("padding", "1rem", "important"), e.style.setProperty("margin", "0.5rem 0", "important"), e.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important"))), e.querySelectorAll(".form").forEach((o) => {
                  o instanceof HTMLElement && (o.closest('[data-testid*="dropdown"]') || o.closest(".gr-dropdown") || o.querySelector('input[role="listbox"]') || o.classList.contains("svelte-1hfxrpf") || o.closest(".svelte-1hfxrpf") || o.querySelector(".svelte-1hfxrpf") || (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "8px", "important"), o.style.setProperty("padding", "1rem", "important"), o.style.setProperty("margin", "0.5rem 0", "important"), o.style.setProperty("box-shadow", "0 1px 3px rgba(0, 0, 0, 0.1)", "important")));
                }), e.classList.contains("column") && (e.style.setProperty("background", "var(--color-base-100)", "important"), e.style.setProperty("background-color", "var(--color-base-100)", "important"), e.style.setProperty("color", "var(--color-base-content)", "important")), e.querySelectorAll(".column, .gr-column, [data-testid*='column']").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"));
                }), e.querySelectorAll("label, [data-testid*='label'], .label, span, p, div, strong, b, h1, h2, h3, h4, h5, h6").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("font-family", "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "important"));
                }), e.querySelectorAll("code, pre, .code").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("background", "var(--color-base-200)", "important"), o.style.setProperty("background-color", "var(--color-base-200)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "4px", "important"), o.style.setProperty("padding", "0.25rem 0.5rem", "important"));
                }), e.querySelectorAll("svg").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("fill", "currentColor", "important"));
                }), e.querySelectorAll("button, input, textarea, select").forEach((o) => {
                  o instanceof HTMLElement && o.style.setProperty("font-family", "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "important");
                }), e.querySelectorAll(".gr-textbox, .gr-dropdown, .gr-slider, .gr-checkbox, .gr-radio, .gr-number, .gr-file, .gr-image, .gr-audio, .gr-video, .gr-dataframe, .gr-plot, .gr-json, .gr-html, .gr-markdown, .gr-code").forEach((o) => {
                  o instanceof HTMLElement && (o.classList.contains("gr-dropdown") || o.closest(".svelte-1hfxrpf") || o.querySelector(".svelte-1hfxrpf") || o.querySelector('input[role="listbox"]') || (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "8px", "important")));
                }), e.querySelectorAll(".wrap, .wrap-inner, .secondary-wrap, .reference").forEach((o) => {
                  var w, N, D, B, G, O;
                  o instanceof HTMLElement && (o.closest('[data-testid*="dropdown"]') || o.closest(".gr-dropdown") || o.querySelector('input[role="listbox"]') || o.querySelector("select") || (w = o.parentElement) != null && w.classList.contains("gr-dropdown") || (B = (D = (N = o.parentElement) == null ? void 0 : N.dataset) == null ? void 0 : D.testid) != null && B.includes("dropdown") || o.classList.contains("svelte-1hfxrpf") || o.closest(".svelte-1hfxrpf") || (G = o.parentElement) != null && G.querySelector('input[role="listbox"]') || (O = o.closest(".container")) != null && O.querySelector('input[role="listbox"]') || (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important")));
                }), e.querySelectorAll("input[role='listbox'], input.border-none, .wrap input, .wrap-inner input, .secondary-wrap input").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "8px", "important"), o.style.setProperty("padding", "0.75rem", "important"));
                }), e.querySelectorAll(".codemirror-wrapper, .cm-editor, .cm-content, .cm-focused").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important"), o.style.setProperty("border-radius", "8px", "important"));
                }), e.querySelectorAll(".icon-button-wrapper, .top-panel, .hide-top-corner, [class*='svelte-9lsba8'], [class*='icon-button'], .icon-wrap").forEach((o) => {
                  var w;
                  o instanceof HTMLElement && (o.closest(".svelte-1hfxrpf") || o.classList.contains("svelte-1hfxrpf") || o.closest('[data-testid*="dropdown"]') || o.querySelector('input[role="listbox"]') || (w = o.parentElement) != null && w.querySelector('input[role="listbox"]') || (o.style.setProperty("background", "var(--color-base-100)", "important"), o.style.setProperty("background-color", "var(--color-base-100)", "important"), o.style.setProperty("color", "var(--color-base-content)", "important"), o.style.setProperty("border", "1px solid var(--color-base-300)", "important")));
                }), e.querySelectorAll("[class*='svelte-']").forEach((o) => {
                  o instanceof HTMLElement && o.style.setProperty("color", "var(--color-base-content)", "important");
                }), e.querySelectorAll("ul, ol, li").forEach((o) => {
                  o instanceof HTMLElement && (o.style.setProperty("list-style", "none", "important"), o.style.setProperty("list-style-type", "none", "important"), o.style.setProperty("list-style-image", "none", "important"), o.style.setProperty("list-style-position", "outside", "important"));
                });
              }
            });
          });
        }).observe(document.body, { childList: !0, subtree: !0 });
      },
      100
    ), document.querySelectorAll(".gradio-container, .app, #root, .gradio-app, .gradio-interface, main").forEach((p) => {
      p.setAttribute("data-theme", f);
    });
    const k = {
      currentTheme: f,
      type: "builtin",
      themeConfig: r
    };
    y && y.dispatch("change", k), C("change", k), n(`Theme ${r.name} applied successfully with maximum specificity + inline styles`), setTimeout(
      () => {
        var F, H;
        const b = document.querySelectorAll("span, button, label, p, div")[0];
        if (b) {
          const R = window.getComputedStyle(b).fontFamily;
          n(`DEBUG: Computed font on sample element: ${R}`), n(`DEBUG: Expected font: ${((F = r.font) == null ? void 0 : F.family) || "none"}`), n(`DEBUG: CSS variable --theme-font-family: ${getComputedStyle(document.documentElement).getPropertyValue("--theme-font-family")}`), n(`DEBUG: CSS variable --font-family: ${getComputedStyle(document.documentElement).getPropertyValue("--font-family")}`), n(`DEBUG: CSS variable --font: ${getComputedStyle(document.documentElement).getPropertyValue("--font")}`);
          const P = (H = r.font) == null ? void 0 : H.family;
          P && R.includes(P) ? n(`✅ SUCCESS: Font "${P}" is successfully applied and active!`) : P && n(`⚠️ WARNING: Font "${P}" not found in computed style, using fallback`);
        }
      },
      500
    );
  }
  function K(r) {
    n(`Applying basic theme: ${r}`);
    const a = document.documentElement, i = document.body;
    a.setAttribute("data-theme", r), i.setAttribute("data-theme", r), document.querySelectorAll(".gradio-container, .app, #root, .gradio-app, .gradio-interface, main").forEach((d) => {
      d.setAttribute("data-theme", r);
    });
    const l = { currentTheme: r, type: "builtin" };
    y && y.dispatch("change", l), C("change", l);
  }
  function U(r) {
    var c;
    n(`Switching to font: ${r}`);
    const a = ((c = Y.find((l) => l.name === r)) == null ? void 0 : c.family) || "Inter, sans-serif";
    document.documentElement.style.setProperty("--theme-font-family", a), document.body.style.fontFamily = a;
  }
  nt(() => {
    var r;
    if (n("Gradio Themer component mounted"), n("onMount - Initial value object:", s), n("onMount - Available themes:", s == null ? void 0 : s.available_themes), X(), n("Initial theme application", s), (r = s == null ? void 0 : s.font) != null && r.family) {
      n("Applying font", s.font.family);
      const a = s.font.family.split(",")[0].replace(/['"]/g, "").trim();
      U(a);
    } else
      U("Inter");
    s != null && s.currentTheme ? (n("Applying currentTheme", s.currentTheme), M(s.currentTheme)) : s != null && s.themeInput ? (n("Applying themeInput", s.themeInput), Q(s.themeInput)) : n("No specific theme provided, will apply when themes load");
  });
  function X() {
    if (document.getElementById("gradio-css-framework"))
      return;
    const r = [
      "Inter:wght@400,500,600,700",
      "Poppins:wght@300,400,500,600,700",
      "Roboto:wght@300,400,500,700",
      "Open+Sans:wght@300,400,500,600,700",
      "Lato:wght@300,400,500,700",
      "Quicksand:wght@300,400,500,600,700"
    ];
    r.forEach((d, x) => {
      const m = document.createElement("link");
      m.id = `google-font-${x}`, m.rel = "preload", m.as = "style", m.href = `https://fonts.googleapis.com/css2?family=${d}&display=swap`, m.onload = function() {
        this.rel = "stylesheet", n(`Google Font preloaded and activated: ${d}`);
      }, document.head.appendChild(m);
    });
    const a = document.createElement("link");
    a.id = "google-fonts-combined", a.rel = "stylesheet", a.href = `https://fonts.googleapis.com/css2?family=${r.join("&family=")}&display=swap`, document.head.appendChild(a);
    const i = document.createElement("link");
    i.id = "gradio-css-framework", i.rel = "stylesheet", i.href = "https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.css", document.head.appendChild(i);
    const c = document.createElement("link");
    c.id = "tailwind-global-css", c.rel = "stylesheet", c.href = "https://cdn.jsdelivr.net/npm/tailwindcss@3.4.4/base.min.css", document.head.appendChild(c);
    const l = document.createElement("style");
    l.id = "gradio-theme-override", l.textContent = `
      /* COMPREHENSIVE GRADIO THEMING */
      
      /* BLACK BORDER ARTIFACT REMOVAL */
      .gradio-container,
      .app,
      #root,
      .gradio-app,
      .gradio-interface,
      main,
      .gr-form,
      .gr-box,
      .gr-panel,
      .gr-group,
      .gr-column,
      .gr-row,
      .gr-tabs,
      .gr-tab-nav,
      .contain,
      .container,
      [data-testid*="column"],
      [data-testid*="row"],
      [data-testid*="group"],
      [data-testid*="form"],
      [data-testid*="panel"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
      }
      
      /* Remove default Gradio black borders and artifacts */
      * {
        border: none !important;
        box-shadow: none !important;
      }
      
      /* Add back necessary borders only for form elements */
      input, textarea, select,
      .gr-textbox textarea,
      .gr-textbox input,
      .gr-number input,
      .gr-dropdown select,
      [data-testid*="textbox"] textarea,
      [data-testid*="textbox"] input,
      [data-testid*="number"] input,
      [data-testid*="dropdown"] select {
        border: 1px solid hsl(var(--b3)) !important;
      }
      
      /* Force smooth transitions and font on everything */
      * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
        font-family: var(--theme-font-family, Inter), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      }
      
      /* Font styling for headings and text */
      h1, h2, h3, h4, h5, h6 {
        font-family: var(--theme-font-family, Inter), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: hsl(var(--bc)) !important;
        font-weight: 600 !important;
      }
      
      body, html {
        font-family: var(--theme-font-family, Inter), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
      }
      
      /* Main containers - apply base background */
      .gradio-container,
      .app,
      #root,
      .gradio-app,
      .gradio-interface,
      main,
      body,
      html {
        background-color: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
      }
      
      /* All input elements */
      input[type="text"],
      input[type="number"],
      input[type="email"],
      input[type="password"],
      textarea,
      select,
      .gr-textbox textarea,
      .gr-textbox input,
      .gr-number input,
      .gr-dropdown select,
      [data-testid*="textbox"] textarea,
      [data-testid*="textbox"] input,
      [data-testid*="number"] input,
      [data-testid*="dropdown"] select {
        background-color: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
        border: 1px solid hsl(var(--b3)) !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem !important;
      }
      
      /* Input focus states */
      input:focus,
      textarea:focus,
      select:focus {
        border-color: hsl(var(--p)) !important;
        outline: 2px solid hsl(var(--p) / 0.2) !important;
        outline-offset: -1px !important;
      }
      
      /* All buttons */
      button,
      .gr-button,
      [data-testid*="button"],
      input[type="submit"] {
        background-color: hsl(var(--p)) !important;
        color: hsl(var(--pc)) !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
      }
      
      button:hover,
      .gr-button:hover {
        background-color: hsl(var(--pf)) !important;
        transform: translateY(-1px) !important;
      }
      
      /* Secondary button variants */
      button[variant="secondary"],
      .gr-button.secondary {
        background-color: hsl(var(--s)) !important;
        color: hsl(var(--sc)) !important;
      }
      
      /* Stop/danger buttons */
      button[variant="stop"],
      .gr-button.stop {
        background-color: hsl(var(--er)) !important;
        color: hsl(var(--erc)) !important;
      }
      
      /* Disabled buttons */
      button:disabled,
      .gr-button:disabled {
        background-color: hsl(var(--b3)) !important;
        color: hsl(var(--bc) / 0.5) !important;
        cursor: not-allowed !important;
        transform: none !important;
      }
      
      /* Component containers and panels */
      .gr-form,
      .gr-box,
      .gr-panel,
      .gr-group,
      .gr-column,
      .gr-row,
      .gr-tab-nav,
      .gr-tabs,
      [data-testid*="column"],
      [data-testid*="row"],
      [data-testid*="group"] {
        background-color: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
      }
      
      /* Specific targeting for .column class (including without gr- prefix) - MAXIMUM SPECIFICITY */
      html body .gradio-container .column,
      html body .gradio-container div.column,
      html body .gradio-container [class="column"],
      html body .gradio-container [class*=" column"],
      html body .gradio-container [class*="column "],
      .column,
      div.column,
      [class="column"],
      [class*=" column"],
      [class*="column "] {
        background-color: hsl(var(--b1)) !important;
        background: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
      }
      
      /* Cards and elevated surfaces */
      .gr-card,
      .gr-interface,
      [class*="border"],
      [class*="shadow"] {
        background-color: hsl(var(--b2)) !important;
        border-color: hsl(var(--b3)) !important;
      }
      
      /* Tab navigation - comprehensive targeting */
      .gr-tab-nav,
      .gr-tabs,
      [data-testid*="tab"],
      .tablist,
      [role="tablist"] {
        background-color: hsl(var(--b1)) !important;
        border-bottom: 1px solid hsl(var(--b3)) !important;
      }
      
      .gr-tab-nav button,
      .gr-tabs button,
      [data-testid*="tab"] button,
      .tablist button,
      [role="tab"] {
        background-color: hsl(var(--b2)) !important;
        color: hsl(var(--bc)) !important;
        border: 1px solid hsl(var(--b3)) !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0.5rem 0.5rem 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        margin-right: 2px !important;
      }
      
      .gr-tab-nav button:hover,
      .gr-tabs button:hover,
      [data-testid*="tab"] button:hover,
      [role="tab"]:hover {
        background-color: hsl(var(--b3)) !important;
        color: hsl(var(--p)) !important;
      }
      
      .gr-tab-nav button.selected,
      .gr-tab-nav button[aria-selected="true"],
      .gr-tabs button.selected,
      [data-testid*="tab"] button.selected,
      [role="tab"][aria-selected="true"] {
        background-color: hsl(var(--b1)) !important;
        border-bottom-color: hsl(var(--p)) !important;
        border-bottom-width: 3px !important;
        color: hsl(var(--p)) !important;
        font-weight: 600 !important;
      }
      
      /* Tab content areas */
      .gr-tab-item,
      .gr-tabitem,
      [data-testid*="tabitem"],
      [role="tabpanel"] {
        background-color: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
        padding: 1.5rem !important;
        border: 1px solid hsl(var(--b3)) !important;
        border-top: none !important;
        border-radius: 0 0 0.5rem 0.5rem !important;
      }
      
      /* Markdown content */
      .markdown,
      .gr-markdown,
      [data-testid*="markdown"] {
        color: hsl(var(--bc)) !important;
        background-color: transparent !important;
      }
      
      .markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
        color: hsl(var(--bc)) !important;
      }
      
      .markdown code {
        background-color: hsl(var(--b2)) !important;
        color: hsl(var(--bc)) !important;
        padding: 0.125rem 0.25rem !important;
        border-radius: 0.25rem !important;
      }
      
      .markdown pre {
        background-color: hsl(var(--b2)) !important;
        border: 1px solid hsl(var(--b3)) !important;
        border-radius: 0.5rem !important;
      }
      
      /* File upload areas */
      .gr-file,
      [data-testid*="file"] {
        background-color: hsl(var(--b2)) !important;
        border: 2px dashed hsl(var(--b3)) !important;
        border-radius: 0.5rem !important;
        color: hsl(var(--bc)) !important;
      }
      
      /* Dropdowns and selects */
      .gr-dropdown,
      [data-testid*="dropdown"] {
        background-color: hsl(var(--b1)) !important;
      }
      
      /* Prevent ALL elements inside dropdowns from getting background styling */
      .gr-dropdown .wrap,
      .gr-dropdown .wrap-inner,
      .gr-dropdown .secondary-wrap,
      .gr-dropdown .block,
      .gr-dropdown .form,
      .gr-dropdown .container,
      .gr-dropdown .icon-wrap,
      .gr-dropdown .reference,
      [data-testid*="dropdown"] .wrap,
      [data-testid*="dropdown"] .wrap-inner,
      [data-testid*="dropdown"] .secondary-wrap,
      [data-testid*="dropdown"] .block,
      [data-testid*="dropdown"] .form,
      [data-testid*="dropdown"] .container,
      [data-testid*="dropdown"] .icon-wrap,
      [data-testid*="dropdown"] .reference,
      .svelte-1hfxrpf.wrap,
      .svelte-1hfxrpf.wrap-inner,
      .svelte-1hfxrpf.secondary-wrap,
      .svelte-1hfxrpf.block,
      .svelte-1hfxrpf.form,
      .svelte-1hfxrpf.container,
      .svelte-1hfxrpf.icon-wrap,
      .svelte-1hfxrpf.reference,
      .svelte-1hfxrpf .wrap,
      .svelte-1hfxrpf .wrap-inner,
      .svelte-1hfxrpf .secondary-wrap,
      .svelte-1hfxrpf .block,
      .svelte-1hfxrpf .form,
      .svelte-1hfxrpf .container,
      .svelte-1hfxrpf .icon-wrap,
      .svelte-1hfxrpf .reference,
      .wrap.svelte-1hfxrpf,
      .wrap-inner.svelte-1hfxrpf,
      .secondary-wrap.svelte-1hfxrpf,
      .block.svelte-1hfxrpf,
      .form.svelte-1hfxrpf,
      .container.svelte-1hfxrpf,
      .icon-wrap.svelte-1hfxrpf,
      .reference.svelte-1hfxrpf {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
      }
      
      /* Sliders */
      .gr-slider input,
      [data-testid*="slider"] input {
        accent-color: hsl(var(--p)) !important;
      }
      
      /* Checkboxes and radio buttons */
      input[type="checkbox"],
      input[type="radio"] {
        accent-color: hsl(var(--p)) !important;
      }
      
      /* Progress bars */
      progress,
      .progress {
        accent-color: hsl(var(--p)) !important;
        background-color: hsl(var(--b3)) !important;
      }
      
      /* Scrollbars */
      ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
      }
      
      ::-webkit-scrollbar-track {
        background: hsl(var(--b2)) !important;
        border-radius: 4px !important;
      }
      
      ::-webkit-scrollbar-thumb {
        background: hsl(var(--b3)) !important;
        border-radius: 4px !important;
      }
      
      ::-webkit-scrollbar-thumb:hover {
        background: hsl(var(--bc) / 0.3) !important;
      }
      
      /* Labels and helper text */
      label,
      .gr-label,
      [data-testid*="label"] {
        color: hsl(var(--bc)) !important;
        font-weight: 500 !important;
      }
      
      /* Error and success states */
      .error,
      .gr-error {
        color: hsl(var(--er)) !important;
        background-color: hsl(var(--er) / 0.1) !important;
      }
      
      .success,
      .gr-success {
        color: hsl(var(--su)) !important;
        background-color: hsl(var(--su) / 0.1) !important;
      }
      
      /* Force inheritance for nested elements */
      .gradio-container * {
        color: inherit !important;
      }
      
      /* NUCLEAR OPTION: Force column backgrounds with maximum CSS specificity */
      html[data-theme] body .gradio-container .column,
      html body .gradio-container div[class*="column"],
      html body .gradio-container *[class*="column"],
      html body .gradio-container *[class="column"] {
        background-color: hsl(var(--b1)) !important;
        background: hsl(var(--b1)) !important;
        color: hsl(var(--bc)) !important;
      }
    `, document.head.appendChild(l), n("Global CSS framework injected successfully");
  }
  function Q(r) {
    n("Applying theme CSS directly", r);
    const a = document.getElementById("gradio-custom-theme");
    a && a.remove();
    const i = document.createElement("style");
    i.id = "gradio-custom-theme";
    const c = J(r);
    i.textContent = c, document.head.appendChild(i);
    const l = r.match(/name:\s*"([^"]+)"/), d = l ? l[1] : "custom";
    g(4, f = d);
    const x = document.documentElement, m = document.body;
    x.setAttribute("data-theme", d), m.setAttribute("data-theme", d), document.querySelectorAll(".gradio-container, .app, #root, .gradio-app, .gradio-interface, main").forEach((b) => {
      b.setAttribute("data-theme", d);
    });
    const p = {
      currentTheme: d,
      type: "theme-css",
      css: c,
      original: r
    };
    y && y.dispatch("change", p), C("change", p);
  }
  function J(r) {
    n("Converting theme CSS", r);
    const a = "corporate", i = {
      "color-base-100": "b1",
      "color-base-200": "b2",
      "color-base-300": "b3",
      "color-base-content": "bc",
      "color-primary": "p",
      "color-primary-content": "pc",
      "color-secondary": "s",
      "color-secondary-content": "sc",
      "color-accent": "a",
      "color-accent-content": "ac",
      "color-neutral": "n",
      "color-neutral-content": "nc",
      "color-info": "in",
      "color-info-content": "inc",
      "color-success": "su",
      "color-success-content": "suc",
      "color-warning": "wa",
      "color-warning-content": "wac",
      "color-error": "er",
      "color-error-content": "erc"
    }, c = /--([^:]+):\s*([^;]+);?/g;
    let l, d = "";
    for (; (l = c.exec(r)) !== null; ) {
      const m = l[1].trim(), k = l[2].trim();
      n(`Found CSS variable: --${m}: ${k}`);
      const p = i[m] || m.replace("color-", "");
      i[m] && (d += `  --${p}: ${k};
`), d += `  --${m}: ${k};
`;
    }
    const x = `[data-theme="${a}"], :root[data-theme="${a}"] {
${d}}

/* Force theme application */
* {
  color-scheme: light;
}`;
    return n("Generated CSS", x), x;
  }
  return T.$$set = (r) => {
    "value" in r && g(2, s = r.value), "gradio" in r && g(3, y = r.gradio);
  }, T.$$.update = () => {
    if (T.$$.dirty[0] & /*value, themeColors, availableThemes, initialThemeApplied, currentTheme*/
    244 && s)
      if (n("Value received from backend", s), n("Available themes in value:", s == null ? void 0 : s.available_themes), s != null && s.available_themes) {
        g(5, h = s.available_themes), g(6, v = Object.keys(h)), n("Loaded user themes", {
          count: v.length,
          themes: v,
          themeColors: h
        });
        const r = s == null ? void 0 : s.currentTheme;
        if (!I || r && v.includes(r)) {
          if (r && v.includes(r))
            n("Applying theme from backend", r), M(r), g(7, I = !0);
          else if (!I && v.length > 0 && (!f || f === "light")) {
            const i = v[0];
            n("Applying default theme from loaded themes", i), M(i), g(7, I = !0);
          }
        } else
          n("Theme unchanged, not overriding user selection");
      } else
        n("No available_themes in value object", {
          value: s,
          available_themes: s == null ? void 0 : s.available_themes,
          keys: Object.keys(s || {})
        });
  }, [
    $,
    _,
    s,
    y,
    f,
    h,
    v,
    I
  ];
}
class Et extends tt {
  constructor(A) {
    super(), ot(
      this,
      A,
      at,
      null,
      rt,
      {
        elem_id: 0,
        elem_classes: 1,
        value: 2,
        gradio: 3
      },
      null,
      [-1, -1]
    );
  }
  get elem_id() {
    return this.$$.ctx[0];
  }
  get elem_classes() {
    return this.$$.ctx[1];
  }
}
export {
  Et as default
};
