export const SNACKBAR_HTML_ELEMENT = `
    <section class="snackbar__element" data-uuid="{}">
        <i class="icon__material icon__large"></i>
        <p></p>
    </section>`;

export const DATA_FILE_HTML_ELEMENT = `
    <section type="checkbox" class="container__list-element container__list-text">
        <i class="icon__material icon__medium">description</i>
        <p data-file="{}" class="notranslate">{}</p>
    </section>`;

export const ACCOUNT_HTML_ELEMENT = `
    <section type="checkbox" class="container__column container__account-element">
        <img src="{}" onerror="this.onerror=null; this.src='./assets/profile-picture.svg';">
        <section class="container__account-text">
            <span title="{}" data-uuid="{}" class="notranslate">{}</span>
            <span>{}</span>
        </section>
    </section>`;

export const CONSOLE_HTML_ELEMENT = `
    <section class="container__row container__gap-medium container__list-element">
        <section class="container__column container__list-text container__console-title">
            <span>{}</span>
        </section>
        <section class="container__column container__console-message">
            <p>{}</p>
            <p class="notranslate">{}</p>
        </section>
    </section>`;

export const CONSOLE_HTML_ELEMENT_BACKGROUND = `
    <section class="container__row container__gap-medium container__list-element" style="background: {};">
        <section class="container__column container__list-text container__console-title">
            <span>{}</span>
        </section>
        <section class="container__column container__console-message">
            <p>{}</p>
            <p class="notranslate">{}</p>
        </section>
    </section>`;

export const TAG_LIST_HTML_ELEMENT = `
    <li class="container__column" data-id="{}" data-value="{}" data-tag-value="{}" type="button">
        <span>{}</span>
        <span>{}</span>
    </li>`;

export const TOPIC_TAG_HTML_ELEMENT = `
    <section class="container__row container__gap-medium"
        data-id="{}" data-value="{}" data-tag-value="{}">
        <span>{}</span>
        <i type="button" class="icon__material icon__small icon__clear">clear</i>
    </section>`;
