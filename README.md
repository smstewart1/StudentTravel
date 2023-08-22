In this project, I looked to model the likelihood of students moving between campuses in anticipation of a campus closure due to foreseen campus upgrades.  

The first step of the project was exploratory data analysis in PowerBI to determine if there were any factors which affected how far students were willing to travel in order to attend a given campus, such as ethnicity, gender, course modality, and the ccourse being taught.  The EDA was also used to look at overall trends in campus enrollment, such as the number of students and where (geographically) students were coming from.
The PowerBI visualization can be accessed here:  <iframe title="TravelByStudents" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=448c3286-cd90-47a0-a5c7-c83b819e6f77&autoAuth=true&ctid=16cc8ad9-84fe-481d-b9b0-48e7758c41aa" frameborder="0" allowFullScreen="true"></iframe>

Tavel distances were estimated by converting student zip codes to latitude/longitude pairs and compairing them to the latitude and longitude of the given campus.  Data was pooled over a 10 year period.

Some key findings were:
- students will typically only tavel to a campus that is within 15-20 miles of their home zip code
- as shown below, there is litle impact of student demographic on the travel distance
![image](https://github.com/smstewart1/StudentTravel/assets/107202785/f8a10b81-51a6-4262-8ede-bfc749999806)
- similarly, there is little impact of the course on the distance traveled
![image](https://github.com/smstewart1/StudentTravel/assets/107202785/64cd2091-a7db-477b-a8ac-7b881cd98a3f)

The probability density function (PDF) of students attending was fit to a log normal distribution and models were built around both campus and courses to see how much variability there was between the models.  
![CHM-090_g0](https://github.com/smstewart1/StudentTravel/assets/107202785/315b7d80-ab25-420f-ab0f-27a41471910d)
![CHM-151_g0](https://github.com/smstewart1/StudentTravel/assets/107202785/0e96dfe6-2ee9-4267-a2ef-e197d9354e7f)
![CHM-152_g0](https://github.com/smstewart1/StudentTravel/assets/107202785/dfe1a5e1-379e-4cc8-b009-bb1dd23966e3)
![CHM-251_g0](https://github.com/smstewart1/StudentTravel/assets/107202785/62cd011c-bfb4-4c52-b92b-26b4ad9b54ab)
![CHM-252_g0](https://github.com/smstewart1/StudentTravel/assets/107202785/384eee41-e2c8-4593-98be-5e0d1a549082)

Using a log normal distribution, the next step was to model how many students would actually go to another campus assuming a campus closure.

The distribution of students was estimated using historic data, shown below
![image](https://github.com/smstewart1/StudentTravel/assets/107202785/1fa93724-295d-47dc-a0fb-75fc14e7db94)

This is an on going project, and as of this revision, the next step is to use historic enrollment data to estimate the demand for each courses on the old campus, then use the models built here to estimate how many of those students will choose to enrollment on a different campus.  
