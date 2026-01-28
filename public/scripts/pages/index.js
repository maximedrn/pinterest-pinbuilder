import { noTranslate } from "../common/noTranslate.js";
import { editHeader } from "../utils/headerManager.js";
import { loadPreviousIframe } from "../utils/iframeManager.js";
import { schemeModeButton, schemeModeManager } from "../utils/schemeManager.js";


window.addEventListener("DOMContentLoaded", async () => {
    noTranslate();  // Icon translation.
    loadPreviousIframe(); // Iframe manager.
    // responsiveHeaderHeight(); // Header manager.
    editHeader();
    schemeModeManager(); // Scheme manager.
    schemeModeButton();
});