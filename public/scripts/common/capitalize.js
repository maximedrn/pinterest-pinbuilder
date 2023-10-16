// web/js/common/capitalize.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


/**
 * Capitalizes the first character of the string.
 *
 * @returns {string} A new string with the first character capitalized.
 */
String.prototype.capitalize = function () {
    return this.replace(/^./, this[0].toUpperCase());
};
