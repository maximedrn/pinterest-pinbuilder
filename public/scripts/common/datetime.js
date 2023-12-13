// web/js/common/datetime.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


/**
 * Formats a date as "DD/MM/YYYY" with an optional number of added days.
 *
 * @param {Date} datetime - The date to format.
 * @param {number} addedDays - (Optional) The number of days to add to
 * the date. Defaults to 0.
 * @returns {string} The formatted date string in the "DD/MM/YYYY" format.
 */
export function datetimeFormat(datetime, addedDays = 0) {
    datetime = new Date(datetime.setDate(datetime.getDate() + addedDays));
    // Get day, month, and year components.
    const day = String(datetime.getDate()).padStart(2, "0");
    const month = String(datetime.getMonth() + 1).padStart(2, "0");
    const year = datetime.getFullYear();
    // Format the date as "DD/MM/YYYY".
    return day + "/" + month + "/" + year;
}

/**
 * Converts a Unix timestamp to a formatted date string in "DD/MM/YYYY" format.
 *
 * @param {number} timestamp - The Unix timestamp to convert.
 * @returns {string} The formatted date string in the "DD/MM/YYYY" format.
 */
export function timeStampToDatetime(timestamp) {
    const date = new Date(timestamp * 1000);
    return datetimeFormat(date);
}

