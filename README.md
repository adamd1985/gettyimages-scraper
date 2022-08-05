# A Python Scraper with Beautiful Soup
 <!-- title: A Python Scraper with Beautiful Soup -->

# Python Components

Create an environment for it:

`conda create -n gettyscrapy python=3.8 -y`
`conda activate gettyscrapy`

install these packages:

`conda install scrapy beautifulsoup4 pysqlite3 -y`

# Project Structure

For a scrapy quickstart use:
`scrapy startproject the_scraper_projectname`

This will generate a Scrapy project in this format:

- the_main_dir
  - the_scraper_projectname
    - *settings.py* - parameters for scrapers and runners, e.g multithreading, bot name, respect robot.txt guidelines, etc.
    - *items.py* - the structured data coming out of a scraper.
    - *middleware.py* - additional functionality provided by scrapy or hooks in various stages of the lifecycle.
    - *pipeline.pys* - glueing everything togther and persisting the data somewhere.
    - *spiders* - where are scrapers are located
      - *spider1.py*
  - *scrapy.cfg* - Holds important variables for a scrapy deployment, e.g. project name and configuration file path.
  


## Spiders Structure

Another quickstart here:

`scrapy genspider -t crawl gettyimages gettyimages.com`

with this setup, you can deploy the scraper using:

`scrapy crawl gettyimages`

In production, you might utilize a spider runner like (scrapyd)[https://docs.scrapy.org/en/latest/topics/deploy.html#deploy-scrapyd]

For our pipeline though, we are treating this as a full python project, therefore we have a main.py *outside the project structure*, where the crawlers are configured there and run on a reactor:

```python
# The path is seen from root, ie. from main.py
settings_file_path = 'gettyscraper.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

settings = get_project_settings()
runner = CrawlerRunner(settings)
runner.crawl(GettyImagesSpider)

d = runner.join()

d.addBoth(lambda _: reactor.stop())
reactor.run()
```

# Closing Comments

**NB**: Inspired by amatuerish technical interviews, were they want you to build an entire app just by reading their mind (ahem: Kalepa). For whomever you want to work with these interviewers, you are welcome!

<div align="right">Made with :heartpulse: by <b>Adam</b></div>
