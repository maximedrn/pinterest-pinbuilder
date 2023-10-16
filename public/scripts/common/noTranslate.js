// web/js/common/noTranslate.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { ICON } from "../utils/constants/elements.js";
import { NO_TRANSLATE } from "../utils/constants/attributes.js";


/**
 * Marks specified elements with a "no-translate" class to prevent
 * translation. This function finds elements with the specified class and
 * adds the "no-translate" class to them, indicating that they should not
 * be translated when using translation services.
 */
export function noTranslate() {
    const icons = [...document.querySelectorAll(ICON)];
    icons.forEach(icon => icon.classList.add(NO_TRANSLATE));
}
