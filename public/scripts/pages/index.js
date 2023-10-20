// web/js/pages/index.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { editHeader } from "../utils/headerManager.js";
import { loadPreviousIframe } from "../utils/iframeManager.js";
import { checkLicenseKey } from "../utils/licenseKeyManager.js";
import { schemeModeButton, schemeModeManager } from "../utils/schemeManager.js";
import { noTranslate } from "../common/noTranslate.js";
import { displayInformation } from "../utils/informationManager.js";


window.addEventListener("DOMContentLoaded", async () => {
    noTranslate();  // Icon translation.
    loadPreviousIframe(); // Iframe manager.
    // responsiveHeaderHeight(); // Header manager.
    editHeader();
    schemeModeManager(); // Scheme manager.
    schemeModeButton();
    checkLicenseKey(); // License key manager.
    displayInformation();
});