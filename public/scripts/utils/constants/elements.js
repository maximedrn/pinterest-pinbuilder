export const ICON = "i";
export const IMAGE = "img";
export const FAVICON_ELEMENT = "#favicon";

// Snackbar container and text.
export const CONTAINER_SNACKBAR = ".snackbar__container";
export const ELEMENT_SNACKBAR_UUID = ".snackbar__element[data-uuid=\"{}\"]";
export const ELEMENT_SNACKBAR_TEXT = " p";
export const ELEMENT_SNACKBAR_ICON = " i";


/**
 * Index page elements.
 */

// Iframe.
export const ELEMENT_IFRAME = "iframe";
export const ELEMENT_IFRAME_SOURCE = ELEMENT_IFRAME + "[src*=\"{}\"]";

// Header and navigation.
export const ELEMENT_HEADER = "header";
export const ELEMENT_NAVIGATION_BUTTON = "header>nav>section";
export const ELEMENT_SCHEME_MODE_BUTTON = ".scheme-mode__button";

/**
 * Process page elements.
 */

// Data files list and browser.
export const CONTAINER_DATA_FILES = ".container__list";
const ELEMENT_BROWSED_DATA_FILE = CONTAINER_DATA_FILES + " .container__browsed-file";
export const ELEMENT_BROWSED_DATA_FILE_BUTTON = ELEMENT_BROWSED_DATA_FILE + " .container__list-text";
export const CONTAINER_BROWSED_DATA_FILE_TEXT = ELEMENT_BROWSED_DATA_FILE + " .container__list-selected";
export const ELEMENT_BROWSED_DATA_FILE_CLEAR = CONTAINER_BROWSED_DATA_FILE_TEXT + " i";
export const ELEMENT_BROWSED_DATA_FILE_TEXT = CONTAINER_BROWSED_DATA_FILE_TEXT + " p";
export const ELEMENT_DATA_FILE_RELOAD = CONTAINER_DATA_FILES + " .container__list-reload";
export const ELEMENT_DATA_FILE = CONTAINER_DATA_FILES + ">section[type=\"checkbox\"]";

// Accounts.
export const CONTAINER_ACCOUNTS = ".container__account";
const ELEMENT_ACCOUNT_BOX = CONTAINER_ACCOUNTS + ">.container__account-element";
export const ELEMENT_ACCOUNT = ELEMENT_ACCOUNT_BOX + "[type=\"checkbox\"]";
export const ELEMENT_ADD_ACCOUNT_BUTTON = ELEMENT_ACCOUNT_BOX + "[type=\"button\"]";

// Fields.
export const ELEMENT_BROWSED_FILE = ELEMENT_BROWSED_DATA_FILE_TEXT;
export const CONTAINER_SELECTED_FILE = ".container__list-element.checked";
export const ELEMENT_SELECTED_FILE = CONTAINER_SELECTED_FILE + " p";
export const ELEMENT_SELECTED_ACCOUNT = ELEMENT_ACCOUNT + ".checked>.container__account-text>span";
export const ELEMENT_STARTING_VALUE = "input[name=\"starting-value\"]";
export const ELEMENT_MAXIMUM_ATTEMPTS = "input[name=\"maximum-attempts\"]";
export const ELEMENT_DELETE_TEMP_FILE = "#delete-temp-folder";

// Start buttons and text.
export const ELEMENT_UPLOAD_BUTTON = "footer>section[name=\"upload-button\"]";
export const ELEMENT_UPLOAD_BUTTON_TEXT = ELEMENT_UPLOAD_BUTTON + " span";
export const ELEMENT_LOGIN_BUTTON = "footer>section[name=\"login-button\"]";
export const ELEMENT_LOGIN_BUTTON_TEXT = ELEMENT_LOGIN_BUTTON + " span";

// Console.
export const CONSOLE_OUTPUT_CONTAINER = ".container__process-output";
export const CONSOLE_OUTPUT_TITLE = CONSOLE_OUTPUT_CONTAINER + " .container__preview-text";
export const CONSOLE_OUTPUT_PARAGRAPH = CONSOLE_OUTPUT_CONTAINER + " .container__outputs";


/**
 * Create page elements.
 */

// Assets container.
export const CONTAINER_ASSETS = ".container__assets>article";
const ELEMENT_BROWSED_FOLDER = CONTAINER_ASSETS + " .container__browsed-folder";
export const ELEMENT_BROWSED_ASSETS_FOLDER_BUTTON = ELEMENT_BROWSED_FOLDER + " .container__list-text";
export const CONTAINER_BROWSED_ASSETS_FOLDER_TEXT = ELEMENT_BROWSED_FOLDER + " .container__list-selected";
export const ELEMENT_ASSETS_FOLDER_CLEAR = CONTAINER_BROWSED_ASSETS_FOLDER_TEXT + " i";
export const ELEMENT_BROWSED_ASSETS_FOLDER_TEXT = CONTAINER_BROWSED_ASSETS_FOLDER_TEXT + " p";
export const CONTAINER_ASSETS_LIST = CONTAINER_ASSETS + " .container__list-assets";
export const ELEMENT_ASSETS_PREVIEW = ".container__assets-element";
export const ELEMENT_LOADING_ASSETS = CONTAINER_ASSETS + " .container__preview-text";
export const ELEMENT_LOADING_ASSETS_TEXT = ELEMENT_LOADING_ASSETS + ">p";

// Navigation buttons.
export const CONTAINER_ASSETS_ACTION_BUTTONS = ".container__assets-buttons";
export const ELEMENT_PREVIOUS_CHUNK_BUTTON = "section[name=\"previous-chunk\"]";
export const ELEMENT_NEXT_CHUNK_BUTTON = "section[name=\"next-chunk\"]";
export const ELEMENT_PREVIOUS_ASSET_BUTTON = "section[name=\"previous-asset\"]";
export const ELEMENT_NEXT_ASSET_BUTTON = "section[name=\"next-asset\"]";

// Pin type.
export const ELEMENT_PIN_TYPE_TOGGLE = "input[name=\"promotable-pin\"]";
export const ELEMENT_PAID_PIN = ".pin__paid";
export const ELEMENT_ORGANIC_PIN = ".pin__organic";

// Fields and action buttons.
export const ELEMENT_APPLY_FOR_ALL_BUTTON = "section[name=\"apply-for-all\"]";
export const ELEMENT_REMOVE_FOR_ALL_BUTTON = "section[name=\"remove-for-all\"]";
export const ELEMENT_REMOVE_BY_INDEX_BUTTON = "section[name=\"remove-by-index\"]";
export const ELEMENT_SAVE_BUTTON = "footer>section[name=\"save-button\"]";
export const ELEMENT_CREATE_FIELDS = "main";

// Topic tags.
export const CONTAINER_TOPIC_TAGS_LIST = ".container__select>ul"
export const ELEMENT_TOPIC_TAGS = CONTAINER_TOPIC_TAGS_LIST + ">li[data-id=\"{}\"]";
export const CONTAINER_TOPIC_TAGS = ".container__topic-tags";
export const ELEMENT_SELECTED_TOPIC_TAGS = CONTAINER_TOPIC_TAGS + ">section[data-id=\"{}\"]";

export const ELEMENT_PINBOARD_FIELD = "input[name=\"pinboard\"]";
export const ELEMENT_TITLE_FIELD = "input[name=\"title\"]";
export const ELEMENT_DESCRIPTION_FIELD = "textarea[name=\"description\"]";
export const ELEMENT_ALTERNATIVE_TEXT_FIELD = "textarea[name=\"alternative-text\"]";
export const ELEMENT_LINK_FIELD = "input[name=\"link\"]";
export const ELEMENT_TOPIC_TAGS_FIELD = "input[name=\"topic-tags\"]";
export const ELEMENT_DATETIME_FIELD = "input[name=\"datetime\"]";
