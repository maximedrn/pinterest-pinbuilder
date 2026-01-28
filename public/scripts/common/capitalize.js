// web/js/common/capitalize.js

/**
 * Capitalizes the first character of the string.
 *
 * @returns {string} A new string with the first character capitalized.
 */
String.prototype.capitalize = function () {
    return this.replace(/^./, this[0].toUpperCase());
};
