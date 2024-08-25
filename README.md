## Project Overview

In this project, I handled the end-to-end process of designing and implementing a data-driven application, starting from conceptual design to user interaction. The main steps of the project are like these:

1. **Entity Relationship Diagram (ERD) Creation**: In the first step, I created an Entity Relationship Diagram to visually map out the data structure and relationships between different entities. This step was important for understanding the data requirements and how different entities relate to each other.

2. **Conversion to Logical Schema**: After finalizing the ERD, I converted it into a logical schema and defined the specific tables, columns, data types, and relationships that need to be implemented in the database. 

3. **Data Storage in Data Lakes**: To handle large volumes of data efficiently, I used Microsoft Azure's data lakes for storing raw and unstructured data. This approach allowed for scalable data storage and it was useful for the data analysis and processing needs in the future.

4. **Database Creation in PostgreSQL**: I created a relational database in PostgreSQL by implementing the logical schema. This involves setting up tables, defining primary and foreign keys, and ensuring data integrity through constraints and relationships.

5. **Database Optimization**: To improve performance and ensure efficient data retrieval, I implemented various optimization techniques. This included indexing frequently queried columns, partitioning large tables, and normalizing data to reduce redundancy. 

6. **Development of User Interface with Flask and React**: To allow users to interact with the database seamlessly, I developed a web application using Flask for the backend and React for the frontend. Flask serves as the RESTful API layer. It handles data requests and responses while React provides a user interface.

The document that explains this process can be found in **database-design.pdf** file. And the user-interface that is created at the end can be seen in the gif below.


![User Interface GIF](figures/user-interface.gif)
