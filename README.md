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