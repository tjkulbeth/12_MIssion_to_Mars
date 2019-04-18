from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # SECTION 1 - NASA Mars News
    print("Beginning Section 1 NASA Mars News")
    browser = init_browser()
    url_mars = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_mars)
    html_mars = browser.html
    soup_mars = BeautifulSoup(html_mars, 'lxml')

    #Get most recent new article from mars
    news_title = soup_mars.find("div", class_='content_title').text

    #Get description of news article
    news_paragraph = soup_mars.find("div", class_='article_teaser_body').text

    print("End Section 1 NASA Mars News")
    browser.quit()

    # SECTION 2 - JPL Images
    print("Beginning Section 2 JPL Images")
    browser = init_browser()
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    browser.is_text_present("FULL IMAGE")
    browser.click_link_by_partial_text("FULL IMAGE")
    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'lxml')

    # find unique tag from style to locate data of interest
    image_location = soup_jpl.find('article')['style'].replace('background-image: url(', '').replace(');', '')[1:-1]
       # image_location
    featured_image_url = "https://www.jpl.nasa.gov" + image_location

    print("End Section 2 JPL Images")
    browser.quit()

    # SECTION 3 - Get mars weather from their twitter account
    print("Beginning Section 3 Get mars weather")
    browser = init_browser()
    url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_weather)
    html_mars_weather = browser.html
    soup_mars_weather = BeautifulSoup(html_mars_weather, 'lxml')
    mars_weather = soup_mars_weather.find('p', class_='tweet-text').text.replace('/n', '').split("pic")[0]
    print("End Section 3 Get mars weather")
    browser.quit()

    # SECTION 4 - Get mars facts using pandas
    print("Beginning Section 4 Get Mars Facts")
    browser = init_browser()
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(mars_facts_url)
    df = mars_tables[0]
    df.columns = ['Title', 'Value'] 
    html_facts = df.to_html(index_names=False, index=False, justify='left')
    html_facts.replace('\n', '')
    print("End Section 4 Get Mars Facts")
    browser.quit()

    # SECTION 5 - Scrape USGA Astrogeology to get images of Mar's hemisphweres
    print("Beginning Section 5 Get USGS Astrology")
    browser = init_browser()
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    html_mars_hemi = browser.html
    soup_mars_hemi = BeautifulSoup(html_mars_hemi, 'lxml')

    hemisphere_image_urls = []
    base_url = "https://astrogeology.usgs.gov"
        
    results = soup_mars_hemi.find_all("div", class_='item')
    results

    for result in results:
        image_url = result.find('a', class_='itemLink')['href']
        hemi_url = base_url + image_url
        browser.visit(hemi_url)
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html, 'lxml')
        title = hemi_soup.find('h2', class_='title').text
        image_loc = hemi_soup.find('a', target="_blank")["href"].strip()
        image_dict = {
            "title": title, "img_url": image_loc
        }
        hemisphere_image_urls.append(image_dict)

    print("End Section 5 Get USGS Astrology")
    browser.quit()
        
    # Generate dictionary on all the python data just scraped
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "image_location": image_location,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_facts,
        "mars_hemispheres": hemisphere_image_urls
    }

    return mars_data

if  __name__ == "__main__":
    data = scrape()
    print(data)

