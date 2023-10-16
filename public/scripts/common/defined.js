// web/js/common/defined.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { EMPTY_VALUES } from "../utils/constants/values.js";


/**
 * Checks if a variable is defined and not equal to any of the
 * specified empty values.
 *
 * @param {any} variable - The variable to check for definition 
 * and emptiness.
 * @returns {boolean} `true` if the variable is defined and not 
 * equal to any empty value, `false` otherwise.
 */
export function defined(variable) {
    for (let emptyValue of EMPTY_VALUES) {
        if (variable == String(emptyValue)) return false;
    };
    return true;
}
