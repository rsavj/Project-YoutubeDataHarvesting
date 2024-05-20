**YouTube Data Harvesting and Warehousing using SQL, MongoDB, and Streamlit**

http://192.168.1.2:8514

**Introduction**

YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQL, MongoDB, and Streamlit to create a user-friendly application that allows users to retrieve, store, and query YouTube channel and video data.

**Project Overview**

The YouTube Data Harvesting and Warehousing project consists of the following components:
- Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
- Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
- Store and Clean data : Once you retrieve the data from the YouTube API, store it in a suitable format for temporary storage before migrating to the data warehouse. You can use pandas DataFrames or other in-memory data structures
- Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
- Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
- Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data

**Technologies Used**

The following technologies are used in this project:
- Python: The programming language used for building the application and scripting tasks.
- Streamlit: A Python library used for creating interactive web applications and data visualizations.
- YouTube API: Google API is used to retrieve channel and video data from YouTube.
- MongoDB: A NoSQL database used as a data lake for storing retrieved YouTube data.
- SQL (MySQL): A relational database used as a data warehouse for storing migrated YouTube data.

**Installation and Setup**

To run the YouTube Data Harvesting and Warehousing project, follow these steps:
1. Install Python: Install the Python programming language on your machine.
2. Install Required Libraries: Install the necessary Python libraries using pip or conda package manager. Required libraries include Streamlit, MongoDB driver and Pandas
3. Set Up Google API: Set up a Google API project and obtain the necessary API credentials for accessing the YouTube API.
4. Configure Database: Set up a MongoDB database and SQL database (MySQL) for storing the data.
5. Configure Application: Update the configuration file or environment variables with the necessary API credentials and database connection details.
6. Run the Application: Launch the Streamlit application using the command-line interface.

**Usage**

Once the project is setup and running, users can access the Streamlit application through a web browser. The application will provide a user interface where users can perform the following actions:
- Enter a YouTube channel ID to retrieve data for that channel.
- Store the retrieved data in the MongoDB data lake.
- Collect and store data for multiple YouTube channels in the data lake.
- Select a channel and migrate its data from the data lake to the SQL data warehouse.
- Search and retrieve data from the SQL database using various search options.
- Perform data analysis and visualization using the provided features.

**Features**

The YouTube Data Harvesting and Warehousing application offers the following features:
- Retrieval of channel and video data from YouTube using the YouTube API.
- Storage of data in a MongoDB database as a data lake.
- Migration of data from the data lake to a SQL database for efficient querying and analysis.
- Search and retrieval of data from the SQL database using different search options, including joining tables.
- Support for handling multiple YouTube channels and managing their data.

**Future Enhancements**

Here are some potential future enhancements for the YouTube Data Harvesting and Warehousing project:
- Authentication and User Management: Implement user authentication and management functionality to secure access to the application.
- Scheduled Data Harvesting: Set up automated data harvesting for selected YouTube channels at regular intervals.
- Advanced Search and Filtering: Enhance the search functionality to allow for more advanced search criteria and filtering options.
- Additional Data Sources: Extend the project to support data retrieval from other social media platforms or streaming services.

**Conclusion**

The YouTube Data Harvesting and Warehousing project provides a powerful tool for retrieving, storing, and analyzing YouTube channel and video data. By leveraging SQL, MongoDB, and Streamlit, users can easily access and manipulate YouTube data in a user-friendly interface. The project offers flexibility, scalability, empowering users to gain insights from the vast amount of YouTube data available.

**References**

- Streamlit Documentation: [ https://docs.streamlit.io/library/api-reference](https://docs.streamlit.io/library/api-reference)
- YouTube API Documentation: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)
- MongoDB Documentation: [https://docs.mongodb.com/](https://docs.mongodb.com/)
- API Data Collection Reference Colab : [https://colab.research.google.com/drive/10PKu9YvhoPyIeWEjIAVuoJrVb3-snU8I?usp=sharing#scrollTo=SKOwdi9QdbJ9](https://colab.research.google.com/drive/10PKu9YvhoPyIeWEjIAVuoJrVb3-snU8I?usp=sharing#scrollTo=SKOwdi9QdbJ9)