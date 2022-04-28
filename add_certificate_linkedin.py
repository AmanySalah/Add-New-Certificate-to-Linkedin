from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
To use this script, you need to install Selenium Webdriver and add its path to the 'PATH' variable.
You can add your username and password to 'EMAIl' and 'PASSWORD' variables before running or it will ask you for them.
You can also add your certificate details or add them at the runtime. 
"""


PATH = ""
WEBSITE_LINK = "https://www.linkedin.com/"
EMAIL = ""
PASSWORD = ""

driver = webdriver.Chrome(PATH)
driver.get(WEBSITE_LINK)
driver.maximize_window()
WAIT = WebDriverWait(driver, 20)


"""
Sign in to linkedin in with your email and password.
"""


def sign_in(EMAIL, PASSWORD):
    if not EMAIL:
        EMAIL = input("Please Enter Your Email: ")

    if not PASSWORD:
        PASSWORD = input("Please Enter Your Password: ")

    sign_in_box = driver.find_element(by=By.ID, value="session_key")
    sign_in_box.send_keys(EMAIL)

    sign_in_pass = driver.find_element(by=By.ID, value="session_password")
    sign_in_pass.send_keys(PASSWORD)

    sign_in_btn = driver.find_element(by=By.CLASS_NAME, value="sign-in-form__submit-button")
    sign_in_btn.click()


"""
Get username and open the profile using link text.
"""


def open_profile():
    # profile = WAIT.until(
    #         EC.presence_of_element_located((By.ID, "ember33")))
    # profile.click() #works

    username = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.t-16"))).text
    print("Username: ", username)
    try:
        profile_link = WAIT.until(
            EC.presence_of_element_located((By.LINK_TEXT, username))
        )
        # print("profile link:", profile_link)
        profile_link.click()
    except:
        print("Sorry, couldn't open your profile.")
        driver.quit()


"""
Open Add license or certification window, and make sure it's loaded
If certificate details aren't ready, ask the user for them.
If there are errors, print them.
"""


def add_certificate():
    edit_btns = WAIT.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pvs-header__right-container a")))
    add_cert_link = driver.current_url + "edit/forms/certification/new/?profileFormEntryPoint=PROFILE_SECTION&trackingId=qAiO0kwtTdi6IBjn6gzeaw%3D%3D"
    driver.get(add_cert_link)
    # WAIT.until(EC.url_changes(add_cert_link))
    driver.switch_to.window(driver.window_handles[-1])

    layer = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.artdeco-modal")))
    print("Layer loaded!")

    certificate_name = "NEW CERTIFICATE"
    if not certificate_name:
        certificate_name = input("Please Enter the Certificate Name: ")
    certificate_name_input = WAIT.until(EC.presence_of_element_located((By.ID, "single-typeahead-entity-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-name")))
    # print(certificate_name_input.get_attribute('placeholder'))
    certificate_name_input.send_keys(certificate_name)

    organization_name = "ORGANIZATION"
    if not organization_name:
        organization_name = input("Please Enter the Organization Name: ")
    organization_name_input = WAIT.until(EC.presence_of_element_located((By.ID, "single-typeahead-entity-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-company")))
    organization_name_input.send_keys(organization_name)

    issue_month, issue_year = "5", "2021"
    if not issue_month or not issue_year:
        issue_month = input("Please Enter the Issue Month (as a number): ")
        issue_year = input("Please Enter the Issue Year (as a number): ")

    select_issue_month = Select(driver.find_element(by=By.ID, value="date-range-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-dateRange-start-date"))
    select_issue_month.select_by_value(issue_month) # Select by value, the user is supposed to enter the month as a number.
    # select_issue_month.select_by_visible_text(issue_month)  # April, June, ...

    select_issue_year = Select(driver.find_element(by=By.ID, value="date-range-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-dateRange-start-date-year-select"))
    select_issue_year.select_by_value(issue_year)

    credential_id = ""
    if not credential_id:
        credential_id = input("Please Enter Your Credential ID (optional): ")
    credential_id_input = WAIT.until(EC.presence_of_element_located((By.ID, "single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-licenseNumber")))
    credential_id_input.send_keys(credential_id)

    credential_url = ""
    if not credential_url:
        credential_url = input("Please Enter Your Credential URL (optional): ")
    credential_url_input = driver.find_element(by=By.ID, value="single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADH5D98BLCOVTBiBwVpNq6C8tsyT2uantEI-1-url")
    credential_url_input.send_keys(credential_url)

    save_div = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.artdeco-modal__actionbar")))
    save_btn = save_div.find_element(by=By.TAG_NAME, value="button")
    save_btn.click()

    try:
        uncompleted = WAIT.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.artdeco-inline-feedback__message")))
        print("Missing or invalid values: ")
        for error in uncompleted:
            print(error.text)
        print("Missing or invalid values, I'm quitting..")
        driver.quit()
    except:
        print("Certificate/Licence Added Successfully!")
        driver.quit()


def main():
    sign_in(EMAIL, PASSWORD)
    open_profile()
    add_certificate()


if __name__ == "__main__":
    main()
