import { datetimeFormat } from "../common/datetime.js";
import {
    DATA_FILES_KEYS,
    FLATPICKR_FORMAT,
    MAXIMUM_SCHEDULE_DAYS
} from "./constants/values.js";


/**
 * Initializes the Flatpickr date and time picker with specific
 * configuration options.
 * 
 * This function initializes the Flatpickr library on a specified
 * element, enabling date and time picking with custom formatting
 * and input options.
 */
export function initializeFlatpickr() {
    const today = new Date();
    const datetimeElement = DATA_FILES_KEYS.datetime;

    flatpickr(datetimeElement, {
        enableTime: true,
        time_24hr: true,
        dateFormat: FLATPICKR_FORMAT,
        allowInput: true,
        enable: [{
            from: datetimeFormat(today),
            to: datetimeFormat(today, MAXIMUM_SCHEDULE_DAYS)
        }]
    });
}
