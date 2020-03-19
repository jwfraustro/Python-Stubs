import pyperclip
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

draft_url = r"https://bulksell.ebay.com/ws/eBayISAPI.dll?SingleList&&DraftURL=https://www.ebay.com/sh/lst/drafts&ReturnURL=https://www.ebay.com/sh/lst/drafts&sellingMode=AddItem&templateId=5578480015&returnUrl=https://bulksell.ebay.com/ws/eBayISAPI.dll?SingleList"

def del_desc(element):
    for i in range(88):
        element.send_keys(Keys.DELETE)

def paste_element(element, text):
    element.send_keys(Keys.LEFT_CONTROL, "a")
    element.send_keys(text)

def launch_browser():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(chrome_options=chrome_options)

    return browser

def create_product(browser):

    if browser.current_url != draft_url:
        browser.get(draft_url)

    print("\n------- Ebay Item -------")
    title = input("\nItem Title: ")
    sku = input("SKU: ").upper()
    upc = "Does not apply"

    condition = input("\nCondition: (NE, NOS, USED, CORE) ").upper()
    if condition in ['NOS', 'USED', 'CORE']:
        cond_desc = input("Condition Description: ")
    else:
        cond_desc = None

    try:
        if condition == "NE":
            condition = "New"
        if condition == "NOS":
            condition = "New other (see details)"
        if condition == "USED":
            condition = "Used"
        if condition == "CORE":
            condition = "For parts or not working"
    except:
        condition = "Used"

    brand = input("\nBrand: ")
    if not brand:
        brand = "N/A"
    mpn = input("MPN: ")
    if not mpn:
        mpn = "N/A"
    try:
        qty = input("\nQuantity: ")
    except:
        qty = 1

    price = input("\nPrice: ")

    if int(qty) == 1:
        shipping = input("Shipping: ")
    if int(qty) > 1:
        base_shipping = input("Base Shipping: ")
        add_shipping = input("Additional Shipping per Item: ")

    desc_text = []
    desc_text.append("<strong>")
    print("\n-----Item Description----\n")
    while True:
        line = input("> ")
        if line == 'q':
            break
        if line == 'pn':
            desc_text.append("P/N: %s<br>" % mpn)
            continue
        if line == '':
            desc_text.append("<br>")
            continue
        if line == 'cond':
            desc_text.append("%s<br>" % cond_desc)
            continue
        if line == 'large':
            desc_text.append(
                "This is a large item, and will need to be shipped freight via LTL. Please contact us before purchasing for an accurate shipping quote.<br>")
        else:
            desc_text.append("%s<br>" % line)
            continue

    desc_text.append("</strong>")

    title_box = browser.find_element_by_id("editpane_title")

    paste_element(title_box, title)
    sku_box = browser.find_element_by_id("editpane_skuNumber")
    paste_element(sku_box, sku)

    upc_box = browser.find_element_by_id("upc")
    paste_element(upc_box, upc)

    condition_box = Select(browser.find_element_by_id("itemCondition"))

    try:
        condition_box.select_by_visible_text(condition)
    except:
        condition = "Used"
        condition_box.select_by_visible_text(condition)

    if cond_desc:
        cond_desc_box = browser.find_element_by_id("editpane_condDesc")
        paste_element(cond_desc_box, cond_desc)

    brand_box = browser.find_element_by_id("Listing.Item.ItemSpecific[Brand]")
    paste_element(brand_box, brand)

    mpn_box = browser.find_element_by_id("Listing.Item.ItemSpecific[Manufacturer Part Number]")
    paste_element(mpn_box, mpn)

    qty_box = browser.find_element_by_id("quantity")
    paste_element(qty_box, qty)

    price_box = browser.find_element_by_id("binPrice")
    paste_element(price_box, price)

    if int(qty) == 1:
        ship_box = browser.find_element_by_id("shipFee1")
        paste_element(ship_box, shipping)
    if int(qty) > 1:
        ship_box = browser.find_element_by_id("shipFee1")
        paste_element(ship_box, base_shipping)
        add_ship_box = browser.find_element_by_id("xShipFee1")
        paste_element(add_ship_box, add_shipping)

    ActionChains(browser).move_to_element(brand_box).perform()

    input("Press enter when photos added...")

    pyperclip.copy(''.join(desc_text))

    print("Pasting Item Description...")
    ActionChains(browser).move_to_element(browser.find_element_by_id("descDiv")).perform()
    browser.find_element_by_css_selector("a[aria-label='HTML']").click()
    browser.switch_to.frame(browser.find_element_by_name('v4-31txtEdit_ht'))
    desc_box = browser.find_element_by_xpath('html/body')
    desc_box.click()

    input("\nPress enter to start new draft...")

    return

def draft_maker():

    browser = launch_browser()

    browser.get(draft_url)

    input("Press enter when logged in...")

    while True:
        create_product(browser)

if __name__ == '__main__':
    draft_maker()
