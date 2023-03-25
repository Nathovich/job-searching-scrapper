# Job Searching Scrapper

This is currently a simple scrapper for the website pracuj.pl, which is in its early stages of development.

The scraper goes through the hardcoded urls that contain some filters as well as hardcoded keywords to be included in the preferable positions, as well as some keywords that exclude some offers that, even if they are within the first range, do not suit me, such as senior roles or roles that require speaking a language other than English. 

There are still some issues to investigate and resolve, such as receiving a link to a company profile, if an offer has a couple of localizations set, or senior roles are noted with a 'Sr' abbreviation. 

However, the code itself is quite easily manipulated to work for other purposes. 

## To be developed:

- url and both keywords list to be moved to separate files;
- offers with more than 1 localization to be scraped with an offer link;
- further scraping of the offers by checking requirements within each offer to be added;
- whole code to be rewritten with the use of selenium;
- other job board websites to be scraped, e.g. justjoin.it or nofluffjobs;
- possibly some interface and possibility to enter both types of keywords to be created.