# Spider information
The function of this spider is extracting information from 
Amazon marketplace, specifically the result of the search
of NVIDIA RTX 3060.

To run this spider you have to install scrapy first
```
> pip install scrapy
```

And then, you have to run this command:
```
> scrapy crawl gpus-spider 
```
If you want to store the results you can use this command
```
> scrapy crawl gpus-spider -o gpus.csv
```
