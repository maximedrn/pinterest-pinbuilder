// web/js/pages/create.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { setSchemeMode } from "../utils/schemeManager.js";
import { CreateManager } from "../utils/createManager.js";
import { noTranslate } from "../common/noTranslate.js";
import { SCHEME_MODES } from "../utils/constants/values.js";
import { initializeFlatpickr } from "../utils/flatpickrManager.js";


window.addEventListener("DOMContentLoaded", async () => {
    window.addEventListener("message", event => { // Scheme mode manager.
        if (SCHEME_MODES.includes(event.data)) setSchemeMode(event.data);
    }, false);

    noTranslate(); // Icon translation.
    initializeFlatpickr(); // Flatpickr package.
    // Create manager.
    const createManager = new CreateManager;
    createManager.assetsFolderSelection();
});
