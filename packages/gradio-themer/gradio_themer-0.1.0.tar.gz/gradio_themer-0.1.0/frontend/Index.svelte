<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import "./styles.css";

  // Gradio-specific props (const to avoid unused export warnings)
  export const elem_id = "";
  export const elem_classes: string[] = [];
  export let value: any = null;
  export let gradio: any = undefined;

  const dispatch = createEventDispatcher();

  // Phase 2: Dynamic themes - themes are now loaded dynamically from backend
  // Themes are now loaded dynamically from backend via value.available_themes

  // Font options for the font selector
  const fontOptions = [
    { name: "Inter", family: "Inter, sans-serif" },
    {
      name: "System",
      family:
        "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    },
    { name: "Roboto", family: "Roboto, sans-serif" },
    { name: "Open Sans", family: "'Open Sans', sans-serif" },
    { name: "Lato", family: "Lato, sans-serif" },
    { name: "Poppins", family: "Poppins, sans-serif" },
    { name: "Montserrat", family: "Montserrat, sans-serif" },
    { name: "Source Sans Pro", family: "'Source Sans Pro', sans-serif" },
    { name: "Ubuntu", family: "Ubuntu, sans-serif" },
    { name: "Nunito", family: "Nunito, sans-serif" },
  ];

  // Color definitions for theme building
  const colorOptions = {
    base: [
      "#ffffff",
      "#f7f7f7",
      "#e5e7eb",
      "#d1d5db",
      "#9ca3af",
      "#374151",
      "#1f2937",
      "#111827",
    ],
    primary: [
      "#3b82f6",
      "#06b6d4",
      "#10b981",
      "#f59e0b",
      "#ef4444",
      "#8b5cf6",
      "#ec4899",
      "#6366f1",
    ],
    secondary: [
      "#64748b",
      "#475569",
      "#334155",
      "#1e293b",
      "#0f172a",
      "#7c3aed",
      "#c026d3",
      "#db2777",
    ],
    accent: [
      "#f97316",
      "#eab308",
      "#84cc16",
      "#22c55e",
      "#06b6d4",
      "#3b82f6",
      "#8b5cf6",
      "#ec4899",
    ],
    neutral: [
      "#374151",
      "#4b5563",
      "#6b7280",
      "#9ca3af",
      "#d1d5db",
      "#f3f4f6",
      "#f9fafb",
      "#ffffff",
    ],
    info: [
      "#0ea5e9",
      "#0284c7",
      "#0369a1",
      "#075985",
      "#0c4a6e",
      "#082f49",
      "#164e63",
      "#155e75",
    ],
    success: [
      "#22c55e",
      "#16a34a",
      "#15803d",
      "#166534",
      "#14532d",
      "#052e16",
      "#064e3b",
      "#065f46",
    ],
    warning: [
      "#f59e0b",
      "#d97706",
      "#b45309",
      "#92400e",
      "#78350f",
      "#451a03",
      "#365314",
      "#1a2e05",
    ],
    error: [
      "#ef4444",
      "#dc2626",
      "#b91c1c",
      "#991b1b",
      "#7f1d1d",
      "#450a0a",
      "#7c2d12",
      "#a16207",
    ],
  };

  // State
  let currentTheme = "light";
  let selectedFont = "Inter";
  let customTheme = {
    name: "custom",
    base: "#ffffff",
    primary: "#3b82f6",
    secondary: "#64748b",
    accent: "#f97316",
    neutral: "#374151",
    info: "#0ea5e9",
    success: "#22c55e",
    warning: "#f59e0b",
    error: "#ef4444",
  };

  let generatedCSS = "";
  let copySuccess = false;
  let activeTab = "themes"; // "themes", "description", or "installation"
  let customThemeCSS = ""; // For custom CSS input

  // Phase 2: Dynamic theme loading from backend
  let themeColors = {}; // Will be populated from backend
  let availableThemes: string[] = []; // Available theme keys for UI
  let initialThemeApplied = false; // Track if we've applied the initial theme
  let lastAppliedTheme = ""; // Track the last theme we applied to detect backend changes

  // Logging
  function log(message: string, data?: any) {
    console.log(`[Gradio Themer] ${message}`, data || "");
    if (gradio) {
      gradio.dispatch("log", { message, data });
    }
  }

  // Phase 2: Dynamic theme loading - themes will be loaded from backend
  // Remove hardcoded themeColors - now loaded from value.available_themes

  // Reactive statement to load themes from backend
  $: if (value) {
    log("Value received from backend", value);
    log("Available themes in value:", value?.available_themes);

    if (value?.available_themes) {
      themeColors = value.available_themes;
      availableThemes = Object.keys(themeColors);
      log("Loaded user themes", {
        count: availableThemes.length,
        themes: availableThemes,
        themeColors: themeColors,
      });

      // Apply theme if it's the initial load OR if backend sends a valid theme
      const backendTheme = value?.currentTheme;

      // Always apply theme if backend sends a valid theme (for random button responsiveness)
      // Only skip if it's the exact same theme AND we've already applied initial theme
      const shouldApplyTheme =
        !initialThemeApplied ||
        (backendTheme && availableThemes.includes(backendTheme));

      if (shouldApplyTheme) {
        if (backendTheme && availableThemes.includes(backendTheme)) {
          log("Applying theme from backend", backendTheme);

          selectTheme(backendTheme);

          lastAppliedTheme = backendTheme;

          initialThemeApplied = true;
        } else if (
          !initialThemeApplied &&
          availableThemes.length > 0 &&
          (!currentTheme || currentTheme === "light")
        ) {
          // Apply first available theme as default if no specific theme set
          const defaultTheme = availableThemes[0];
          log("Applying default theme from loaded themes", defaultTheme);
          selectTheme(defaultTheme);
          lastAppliedTheme = defaultTheme;
          initialThemeApplied = true;
        }
      } else {
        log("Theme unchanged, not overriding user selection");
      }
    } else {
      log("No available_themes in value object", {
        value,
        available_themes: value?.available_themes,
        keys: Object.keys(value || {}),
      });
    }
  }

  function getActualFontInUse(): string {
    // Create a test element to check what font is actually being used
    const testElement = document.createElement("div");
    testElement.style.cssText = `
      position: absolute;
      visibility: hidden;
      font-size: 16px;
      font-family: inherit;
    `;
    document.body.appendChild(testElement);

    const computedStyle = window.getComputedStyle(testElement);
    const actualFont = computedStyle.fontFamily;

    document.body.removeChild(testElement);

    // Extract the first font name from the font stack
    const firstFont = actualFont.split(",")[0].replace(/['"]/g, "").trim();
    return firstFont;
  }

  // addFontIndicator function removed to prevent popup on refresh

  function loadGradioFont(fontConfig: any) {
    log(
      `Loading Stable Font: ${fontConfig.name || fontConfig.family}`,
      fontConfig
    );

    // Use simple font name to avoid triggering Gradio's font loader
    const fontName = fontConfig.family; // Use the direct font name
    const displayName = fontConfig.name || fontName;

    log(`Using stable font: ${fontName}`);
    applySystemFont(fontName, displayName);
  }

  function applySystemFont(fontStack: string, fontName: string) {
    log(`Applying stable system font: ${fontName}`);

    // STEP 1: Block all Gradio font loading attempts
    blockGradioFontLoading();

    // STEP 2: Create comprehensive font CSS with maximum stability
    const fontCSS = `
      /* COMPLETE FONT OVERRIDE - NO GRADIO FONT LOADING */
      
      /* Override all possible font CSS variables */
      :root, html, body, .gradio-container {
        --font: ${fontName}, sans-serif !important;
        --font-family: ${fontName}, sans-serif !important;
        --theme-font-family: ${fontName}, sans-serif !important;
        --font-sans: ${fontName}, sans-serif !important;
        --font-mono: monospace !important;
        --body-font-family: ${fontName}, sans-serif !important;
        --text-font-family: ${fontName}, sans-serif !important;
      }
      
      /* Block any @font-face rules */
      @media all {
        @font-face {
          font-family: 'ui-sans-serif';
          src: local('${fontName}');
        }
        @font-face {
          font-family: 'system-ui';
          src: local('${fontName}');
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
        font-family: ${fontName}, sans-serif !important;
        font-size: inherit !important;
      }
    `;

    // Remove existing font CSS
    const existing = document.getElementById("gradio-font-stable");
    if (existing) existing.remove();

    // Apply stable font CSS
    const style = document.createElement("style");
    style.id = "gradio-font-stable";
    style.textContent = fontCSS;
    document.head.appendChild(style);

    // Visual confirmation removed to prevent popup on refresh
    log(
      `✅ Stable system font ${fontName} applied (no font loading conflicts)`
    );
  }

  function blockGradioFontLoading() {
    // Remove any existing font links
    const fontLinks = document.querySelectorAll('link[href*="/static/fonts/"]');
    fontLinks.forEach((link) => link.remove());

    // Block future font loading by intercepting appendChild
    if (!(window as any).gradioFontBlocked) {
      const originalAppendChild = document.head.appendChild;
      document.head.appendChild = function (child) {
        if (
          child instanceof HTMLLinkElement &&
          child.href &&
          child.href.includes("/static/fonts/")
        ) {
          log(`🚫 BLOCKED Gradio font loading: ${child.href}`);
          return child; // Don't actually append
        }
        return originalAppendChild.call(this, child);
      };
      (window as any).gradioFontBlocked = true;
      log(`🚫 Gradio font loading blocked`);
    }
  }

  // Keep the old function name for compatibility but redirect to new system
  function loadGoogleFont(fontConfig: any) {
    log(`Redirecting Google Font to Gradio system: ${fontConfig.family}`);
    loadGradioFont(fontConfig);

    // No additional setup needed - system fonts are always available
  }

  function selectTheme(theme: string) {
    log(`Switching to theme: ${theme}`);
    currentTheme = theme;
    lastAppliedTheme = theme; // Track the theme we're applying

    // Check if we have user themes loaded and this theme exists
    if (themeColors && themeColors[theme]) {
      log(`Applying user theme: ${theme}`, themeColors[theme]);
      applyThemeColors(themeColors[theme]);
      return;
    }

    // Fallback to basic theme application for unknown themes
    log(`Applying basic theme: ${theme} (no custom configuration found)`);
    applyBasicTheme(theme);
  }

  function applyGradioNativeTheme(themeConfig: any) {
    log(`Applying Gradio native theme with font: ${themeConfig.font?.family}`);

    // For Gradio native themes, we should let Gradio handle the theming
    // and only apply minimal overrides for colors that match our JSON themes
    if (themeConfig.gradio_theme) {
      // Apply the Gradio theme to the app
      // This would require integration with Gradio's theme system
      log(`Gradio theme object available:`, themeConfig.gradio_theme);

      // Apply color overrides to match our JSON theme colors
      const themeKey = themeConfig.currentTheme;
      if (themeColors && themeColors[themeKey]) {
        const colorConfig = themeColors[themeKey];
        log(`Applying color overrides for: ${colorConfig.name}`);
        applyColorOverrides(colorConfig);
      }
    }
  }

  function applyColorOverrides(themeConfig: any) {
    log(`Applying color overrides for: ${themeConfig.name}`);

    // Apply only color overrides, let Gradio handle fonts
    const colorCSS = `
      :root {
        ${Object.entries(themeConfig.colors)
          .map(([key, value]) => `--color-${key}: ${value};`)
          .join("\n        ")}
      }
      
      /* Apply background override */
      body, .gradio-container, main {
        background: ${themeConfig.background} !important;
        background-color: ${themeConfig.background} !important;
      }
    `;

    // Remove existing color overrides
    const existing = document.getElementById("gradio-color-overrides");
    if (existing) {
      existing.remove();
    }

    // Inject color overrides
    const style = document.createElement("style");
    style.id = "gradio-color-overrides";
    style.textContent = colorCSS;
    document.head.appendChild(style);

    log(`Color overrides applied for ${themeConfig.name}`);
  }

  function applyThemeColors(themeConfig: any) {
    log(`Applying theme colors for: ${themeConfig.name}`);

    // Remove existing custom theme
    const existing = document.getElementById("gradio-custom-theme");
    if (existing) {
      existing.remove();
    }

    // Load fonts based on configuration
    if (themeConfig.font) {
      // Always use the simple system font approach
      loadGradioFont(themeConfig.font);
    }

    // Build CSS variables from theme colors
    let cssVars = ":root {\n";
    for (const [key, value] of Object.entries(themeConfig.colors)) {
      cssVars += `  --color-${key}: ${value};\n`;
    }

    // Add font family variable using Gradio's standard CSS variables
    if (themeConfig.font) {
      const fontFamily = themeConfig.font.family;
      // Create comprehensive font stack with better fallbacks
      const fontStack = `"${fontFamily}", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"`;

      // Use Gradio's standard font CSS variables
      cssVars += `  --font-family: ${fontStack};\n`;
      cssVars += `  --font: ${fontStack};\n`;
      cssVars += `  --theme-font-family: "${fontFamily}";\n`;
      log(
        `Setting font CSS variables to: "${fontFamily}" with comprehensive fallbacks`
      );
    } else {
      log(`No font configuration found in theme config`);
    }

    cssVars += "}\n";

    // Create comprehensive CSS with theme-specific background
    const themeCSS =
      cssVars +
      `
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
        background: ${themeConfig.background} !important;
        background-color: ${themeConfig.background} !important;
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
    `;

    // Inject the CSS with maximum priority
    const style = document.createElement("style");
    style.id = "gradio-custom-theme";
    style.textContent = themeCSS;
    document.head.appendChild(style);

    // Also set the CSS variables directly on the document root as backup
    if (themeConfig.font) {
      const fontFamily = themeConfig.font.family;
      const fontStack = `"${fontFamily}", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"`;
      document.documentElement.style.setProperty("--font-family", fontStack);
      document.documentElement.style.setProperty("--font", fontStack);
      document.documentElement.style.setProperty(
        "--theme-font-family",
        `"${fontFamily}"`
      );
      log(
        `Backup: Set comprehensive font CSS variables directly on document root: "${fontFamily}"`
      );
    }

    // Apply theme attributes globally
    const root = document.documentElement;
    const body = document.body;
    root.setAttribute("data-theme", currentTheme);
    body.setAttribute("data-theme", currentTheme);

    // FORCE INLINE STYLES - Maximum priority approach
    setTimeout(() => {
      log("Applying inline styles with maximum priority");

      // Force background on everything
      const allContainers = document.querySelectorAll(
        "body, html, .gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
      );
      allContainers.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "background",
            themeConfig.background,
            "important"
          );
          el.style.setProperty(
            "background-color",
            themeConfig.background,
            "important"
          );
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty(
            "font-family",
            "var(--theme-font-family), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "important"
          );
        }
      });

      // Force styling on block elements (exclude dropdowns)
      const blockElements = document.querySelectorAll(".block");
      blockElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this block is part of dropdown
          const isDropdownBlock =
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownBlock) {
            el.style.setProperty(
              "background",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "background-color",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
            el.style.setProperty(
              "border",
              "1px solid var(--color-base-300)",
              "important"
            );
            el.style.setProperty("border-radius", "8px", "important");
            el.style.setProperty("padding", "1rem", "important");
            el.style.setProperty("margin", "0.5rem 0", "important");
            el.style.setProperty(
              "box-shadow",
              "0 1px 3px rgba(0, 0, 0, 0.1)",
              "important"
            );
          }
        }
      });

      // Force styling on form elements (exclude dropdowns)
      const formElements = document.querySelectorAll(".form");
      formElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this form is part of dropdown
          const isDropdownForm =
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownForm) {
            el.style.setProperty(
              "background",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "background-color",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
            el.style.setProperty(
              "border",
              "1px solid var(--color-base-300)",
              "important"
            );
            el.style.setProperty("border-radius", "8px", "important");
            el.style.setProperty("padding", "1rem", "important");
            el.style.setProperty("margin", "0.5rem 0", "important");
            el.style.setProperty(
              "box-shadow",
              "0 1px 3px rgba(0, 0, 0, 0.1)",
              "important"
            );
          }
        }
      });

      // Force styling on labels and text elements
      const labelElements = document.querySelectorAll(
        "label, [data-testid*='label'], .label, span, p, div, strong, b, h1, h2, h3, h4, h5, h6"
      );
      labelElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty(
            "font-family",
            "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "important"
          );
        }
      });

      // Force styling on code elements
      const codeElements = document.querySelectorAll("code, pre, .code");
      codeElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "background",
            "var(--color-base-200)",
            "important"
          );
          el.style.setProperty(
            "background-color",
            "var(--color-base-200)",
            "important"
          );
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty(
            "border",
            "1px solid var(--color-base-300)",
            "important"
          );
          el.style.setProperty("border-radius", "4px", "important");
          el.style.setProperty("padding", "0.25rem 0.5rem", "important");
        }
      });

      // Force styling on SVG icons
      const svgElements = document.querySelectorAll("svg");
      svgElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty("fill", "currentColor", "important");
        }
      });

      // Force font styling on buttons and inputs
      const buttonInputElements = document.querySelectorAll(
        "button, input, textarea, select"
      );
      buttonInputElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "font-family",
            "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "important"
          );
        }
      });

      // Force styling on Gradio specific elements (exclude dropdowns)
      const gradioElements = document.querySelectorAll(
        ".gr-textbox, .gr-dropdown, .gr-slider, .gr-checkbox, .gr-radio, .gr-number, .gr-file, .gr-image, .gr-audio, .gr-video, .gr-dataframe, .gr-plot, .gr-json, .gr-html, .gr-markdown, .gr-code"
      );
      gradioElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this Gradio element is part of dropdown
          const isDropdownGradio =
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownGradio) {
            el.style.setProperty(
              "background",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "background-color",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
            el.style.setProperty(
              "border",
              "1px solid var(--color-base-300)",
              "important"
            );
            el.style.setProperty("border-radius", "8px", "important");
          }
        }
      });

      // Force styling on Svelte component wrappers (exclude dropdowns)
      const wrapperElements = document.querySelectorAll(
        ".wrap, .wrap-inner, .secondary-wrap, .reference"
      );
      wrapperElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this wrapper is part of dropdown
          const isDropdownWrapper =
            el.classList.contains("svelte-1hfxrpf") ||
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownWrapper) {
            el.style.setProperty(
              "background",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "background-color",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
          }
        }
      });

      // Force styling on dropdown inputs
      const dropdownInputs = document.querySelectorAll(
        "input[role='listbox'], input.border-none, .wrap input, .wrap-inner input, .secondary-wrap input"
      );
      dropdownInputs.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "background",
            "var(--color-base-100)",
            "important"
          );
          el.style.setProperty(
            "background-color",
            "var(--color-base-100)",
            "important"
          );
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty(
            "border",
            "1px solid var(--color-base-300)",
            "important"
          );
          el.style.setProperty("border-radius", "8px", "important");
          el.style.setProperty("padding", "0.75rem", "important");
        }
      });

      // Force styling on all Svelte generated elements (exclude dropdowns)
      const svelteElements = document.querySelectorAll("[class*='svelte-']");
      svelteElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this Svelte element is part of dropdown
          const isDropdownSvelte =
            el.classList.contains("svelte-1hfxrpf") ||
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownSvelte) {
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
          }
        }
      });

      // Remove list markers
      const listElements = document.querySelectorAll("ul, ol, li");
      listElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty("list-style", "none", "important");
          el.style.setProperty("list-style-type", "none", "important");
          el.style.setProperty("list-style-image", "none", "important");
          el.style.setProperty("list-style-position", "outside", "important");
        }
      });

      // Force styling on CodeMirror wrappers
      const codemirrorElements = document.querySelectorAll(
        ".codemirror-wrapper, .cm-editor, .cm-content, .cm-focused"
      );
      codemirrorElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          el.style.setProperty(
            "background",
            "var(--color-base-100)",
            "important"
          );
          el.style.setProperty(
            "background-color",
            "var(--color-base-100)",
            "important"
          );
          el.style.setProperty(
            "color",
            "var(--color-base-content)",
            "important"
          );
          el.style.setProperty(
            "border",
            "1px solid var(--color-base-300)",
            "important"
          );
          el.style.setProperty("border-radius", "8px", "important");
        }
      });

      // Force styling on icon button wrappers (exclude dropdowns)
      const iconButtonElements = document.querySelectorAll(
        ".icon-button-wrapper, .top-panel, .hide-top-corner, [class*='svelte-9lsba8'], [class*='icon-button']"
      );
      iconButtonElements.forEach((el) => {
        if (el && el instanceof HTMLElement) {
          // Skip if this icon button is part of dropdown
          const isDropdownIcon =
            el.classList.contains("svelte-1hfxrpf") ||
            el.closest(".svelte-1hfxrpf") ||
            el.querySelector(".svelte-1hfxrpf") ||
            el.querySelector('input[role="listbox"]') ||
            el.closest('[class*="dropdown"]');

          if (!isDropdownIcon) {
            el.style.setProperty(
              "background",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "background-color",
              "var(--color-base-100)",
              "important"
            );
            el.style.setProperty(
              "color",
              "var(--color-base-content)",
              "important"
            );
            el.style.setProperty(
              "border",
              "1px solid var(--color-base-300)",
              "important"
            );
          }
        }
      });

      // REMOVED: Force styling on models dropdown section
      // This was causing nested dropdown styling by explicitly targeting .svelte-1hfxrpf elements
      // Dropdown styling is now handled only through CSS and non-dropdown-specific sections

      log("Inline styles applied with maximum priority");

      // NUCLEAR FONT APPLICATION - Apply font to absolutely everything
      setTimeout(() => {
        if (themeConfig.font) {
          // Create VISUALLY DISTINCT font stacks for each theme
          const fontMappings = {
            Inter: '"Times New Roman", "Georgia", serif',
            Poppins: '"Arial Black", "Impact", "Helvetica", sans-serif',
            Roboto: '"Courier New", "Monaco", "Consolas", monospace',
            "Open Sans": '"Comic Sans MS", "Trebuchet MS", cursive',
            Lato: '"Palatino", "Book Antiqua", "Times", serif',
          };

          // Use visually distinct fallback if Google Font fails
          const distinctFont =
            fontMappings[themeConfig.font.family] ||
            '"Georgia", "Times New Roman", serif';
          const fontStack = `"${themeConfig.font.family}", ${distinctFont}`;

          log(`Using VISUALLY DISTINCT font stack: ${fontStack}`);

          // Apply to every single element on the page with EXTREME priority
          const allElements = document.querySelectorAll("*");
          allElements.forEach((el) => {
            if (el instanceof HTMLElement) {
              el.style.setProperty("font-family", fontStack, "important");
              // Also set font-weight and size for more visual distinction
              if (!el.style.fontWeight) {
                el.style.setProperty("font-weight", "500", "important");
              }
            }
          });

          // EXTREME MEASURE: Override Gradio's CSS with ultra-high specificity
          const extremeCSS = document.createElement("style");
          extremeCSS.id = "extreme-font-override";
          extremeCSS.textContent = `
            html * {
              font-family: ${fontStack} !important;
              font-weight: 500 !important;
            }
            
            html body * {
              font-family: ${fontStack} !important;
              font-weight: 500 !important;
            }
            
            html body .gradio-container * {
              font-family: ${fontStack} !important;
              font-weight: 500 !important;
            }
          `;

          // Remove existing extreme override
          const existing = document.getElementById("extreme-font-override");
          if (existing) existing.remove();

          document.head.appendChild(extremeCSS);

          log(
            `Nuclear font application: ${themeConfig.font.family} applied to ${allElements.length} elements`
          );

          // Visual font indicator removed to prevent popup on refresh
        }
      }, 200);

      // Set up MutationObserver to handle dynamically added elements
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
              const element = node as HTMLElement;

              // Skip dropdown elements completely
              if (
                element.classList.contains("svelte-1hfxrpf") ||
                element.closest(".svelte-1hfxrpf") ||
                element.querySelector(".svelte-1hfxrpf") ||
                element.querySelector('input[role="listbox"]') ||
                element.closest('[class*="dropdown"]')
              ) {
                return;
              }

              // Apply theme to newly added block elements
              if (element.classList.contains("block")) {
                element.style.setProperty(
                  "background",
                  "var(--color-base-100)",
                  "important"
                );
                element.style.setProperty(
                  "background-color",
                  "var(--color-base-100)",
                  "important"
                );
                element.style.setProperty(
                  "color",
                  "var(--color-base-content)",
                  "important"
                );
                element.style.setProperty(
                  "border",
                  "1px solid var(--color-base-300)",
                  "important"
                );
                element.style.setProperty("border-radius", "8px", "important");
                element.style.setProperty("padding", "1rem", "important");
                element.style.setProperty("margin", "0.5rem 0", "important");
                element.style.setProperty(
                  "box-shadow",
                  "0 1px 3px rgba(0, 0, 0, 0.1)",
                  "important"
                );
              }

              // Find any nested block elements
              const nestedBlocks = element.querySelectorAll(".block");
              nestedBlocks.forEach((blockEl) => {
                if (blockEl instanceof HTMLElement) {
                  // Skip block elements that are part of dropdown components
                  const isDropdownBlock =
                    blockEl.closest('[data-testid*="dropdown"]') ||
                    blockEl.closest(".gr-dropdown") ||
                    blockEl.querySelector('input[role="listbox"]') ||
                    blockEl.classList.contains("svelte-1hfxrpf") ||
                    blockEl.closest(".svelte-1hfxrpf") ||
                    blockEl.querySelector(".svelte-1hfxrpf");

                  if (!isDropdownBlock) {
                    blockEl.style.setProperty(
                      "background",
                      "var(--color-base-100)",
                      "important"
                    );
                    blockEl.style.setProperty(
                      "background-color",
                      "var(--color-base-100)",
                      "important"
                    );
                    blockEl.style.setProperty(
                      "color",
                      "var(--color-base-content)",
                      "important"
                    );
                    blockEl.style.setProperty(
                      "border",
                      "1px solid var(--color-base-300)",
                      "important"
                    );
                    blockEl.style.setProperty(
                      "border-radius",
                      "8px",
                      "important"
                    );
                    blockEl.style.setProperty("padding", "1rem", "important");
                    blockEl.style.setProperty(
                      "margin",
                      "0.5rem 0",
                      "important"
                    );
                    blockEl.style.setProperty(
                      "box-shadow",
                      "0 1px 3px rgba(0, 0, 0, 0.1)",
                      "important"
                    );
                  }
                }
              });

              // Apply theme to newly added form elements
              if (element.classList.contains("form")) {
                // Skip form elements that are part of dropdown components
                const isDropdownForm =
                  element.closest('[data-testid*="dropdown"]') ||
                  element.closest(".gr-dropdown") ||
                  element.querySelector('input[role="listbox"]') ||
                  element.classList.contains("svelte-1hfxrpf") ||
                  element.closest(".svelte-1hfxrpf") ||
                  element.querySelector(".svelte-1hfxrpf");

                if (!isDropdownForm) {
                  element.style.setProperty(
                    "background",
                    "var(--color-base-100)",
                    "important"
                  );
                  element.style.setProperty(
                    "background-color",
                    "var(--color-base-100)",
                    "important"
                  );
                  element.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  element.style.setProperty(
                    "border",
                    "1px solid var(--color-base-300)",
                    "important"
                  );
                  element.style.setProperty(
                    "border-radius",
                    "8px",
                    "important"
                  );
                  element.style.setProperty("padding", "1rem", "important");
                  element.style.setProperty("margin", "0.5rem 0", "important");
                  element.style.setProperty(
                    "box-shadow",
                    "0 1px 3px rgba(0, 0, 0, 0.1)",
                    "important"
                  );
                }
              }

              // Apply theme to nested form elements
              const nestedForms = element.querySelectorAll(".form");
              nestedForms.forEach((formEl) => {
                if (formEl instanceof HTMLElement) {
                  // Skip form elements that are part of dropdown components
                  const isDropdownForm =
                    formEl.closest('[data-testid*="dropdown"]') ||
                    formEl.closest(".gr-dropdown") ||
                    formEl.querySelector('input[role="listbox"]') ||
                    formEl.classList.contains("svelte-1hfxrpf") ||
                    formEl.closest(".svelte-1hfxrpf") ||
                    formEl.querySelector(".svelte-1hfxrpf");

                  if (!isDropdownForm) {
                    formEl.style.setProperty(
                      "background",
                      "var(--color-base-100)",
                      "important"
                    );
                    formEl.style.setProperty(
                      "background-color",
                      "var(--color-base-100)",
                      "important"
                    );
                    formEl.style.setProperty(
                      "color",
                      "var(--color-base-content)",
                      "important"
                    );
                    formEl.style.setProperty(
                      "border",
                      "1px solid var(--color-base-300)",
                      "important"
                    );
                    formEl.style.setProperty(
                      "border-radius",
                      "8px",
                      "important"
                    );
                    formEl.style.setProperty("padding", "1rem", "important");
                    formEl.style.setProperty("margin", "0.5rem 0", "important");
                    formEl.style.setProperty(
                      "box-shadow",
                      "0 1px 3px rgba(0, 0, 0, 0.1)",
                      "important"
                    );
                  }
                }
              });

              // Apply theme to column elements (including .column without gr- prefix)
              if (element.classList.contains("column")) {
                element.style.setProperty(
                  "background",
                  "var(--color-base-100)",
                  "important"
                );
                element.style.setProperty(
                  "background-color",
                  "var(--color-base-100)",
                  "important"
                );
                element.style.setProperty(
                  "color",
                  "var(--color-base-content)",
                  "important"
                );
              }

              // Apply theme to nested column elements
              const nestedColumns = element.querySelectorAll(
                ".column, .gr-column, [data-testid*='column']"
              );
              nestedColumns.forEach((columnEl) => {
                if (columnEl instanceof HTMLElement) {
                  columnEl.style.setProperty(
                    "background",
                    "var(--color-base-100)",
                    "important"
                  );
                  columnEl.style.setProperty(
                    "background-color",
                    "var(--color-base-100)",
                    "important"
                  );
                  columnEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                }
              });

              // Apply theme to nested labels and text elements
              const nestedLabels = element.querySelectorAll(
                "label, [data-testid*='label'], .label, span, p, div, strong, b, h1, h2, h3, h4, h5, h6"
              );
              nestedLabels.forEach((labelEl) => {
                if (labelEl instanceof HTMLElement) {
                  labelEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  labelEl.style.setProperty(
                    "font-family",
                    "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                    "important"
                  );
                }
              });

              // Apply theme to nested code elements
              const nestedCode = element.querySelectorAll("code, pre, .code");
              nestedCode.forEach((codeEl) => {
                if (codeEl instanceof HTMLElement) {
                  codeEl.style.setProperty(
                    "background",
                    "var(--color-base-200)",
                    "important"
                  );
                  codeEl.style.setProperty(
                    "background-color",
                    "var(--color-base-200)",
                    "important"
                  );
                  codeEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  codeEl.style.setProperty(
                    "border",
                    "1px solid var(--color-base-300)",
                    "important"
                  );
                  codeEl.style.setProperty("border-radius", "4px", "important");
                  codeEl.style.setProperty(
                    "padding",
                    "0.25rem 0.5rem",
                    "important"
                  );
                }
              });

              // Apply theme to nested SVG icons
              const nestedSvgs = element.querySelectorAll("svg");
              nestedSvgs.forEach((svgEl) => {
                if (svgEl instanceof HTMLElement) {
                  svgEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  svgEl.style.setProperty("fill", "currentColor", "important");
                }
              });

              // Apply fonts to nested buttons and inputs
              const nestedInputs = element.querySelectorAll(
                "button, input, textarea, select"
              );
              nestedInputs.forEach((inputEl) => {
                if (inputEl instanceof HTMLElement) {
                  inputEl.style.setProperty(
                    "font-family",
                    "var(--theme-font-family, 'Inter'), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                    "important"
                  );
                }
              });

              // Apply theme to nested Gradio elements
              const nestedGradio = element.querySelectorAll(
                ".gr-textbox, .gr-dropdown, .gr-slider, .gr-checkbox, .gr-radio, .gr-number, .gr-file, .gr-image, .gr-audio, .gr-video, .gr-dataframe, .gr-plot, .gr-json, .gr-html, .gr-markdown, .gr-code"
              );
              nestedGradio.forEach((gradioEl) => {
                if (gradioEl instanceof HTMLElement) {
                  // Skip dropdown elements to prevent nested styling
                  const isDropdownElement =
                    gradioEl.classList.contains("gr-dropdown") ||
                    gradioEl.closest(".svelte-1hfxrpf") ||
                    gradioEl.querySelector(".svelte-1hfxrpf") ||
                    gradioEl.querySelector('input[role="listbox"]');

                  if (!isDropdownElement) {
                    gradioEl.style.setProperty(
                      "background",
                      "var(--color-base-100)",
                      "important"
                    );
                    gradioEl.style.setProperty(
                      "background-color",
                      "var(--color-base-100)",
                      "important"
                    );
                    gradioEl.style.setProperty(
                      "color",
                      "var(--color-base-content)",
                      "important"
                    );
                    gradioEl.style.setProperty(
                      "border",
                      "1px solid var(--color-base-300)",
                      "important"
                    );
                    gradioEl.style.setProperty(
                      "border-radius",
                      "8px",
                      "important"
                    );
                  }
                }
              });

              // Apply theme to nested wrapper elements (but skip dropdown wrapper elements)
              const nestedWrappers = element.querySelectorAll(
                ".wrap, .wrap-inner, .secondary-wrap, .reference"
              );
              nestedWrappers.forEach((wrapperEl) => {
                if (wrapperEl instanceof HTMLElement) {
                  // Skip wrapper elements that are part of dropdown components
                  const isDropdownWrapper =
                    wrapperEl.closest('[data-testid*="dropdown"]') ||
                    wrapperEl.closest(".gr-dropdown") ||
                    wrapperEl.querySelector('input[role="listbox"]') ||
                    wrapperEl.querySelector("select") ||
                    wrapperEl.parentElement?.classList.contains(
                      "gr-dropdown"
                    ) ||
                    wrapperEl.parentElement?.dataset?.testid?.includes(
                      "dropdown"
                    ) ||
                    wrapperEl.classList.contains("svelte-1hfxrpf") ||
                    wrapperEl.closest(".svelte-1hfxrpf") ||
                    wrapperEl.parentElement?.querySelector(
                      'input[role="listbox"]'
                    ) ||
                    wrapperEl
                      .closest(".container")
                      ?.querySelector('input[role="listbox"]');

                  if (!isDropdownWrapper) {
                    wrapperEl.style.setProperty(
                      "background",
                      "var(--color-base-100)",
                      "important"
                    );
                    wrapperEl.style.setProperty(
                      "background-color",
                      "var(--color-base-100)",
                      "important"
                    );
                    wrapperEl.style.setProperty(
                      "color",
                      "var(--color-base-content)",
                      "important"
                    );
                  }
                }
              });

              // Apply theme to nested dropdown inputs
              const nestedDropdownInputs = element.querySelectorAll(
                "input[role='listbox'], input.border-none, .wrap input, .wrap-inner input, .secondary-wrap input"
              );
              nestedDropdownInputs.forEach((inputEl) => {
                if (inputEl instanceof HTMLElement) {
                  inputEl.style.setProperty(
                    "background",
                    "var(--color-base-100)",
                    "important"
                  );
                  inputEl.style.setProperty(
                    "background-color",
                    "var(--color-base-100)",
                    "important"
                  );
                  inputEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  inputEl.style.setProperty(
                    "border",
                    "1px solid var(--color-base-300)",
                    "important"
                  );
                  inputEl.style.setProperty(
                    "border-radius",
                    "8px",
                    "important"
                  );
                  inputEl.style.setProperty("padding", "0.75rem", "important");
                }
              });

              // Apply theme to nested CodeMirror elements
              const nestedCodeMirror = element.querySelectorAll(
                ".codemirror-wrapper, .cm-editor, .cm-content, .cm-focused"
              );
              nestedCodeMirror.forEach((cmEl) => {
                if (cmEl instanceof HTMLElement) {
                  cmEl.style.setProperty(
                    "background",
                    "var(--color-base-100)",
                    "important"
                  );
                  cmEl.style.setProperty(
                    "background-color",
                    "var(--color-base-100)",
                    "important"
                  );
                  cmEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                  cmEl.style.setProperty(
                    "border",
                    "1px solid var(--color-base-300)",
                    "important"
                  );
                  cmEl.style.setProperty("border-radius", "8px", "important");
                }
              });

              // Apply theme to nested icon button elements (but skip dropdown icon elements)
              const nestedIconButtons = element.querySelectorAll(
                ".icon-button-wrapper, .top-panel, .hide-top-corner, [class*='svelte-9lsba8'], [class*='icon-button'], .icon-wrap"
              );
              nestedIconButtons.forEach((iconEl) => {
                if (iconEl instanceof HTMLElement) {
                  // Skip icon elements that are part of dropdown components
                  const isDropdownIcon =
                    iconEl.closest(".svelte-1hfxrpf") ||
                    iconEl.classList.contains("svelte-1hfxrpf") ||
                    iconEl.closest('[data-testid*="dropdown"]') ||
                    iconEl.querySelector('input[role="listbox"]') ||
                    iconEl.parentElement?.querySelector(
                      'input[role="listbox"]'
                    );

                  if (!isDropdownIcon) {
                    iconEl.style.setProperty(
                      "background",
                      "var(--color-base-100)",
                      "important"
                    );
                    iconEl.style.setProperty(
                      "background-color",
                      "var(--color-base-100)",
                      "important"
                    );
                    iconEl.style.setProperty(
                      "color",
                      "var(--color-base-content)",
                      "important"
                    );
                    iconEl.style.setProperty(
                      "border",
                      "1px solid var(--color-base-300)",
                      "important"
                    );
                  }
                }
              });

              // Apply theme to nested Svelte elements
              const nestedSvelte =
                element.querySelectorAll("[class*='svelte-']");
              nestedSvelte.forEach((svelteEl) => {
                if (svelteEl instanceof HTMLElement) {
                  svelteEl.style.setProperty(
                    "color",
                    "var(--color-base-content)",
                    "important"
                  );
                }
              });

              // Remove list styling from newly added lists
              const nestedLists = element.querySelectorAll("ul, ol, li");
              nestedLists.forEach((listEl) => {
                if (listEl instanceof HTMLElement) {
                  listEl.style.setProperty("list-style", "none", "important");
                  listEl.style.setProperty(
                    "list-style-type",
                    "none",
                    "important"
                  );
                  listEl.style.setProperty(
                    "list-style-image",
                    "none",
                    "important"
                  );
                  listEl.style.setProperty(
                    "list-style-position",
                    "outside",
                    "important"
                  );
                }
              });
            }
          });
        });
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      });
    }, 100);

    // Apply to Gradio containers
    const gradioContainers = document.querySelectorAll(
      ".gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
    );
    gradioContainers.forEach((container) => {
      container.setAttribute("data-theme", currentTheme);
    });

    // Dispatch change event
    const themeData = { currentTheme, type: "builtin", themeConfig };
    if (gradio) {
      gradio.dispatch("change", themeData);
    }
    dispatch("change", themeData);

    log(
      `Theme ${themeConfig.name} applied successfully with maximum specificity + inline styles`
    );

    // Debug: Check what fonts are actually being applied
    setTimeout(() => {
      const testElements = document.querySelectorAll(
        "span, button, label, p, div"
      );
      const sampleElement = testElements[0];
      if (sampleElement) {
        const computedStyle = window.getComputedStyle(sampleElement);
        const actualFont = computedStyle.fontFamily;
        log(`DEBUG: Computed font on sample element: ${actualFont}`);
        log(`DEBUG: Expected font: ${themeConfig.font?.family || "none"}`);
        log(
          `DEBUG: CSS variable --theme-font-family: ${getComputedStyle(document.documentElement).getPropertyValue("--theme-font-family")}`
        );
        log(
          `DEBUG: CSS variable --font-family: ${getComputedStyle(document.documentElement).getPropertyValue("--font-family")}`
        );
        log(
          `DEBUG: CSS variable --font: ${getComputedStyle(document.documentElement).getPropertyValue("--font")}`
        );

        // Check if the expected font is actually in the computed font family
        const expectedFont = themeConfig.font?.family;
        if (expectedFont && actualFont.includes(expectedFont)) {
          log(
            `✅ SUCCESS: Font "${expectedFont}" is successfully applied and active!`
          );
        } else if (expectedFont) {
          log(
            `⚠️ WARNING: Font "${expectedFont}" not found in computed style, using fallback`
          );
        }
      }
    }, 500);
  }

  function applyBasicTheme(theme: string) {
    log(`Applying basic theme: ${theme}`);

    // Apply theme to document root and body for global effect
    const root = document.documentElement;
    const body = document.body;
    root.setAttribute("data-theme", theme);
    body.setAttribute("data-theme", theme);

    // Also apply to any Gradio containers and main elements
    const gradioContainers = document.querySelectorAll(
      ".gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
    );
    gradioContainers.forEach((container) => {
      container.setAttribute("data-theme", theme);
    });

    // Dispatch change event
    const themeData = { currentTheme: theme, type: "builtin" };
    if (gradio) {
      gradio.dispatch("change", themeData);
    }
    dispatch("change", themeData);
  }

  function selectFont(font: string) {
    log(`Switching to font: ${font}`);
    selectedFont = font;
    const fontFamily =
      fontOptions.find((f) => f.name === font)?.family || "Inter, sans-serif";

    // Apply font to document via CSS variable
    const root = document.documentElement;
    root.style.setProperty("--theme-font-family", fontFamily);

    // Also set font-family directly on body for immediate effect
    document.body.style.fontFamily = fontFamily;
  }

  function generateCustomCSS() {
    log("Generating custom CSS", customTheme);

    const css = `[data-theme="custom"] {
  --color-base-100: ${customTheme.base};
  --color-base-200: color-mix(in srgb, ${customTheme.base} 90%, black);
  --color-base-300: color-mix(in srgb, ${customTheme.base} 80%, black);
  --color-base-content: color-mix(in srgb, ${customTheme.base} 20%, black);
  --color-primary: ${customTheme.primary};
  --color-primary-content: #ffffff;
  --color-secondary: ${customTheme.secondary};
  --color-secondary-content: #ffffff;
  --color-accent: ${customTheme.accent};
  --color-accent-content: #ffffff;
  --color-neutral: ${customTheme.neutral};
  --color-neutral-content: #ffffff;
  --color-info: ${customTheme.info};
  --color-info-content: #ffffff;
  --color-success: ${customTheme.success};
  --color-success-content: #ffffff;
  --color-warning: ${customTheme.warning};
  --color-warning-content: #000000;
  --color-error: ${customTheme.error};
  --color-error-content: #ffffff;
}`;

    generatedCSS = css;
    applyCustomTheme(css);
  }

  function applyCustomTheme(css: string) {
    log("Applying custom theme CSS");

    // Remove existing custom theme
    const existing = document.getElementById("gradio-custom-theme");
    if (existing) {
      existing.remove();
    }

    // Add new custom theme
    const style = document.createElement("style");
    style.id = "gradio-custom-theme";
    style.textContent = css;
    document.head.appendChild(style);

    // Switch to custom theme globally
    currentTheme = "custom";
    const root = document.documentElement;
    const body = document.body;
    root.setAttribute("data-theme", "custom");
    body.setAttribute("data-theme", "custom");

    // Also apply to any Gradio containers and main elements
    const gradioContainers = document.querySelectorAll(
      ".gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
    );
    gradioContainers.forEach((container) => {
      container.setAttribute("data-theme", "custom");
    });

    // Dispatch change event
    const themeData = {
      currentTheme: "custom",
      type: "custom",
      css: generatedCSS,
      colors: customTheme,
    };
    if (gradio) {
      gradio.dispatch("change", themeData);
    }
    dispatch("change", themeData);
  }

  function copyToClipboard() {
    if (navigator.clipboard && generatedCSS) {
      navigator.clipboard.writeText(generatedCSS).then(() => {
        copySuccess = true;
        log("CSS copied to clipboard");
        setTimeout(() => (copySuccess = false), 2000);
      });
    }
  }

  function updateCustomColor(colorType: string, color: string) {
    log(`Updating ${colorType} to ${color}`);
    customTheme[colorType] = color;
    generateCustomCSS();
  }

  function applyCustomThemeCSS() {
    if (!customThemeCSS.trim()) return;

    log("Applying custom theme CSS from input");

    // Remove existing custom theme
    const existing = document.getElementById("gradio-custom-theme");
    if (existing) {
      existing.remove();
    }

    // Add new custom theme
    const style = document.createElement("style");
    style.id = "gradio-custom-theme";
    style.textContent = customThemeCSS;
    document.head.appendChild(style);

    // Try to extract theme name from CSS or use 'custom'
    const themeNameMatch = customThemeCSS.match(/data-theme="([^"]+)"/);
    const themeName = themeNameMatch ? themeNameMatch[1] : "custom";

    // Switch to the custom theme globally
    currentTheme = themeName;
    const root = document.documentElement;
    const body = document.body;
    root.setAttribute("data-theme", themeName);
    body.setAttribute("data-theme", themeName);

    // Also apply to any Gradio containers and main elements
    const gradioContainers = document.querySelectorAll(
      ".gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
    );
    gradioContainers.forEach((container) => {
      container.setAttribute("data-theme", themeName);
    });

    // Dispatch change event
    const themeData = {
      currentTheme: themeName,
      type: "custom",
      css: customThemeCSS,
    };
    if (gradio) {
      gradio.dispatch("change", themeData);
    }
    dispatch("change", themeData);
  }

  // Initialize component and inject global CSS
  onMount(() => {
    log("Gradio Themer component mounted");
    log("onMount - Initial value object:", value);
    log("onMount - Available themes:", value?.available_themes);

    // Inject CSS framework globally into document head
    injectGlobalCSS();

    // Apply initial theme
    log("Initial theme application", value);

    // Apply font settings if provided
    if (value?.font?.family) {
      log("Applying font", value.font.family);
      const fontName = value.font.family
        .split(",")[0]
        .replace(/['"]/g, "")
        .trim();
      selectFont(fontName);
    } else {
      // Set default font to Inter
      selectFont("Inter");
    }

    // Apply initial theme - now with dynamic theme support
    if (value?.currentTheme) {
      log("Applying currentTheme", value.currentTheme);
      selectTheme(value.currentTheme);
    } else if (value?.themeInput) {
      log("Applying themeInput", value.themeInput);
      // Apply custom theme CSS directly
      applyThemeCSS(value.themeInput);
    } else {
      log("No specific theme provided, will apply when themes load");
      // Don't apply any theme yet - wait for dynamic themes to load
      // The reactive statement will handle initial theme application
    }
  });

  function injectGlobalCSS() {
    // Check if CSS framework is already injected
    if (document.getElementById("gradio-css-framework")) {
      return;
    }

    // PRELOAD GOOGLE FONTS FIRST - This is critical for proper font loading
    const googleFonts = [
      "Inter:wght@400,500,600,700",
      "Poppins:wght@300,400,500,600,700",
      "Roboto:wght@300,400,500,700",
      "Open+Sans:wght@300,400,500,600,700",
      "Lato:wght@300,400,500,700",
      "Quicksand:wght@300,400,500,600,700",
    ];

    googleFonts.forEach((font, index) => {
      const fontLink = document.createElement("link");
      fontLink.id = `google-font-${index}`;
      fontLink.rel = "preload";
      fontLink.as = "style";
      fontLink.href = `https://fonts.googleapis.com/css2?family=${font}&display=swap`;
      fontLink.onload = function () {
        (this as HTMLLinkElement).rel = "stylesheet";
        log(`Google Font preloaded and activated: ${font}`);
      };
      document.head.appendChild(fontLink);
    });

    // Add a combined Google Fonts link as backup
    const combinedFonts = document.createElement("link");
    combinedFonts.id = "google-fonts-combined";
    combinedFonts.rel = "stylesheet";
    combinedFonts.href = `https://fonts.googleapis.com/css2?family=${googleFonts.join("&family=")}&display=swap`;
    document.head.appendChild(combinedFonts);

    // Inject CSS framework globally
    const frameworkCSS = document.createElement("link");
    frameworkCSS.id = "gradio-css-framework";
    frameworkCSS.rel = "stylesheet";
    frameworkCSS.href =
      "https://cdn.jsdelivr.net/npm/daisyui@4.12.10/dist/full.css";
    document.head.appendChild(frameworkCSS);

    // Inject Tailwind base CSS
    const tailwindCSS = document.createElement("link");
    tailwindCSS.id = "tailwind-global-css";
    tailwindCSS.rel = "stylesheet";
    tailwindCSS.href =
      "https://cdn.jsdelivr.net/npm/tailwindcss@3.4.4/base.min.css";
    document.head.appendChild(tailwindCSS);

    // Inject aggressive override CSS for Gradio
    const overrideCSS = document.createElement("style");
    overrideCSS.id = "gradio-theme-override";
    overrideCSS.textContent = `
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
    `;
    document.head.appendChild(overrideCSS);

    log("Global CSS framework injected successfully");
  }

  function applyThemeCSS(cssInput: string) {
    log("Applying theme CSS directly", cssInput);

    // Remove existing custom theme
    const existing = document.getElementById("gradio-custom-theme");
    if (existing) {
      existing.remove();
    }

    // Parse and apply the theme CSS
    const style = document.createElement("style");
    style.id = "gradio-custom-theme";

    // Convert theme format to CSS variables
    const cssContent = convertThemeToCSSVars(cssInput);
    style.textContent = cssContent;
    document.head.appendChild(style);

    // Extract theme name or use 'custom'
    const themeNameMatch = cssInput.match(/name:\s*"([^"]+)"/);
    const themeName = themeNameMatch ? themeNameMatch[1] : "custom";

    // Apply theme globally
    currentTheme = themeName;
    const root = document.documentElement;
    const body = document.body;
    root.setAttribute("data-theme", themeName);
    body.setAttribute("data-theme", themeName);

    // Apply to Gradio containers
    const gradioContainers = document.querySelectorAll(
      ".gradio-container, .app, #root, .gradio-app, .gradio-interface, main"
    );
    gradioContainers.forEach((container) => {
      container.setAttribute("data-theme", themeName);
    });

    // Dispatch change event
    const themeData = {
      currentTheme: themeName,
      type: "theme-css",
      css: cssContent,
      original: cssInput,
    };
    if (gradio) {
      gradio.dispatch("change", themeData);
    }
    dispatch("change", themeData);
  }

  function convertThemeToCSSVars(themeCSS: string) {
    log("Converting theme CSS", themeCSS);

    // Extract theme name from input or use 'custom'
    const themeName = "corporate"; // Default name

    // Map color names to standard CSS variable names
    const colorMap = {
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
      "color-error-content": "erc",
    };

    // Extract all CSS variables from the input
    const cssVarRegex = /--([^:]+):\s*([^;]+);?/g;
    let match;
    let cssVars = "";

    while ((match = cssVarRegex.exec(themeCSS)) !== null) {
      const varName = match[1].trim();
      const varValue = match[2].trim();

      log(`Found CSS variable: --${varName}: ${varValue}`);

      // Map to short names if it's a color
      const shortName = colorMap[varName] || varName.replace("color-", "");

      // Add the short name version for framework compatibility
      if (colorMap[varName]) {
        cssVars += `  --${shortName}: ${varValue};\n`;
      }

      // Always add the original variable
      cssVars += `  --${varName}: ${varValue};\n`;
    }

    const finalCSS = `[data-theme="${themeName}"], :root[data-theme="${themeName}"] {\n${cssVars}}\n\n/* Force theme application */\n* {\n  color-scheme: light;\n}`;

    log("Generated CSS", finalCSS);
    return finalCSS;
  }

  // Phase 2: Theme loading function completed
</script>
