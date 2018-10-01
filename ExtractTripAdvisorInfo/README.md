
### Functionalities

get_tripadvisor : extract information for one page of Tripadvisor restaurants.

crawl_restaurant_tripadvisor: extract information for all the Tripadvisor restaurants in a specific city. 

### Information to extract
* Name restaurant
* Ranking position
* Evaluation
* Number of reviews
* Food categories

### Prerequisites

* Python 3
* requests
* urllib
* bs4
* Selenium

### Installation

* requests or urllib to make request and download html code of the wepages.
* bs4 to extract information from html code
* Selenium to automate web browser interaction (check out https://selenium-python.readthedocs.io/installation.html#drivers , to download the driver)

### Examples

dfout = get_tripadvisor(URL = "https://www.tripadvisor.es/Restaurants-g187438-Malaga_Costa_del_Sol_Province_of_Malaga_Andalucia.html")

dfout = crawl_restaurant_tripadvisor(nameCity="Málaga")
