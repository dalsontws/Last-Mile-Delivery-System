# Hotspotting - Our Last Mile Delivery System

This is a project developed during the [ŠKODA Smart Mobility Hackathon 2019](https://www.ceehacks.com/smhprague2019/) held at [ŠKODA AUTO DigiLab, Prague](https://skodaautodigilab.com/). 

![hackathon-group](images/group.jpg?raw=true "Title")

We took on the challenge of Effective Delivery.
Based on a set of data about deliveries collected from more than 500.000 delivery rides, we have to find the best possible route planning and effective use of resources available. 

We created an algorithm that finds bottlenecks based on the data provided from [DoDo](https://idodo.cz/en/for-partners-2/), a Czech Republic delivery company to discover cases of the low driver and car utilization.

Last mile delivery has been a problem identified in Prague; a possible cause is the difficulty of movement from existing transportation networks (roads,  railway stations, bus depots, and ferry berths) to the ending location or destination.

This algorithm allows us to identify possible bottlenecks due to the last mile. 
Using the algorithm, we can identify bus stops in Prague as possible areas for drop off for food deliveries, and afterwards completed by different modes of transportation (cycling) to complete the last mile. 

From the starting location, we will use the conventional mode of transport (car, motorbike) to the identified bus stop, and continue the last mile journey to the destination using a bicycle. 

### How it works

The python script `bus-stop-identifier.py` takes in an existing data set with bus stop data and identify a singular bus stop between the **starting location** and the **destination** that is optimal. 
An optimal bus stop consists of the shortest time taken from **starting location** to bus stop using a car/motorbike, together with the shortest time taken from that bus stop to the **destination** using a bicycle. 

### Prerequisites

- Python 3.6 or above

### Libraries and APIs used

- Pandas for data manipulation and extraction
- Requests for API calls 
- Glob for iteration of data files (in csv)
- HERE REST API for Route Planning


### Authors

* **Dalson Tan** - *Initial work* - [dalsontws](https://github.com/dalsontws)

### Acknowledgments

* DoDo for providing historical dataset for algorithm implementation
* HERE Maps for their route planning API
