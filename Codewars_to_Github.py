import os
import easygui
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from github import Github

from scripts.decorators import logtime


def selenium_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = 'temp/chromedriver.exe'
    browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    return browser


def login():
    msg = "Login into CodeWars"
    title = "Login window"
    field_names = ["UserID", "Password"]
    field_values = easygui.multpasswordbox(msg, title, field_names)

    while True:
        if field_values is None:
            break
        errmsg = ''
        for i in range(len(field_names)):
            if field_values[i].strip() == "":
                errmsg = f'{field_names[i]} is a required field. \n\n'
        if errmsg == '':
            break
        field_values = easygui.multpasswordbox(errmsg, title, field_names, field_values)
    return field_values


def page_connect(user_email, user_password):
    user_name = os.getenv('USER_NAME')
    browser = selenium_chrome()
    browser.get('https://www.codewars.com/users/sign_in')
    browser.find_element_by_id('user_email').send_keys(user_email)
    browser.find_element_by_id('user_password').send_keys(user_password)
    browser.find_element_by_xpath('//button[text()="Log In"]').click()
    profile_url = f'https://www.codewars.com/users/{user_name}/completed_solutions'
    browser.get(profile_url)
    browser.execute_script('window.scrollTo(0, 5000)')
    time.sleep(2)
    return browser.page_source


def github_connect():
    user = Github(os.getenv('GITHUB_TOKEN')).get_user()
    repo_name = 'CodeWars'
    kata_names = [repo for repo in user.get_repos()]
    if repo_name not in kata_names:
        user.create_repo(repo_name)
    return user.get_repo(repo_name)


def copy_details(link):
    browser = selenium_chrome()
    browser.get(f'https://www.codewars.com{link}')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    return str(soup.find(id='description').find('p'))


@logtime
def main():
    page_temp = 'temp/page_temp.html'
    page_txt = open(page_temp, 'r+')
    if os.path.getsize(page_temp) == 0:
        login_window = login()
        page_txt.write(page_connect(login_window[0], login_window[1]))

    code = []
    soup = BeautifulSoup(page_txt.read(), 'lxml')
    results = soup.find_all('div', class_='list-item solutions')
    repo = github_connect()
    for i, kata in enumerate(results):
        link = kata.find('a')['href']
        name = kata.find('a').contents[0]
        for x in kata.find_all('span'):
            code.append(x.get_text())
        code.append('|')
        ret = ''.join(code).split('|')
        repo.create_file(f'{name}/README.md', 'Copy from CodeWars', copy_details(link)[3:-4], branch='test')
        repo.create_file(f'{name}/{name}.py', 'Copy from CodeWars', ret[i], branch='test')


if __name__ == '__main__':
    main()
