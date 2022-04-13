from scrape_csv import ScriptScraper
import csv

def run_script_scraper(titles, site_url, thread_count, download_directory):
    # Initialize the "Springfield, Springfield" screen scraper
    scraper = ScriptScraper(titles,
                            site_url,
                            thread_count,
                            download_directory
                            )

    print('Starting script scraping procedure:\n\ttitles:{titles}'
            .format(
            titles=str(titles)
            )
        )
    scraper.scrape_site()
    print('Script scraping procedure completed. Check log for details.')


if __name__ == '__main__':
    # Parameters for scraping scripts from "Springfield, Springfield" site
    site_url = 'https://www.springfieldspringfield.co.uk'
    thread_count = 4
    download_directory = 'test'

    with open('try.csv', newline='') as f:
        reader = csv.reader(f)
        titles = list(reader)
    # Engage!
    run_script_scraper(titles, site_url, thread_count, download_directory)
