## Create table use command

```
python pipeline/model.py
```


## Sql for create table

```
CREATE TABLE pyml.crawl_data (
	id INT auto_increment primary key NOT NULL,
	`domain` varchar(255) NULL,
    `url` varchar(255) NULL,
	title varchar(255) NULL,
	content LONGTEXT NULL,
	`date` DATETIME NULL,
	tags json NULL
    `created_at` DATETIME NULL,
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;

```

# Run crawl daily for site

```
from imp import reload

import cl_crawl.helper as helper
import cl_crawl.vtc_new as vtc_new
import crawl
reload(crawl)
reload(helper)


tn = crawl.CrawlCafeF()
tn.run(daily=True)

crawl.VnexpressCrawler().run(daily=True)

crawl.VnEconomySpider().run(daily=True)

crawl.CrawlThanhNien().run(daily=True)

vtc_new.VTCCrawler().run(daily=True)

driver = crawl.create_driver()
driver2 = crawl.create_driver()

vs = crawl.CrawlVietStock(driver=driver, driver2=driver2)
vs.run(fresh_start=True, daily=True)

driver.quit()
driver2.quit()
```