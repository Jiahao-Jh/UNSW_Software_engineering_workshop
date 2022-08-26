# SENG3011_GroupName

Team Members:
| Name          | Email         | 
| ------------- |:-------------:| 
| Shuhao Hu    | shuhao.hu@student.unw.edu.au |
| Kexin Tian     | z5212870@ad.unsw.edu.au     |
| Jiahao Zhang | zhangjiaho890@gmail.com     |
| Dongfei Fan | z5211565@ad.unsw.edu.au     |
| Haochen Shi | z5255218@ad.unsw.edu.au   |

Project Introduction:
After the COVID-19 global pandemic, it raises people’s attention on the early detection of infectious disease. The Integrated Systems for Epidemic Response(ISER) at UNSW is a organization that working on this area. The EpiWATCH system they developed using open-source data detected many infectious diseases in very early stage and contribute towards global epidemic response.

In our project, we plan to develop a platform and an API towards our benchmark EpiWATCH system. The API we developed would be able to access by other teams in SENG3011 to find disease reports in CDC.

> Stage 1 is to build an API which will handle requests from users about disease outbreaks from [CDC Websites](https://www.cdc.gov/outbreaks)
> 
> Stage 2 is to build an Web interface using stage 1 APIs based on our own API or other teams APIs


Python is used to scrape disease articles and reports from [CDC Websites](https://www.cdc.gov/outbreaks)

AWS API Gateway is used to handle user requests and pass user parameters to python scraper

# Demo

The website is currently disabled, the following images are kept as demonstration.

## project structure
![Alt text](/images/4.jpg)


## project functionality

![Alt text](/images/project_diagram.jpg)

## project website demo
![Alt text](/images/HomePage.jpg)
![Alt text](/images/articlePage.jpg)
![Alt text](/images/1.jpg)
![Alt text](/images/2.jpg)
![Alt text](/images/3.jpg)