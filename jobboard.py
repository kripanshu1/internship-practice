import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_indeed_jobs(query, location):
    base_url = "https://www.indeed.com/jobs"
    params = {
        'q': query,
        'l': location,
        'start': 0
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
        'Referer': 'https://www.indeed.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(base_url, params=params)
        time.sleep(1)  # polite delay
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to retrieve jobs: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('div', class_='job_seen_beacon')

    jobs = []
    for job in job_cards:
        title_elem = job.find('h2', class_='jobTitle')
        company_elem = job.find('span', class_='companyName')
        location_elem = job.find('div', class_='companyLocation')
        link_elem = job.find('a', href=True)

        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        company = company_elem.get_text(strip=True) if company_elem else 'N/A'
        location = location_elem.get_text(strip=True) if location_elem else 'N/A'
        link = "https://www.indeed.com" + link_elem['href'] if link_elem else 'N/A'

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'link': link
        })

    return jobs

def save_jobs_to_csv(jobs, filename='job_listings.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'company', 'location', 'link'])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    print(f"Saved {len(jobs)} jobs to {filename}")

def main():
    query = input("Enter job title or keywords to search: ").strip()
    location = input("Enter job location: ").strip()
    jobs = scrape_indeed_jobs(query, location)
    if jobs:
        save_jobs_to_csv(jobs)
    else:
        print("No jobs found or failed to scrape.")

if __name__ == "__main__":
    main()
