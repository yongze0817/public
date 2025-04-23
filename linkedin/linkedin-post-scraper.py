# Import necessary libraries
from numpy import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def log_linkedin():
    # LinkedIn Credentials
    username = "" # 填写LinkedIn账户用户名
    password = "" # 填写LinkedIn账户密码

    # Initialize WebDriver for Chrome
    browser = webdriver.Chrome()

    # Open LinkedIn login page
    browser.get('https://www.linkedin.com/login')

    # Enter login credentials and submit
    elementID = browser.find_element(By.ID, "username")
    elementID.send_keys(username)
    elementID = browser.find_element(By.ID, "password")
    elementID.send_keys(password)
    elementID.submit()

    time.sleep(random.uniform(3,7))

    return browser

def post_sraper(browser, page):
    # Set LinkedIn page URL for scraping
    page = page

    # Navigate to the posts page of the company
    post_page = page + '/recent-activity'
    post_page = post_page.replace('//recent-activity', '/recent-activity')
    browser.get(post_page)

    # Extract company name from URL
    prof_name = page.rstrip('/').split('/')[-1].replace('-', ' ').title()
    # prof_name = prof_name

    # Set parameters for scrolling through the page
    SCROLL_PAUSE_TIME = 20
    MAX_SCROLLS = False
    last_height = browser.execute_script("return document.body.scrollHeight")
    scrolls = 0
    no_change_count = 0

    # Scroll through the page until no new content is loaded
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        no_change_count = no_change_count + 1 if new_height == last_height else 0
        if no_change_count >= 3 or (MAX_SCROLLS and scrolls >= MAX_SCROLLS):
            break
        last_height = new_height
        scrolls += 1

    # Parse the page source with BeautifulSoup
    prof_page = browser.page_source
    linkedin_soup = bs(prof_page.encode("utf-8"), "html.parser")

    # prof_name = linkedin_soup.find('title')
    # prof_name = prof_name.split(" | ")[1]
    # print(prof_name)

    containers = linkedin_soup.find_all("li",{"class":"nQvGpufOVFqrtGWPZRxlQpWSLqoatrYPEbNbFwk"})
    post_number = len(containers)

    print(post_number)
    # Save the parsed HTML to a file
    with open(f"post_data/{prof_name}_soup.txt", "w+", encoding='utf-8') as t:
        t.write(linkedin_soup.prettify())


    # Define a data structure to hold all the post information
    posts_data = []


    # Function to extract text from a container
    def get_text(container, selector, attributes):
        try:
            element = container.find(selector, attributes)
            if element:
                return element.text.strip()
        except Exception as e:
            print(e)
        return ""


    # Function to extract media information
    def get_media_info(container):
        media_info = [("div", {"class": "update-components-header__text-wrapper"}, "Shared Post"),
                    ("div", {"class": "update-components-video"}, "Video"),
                    ("div", {"class": "update-components-linkedin-video"}, "Video"),
                    ("div", {"class": "update-components-image"}, "Image"),
                    ("article", {"class": "update-components-article"}, "Article"),
                    ("div", {"class": "feed-shared-external-video__meta"}, "Youtube Video"),
                    ("div", {"class": "feed-shared-poll ember-view"}, "Other: Poll, Shared Post, etc")]

        for selector, attrs, media_type in media_info:
            element = container.find(selector, attrs)
            if element:
                if media_type == "Shared Post":
                    return "None", media_type
                else:
                    link = element.find('a', href=True)
                    return link['href'] if link else "None", media_type
        return "None", "Unknown"


    # Main loop to process each container
    for container in containers:
        post_text = get_text(container, "div", {"class": "update-components-text relative update-components-update-v2__commentary"})
        # print(post_text)
        
        media_link, media_type = get_media_info(container)
        
        # Date
        post_date = get_text(container, "span", {"class": "update-components-actor__sub-description text-body-xsmall t-black--light"})
        import re
        post_date = re.sub(r'\s*•\s*', ' • ', post_date.replace('\n', ' '))
        print(post_date)

        # Likes
        post_likes = get_text(container, "span",{"class":"social-details-social-counts__reactions-count"})

        # Comments
        comment_element = container.find_all(
            lambda tag: tag.name == 'button' and 'aria-label' in tag.attrs and 'comment' in tag['aria-label'].lower())
        comment_idx = 0
        post_comments = comment_element[comment_idx].text.strip() if comment_element and comment_element[
            comment_idx].text.strip() != '' else 0
        if post_comments == 'Comment':
            post_comments=0

        # Shares
        shares_element = container.find_all(
            lambda tag: tag.name == 'button' and 'aria-label' in tag.attrs and 'repost' in tag['aria-label'].lower())
        shares_idx = 1 if len(shares_element) > 1 else 0
        post_shares = shares_element[shares_idx].text.strip() if shares_element and shares_element[
            shares_idx].text.strip() != '' else 0

        # Append the collected data to the posts_data list
        posts_data.append({
            "Page": prof_name,
            "Number": post_number,
            "Date": post_date,
            "Post Text": post_text,
            "Media Type": media_type,
            "Likes": post_likes,
            "Comments": post_comments,
            "Shares":post_shares,
            "Media Link": media_link
        })


    try:
        df = pd.DataFrame(posts_data)
    except:
        for item in list(posts_data.keys()):
            print(item)
            print(len(posts_data[item]))

    for col in df.columns:
        try:
            df[col] = df[col].astype(int)
        except:
            pass


    # Export the DataFrame to a CSV file
    csv_file = f"post_data/{prof_name}_posts.csv"
    df.to_csv(csv_file, encoding='utf-8', index=False)
    print(f"Data exported to {csv_file}")


if "__main__":
    
    file_path = "faculty_linkedin post.xlsx"

    sheet_name = "list"  
    list = pd.read_excel(file_path, sheet_name=sheet_name)
    filtered_list = list[list['Unnamed: 5'] == 'Y']

    # initialize Chrome options
    chrome_options = Options()

    browser = log_linkedin()

    for page in filtered_list['LinkedIn_url']:
        post_sraper(browser, page)