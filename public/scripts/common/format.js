// web/js/common/format.js

/**
 * Replaces placeholders in the string with values provided as arguments.
 *
 * This method replaces occurrences of "{}" in the string with values provided
 * as arguments in the same order. If there are more placeholders than
 * arguments, the extra placeholders will remain unchanged. If there are more
 * arguments than placeholders, the extra arguments will be ignored.
 *
 * @returns {string} A new string with placeholders replaced by the provided
 * values.
 */
String.prototype.format = function () {
    var i = 0;
    var args = arguments;

    return this.replace(/{}/g, function () {
        return typeof args[i] != "undefined" ? args[i++] : "";
    });
};
