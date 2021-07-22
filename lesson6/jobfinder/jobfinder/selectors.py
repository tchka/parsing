NAVIGATION_SELECTORS = {
    'parse_item': '//div[contains(@data-qa, "vacancy-serp__results")]\
    /div[contains(@data-qa, "vacancy-serp__vacancy")]\
    //a[contains(@data-qa, "vacancy-title")]/@href',
    'parse': '//a[contains(@data-qa, "pager-next")]/@href',
}
ITEM_SELECTORS = {
    'title': '//h1/text()',
    'salary': '//p[contains(@class, "vacancy-salary")]//text()'
}
SJ_NAVIGATION_SELECTORS = {
    'parse_item': '//*[contains(@class,"f-test-vacancy-item")]\
    //a[@target="_blank"]/@href',
    'parse': '//a[contains(@class, "f-test-button-dalshe")]/@href',
}
SJ_ITEM_SELECTOR = {
    'title': '//h1/text()',
    'salary': '//h1/../span//text()'
}
