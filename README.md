# YouTube Data Harvesting and Warehousing

A Streamlit-based application to harvest YouTube data using the YouTube Data API, process it, and store it in a MySQL database for further analysis.

## Features

- **Channel Insights**: Retrieve details about YouTube channels such as name, description, views, and subscription count.
- **Playlist and Video Data**: Fetch information about videos in a channel’s playlist, including views, likes, comments, and duration.
- **Comment Analysis**: Extract and store comments from videos for sentiment analysis or other use cases.
- **Data Storage**: Organize and store retrieved data in MySQL database tables for querying and analysis.
- **Query Interface**: Explore insights with predefined queries, such as top-performing videos and channels.

## Prerequisites

- **Python**: Python 3.8 or later.
- **MySQL**: A running MySQL database instance.
- **API Key**: A valid YouTube Data API key.

### Python Dependencies

Install the following Python packages:
- `streamlit`
- `google-api-python-client`
- `mysql-connector-python`
- `pandas`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your MySQL database:
   - Create a database named `CA_P1`.
   - Update the database connection details in the code (`host`, `user`, `password`).

4. Add your YouTube Data API key:
   Replace the placeholder `api_key` in the code with your actual API key.

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run Capstone_Project_1.py
    ```

2. Use the web interface to:
    - Enter a YouTube Channel ID to fetch channel data.
    - Analyze data with dropdown query options.

3. Query options include:
    - Videos and their respective channels.
    - Channels with the most videos.
    - Top 10 most viewed videos and more.

## Example Queries

- **Top 10 Most Viewed Videos**:
  Displays the most popular videos along with their view counts and respective channels.

- **Channels Publishing in 2022**:
  Lists channels that uploaded videos in 2022.

  # How the code works

## 1. **YouTube Data Retrieval**
- **API Configuration**: The YouTube Data API is initialized using an API key to interact with YouTube's data.
- **Functions for Data Fetching**:
  - `channel_data(ch_id)`: Retrieves channel details like name, description, subscriber count, and total views for a given channel ID.
  - `playlist_data(pl_id)`: Extracts video IDs from a channel’s upload playlist.
  - `video_data(vd_id)`: Fetches metadata (e.g., title, description, view count) for a specific video ID.
  - `get_comment_ids(vd_id)`: Retrieves comment IDs for a video.
  - `comment_data(cm_id)`: Fetches comment details such as author name, comment text, and publish date.

## 2. **Streamlit Web Interface**
- **Page 1**: Allows users to input a channel ID and displays:
  - Channel name and description.
  - Total views, subscriber count, and publication date.
- **Page 2**: Enables interaction with pre-defined queries through a dropdown menu to explore the stored data.

## 3. **Data Processing with pandas**
- **DataFrames**: 
  - The project uses `pandas` to create, manipulate, and process data for channels, videos, and comments.
  - Separate DataFrames (`channel_df`, `video_df`, `comment_df`) store the respective data before it is saved to the database.
- **Data Cleaning and Transformation**:
  - Converts API responses into structured tabular data.
  - Handles missing values and inconsistent formats (e.g., converting YouTube durations into seconds).
  - Ensures appropriate data types for storage and analysis.
- **Batch Inserts**:
  - `pandas` DataFrames are used to prepare data for batch inserts into MySQL tables, optimizing database storage.

## 4. **Database Storage**
- **Database Connection**: Connects to a MySQL database named `CA_P1`.
- **Database Schema**:
  - `channel_info`: Stores channel-related metadata.
  - `video_info`: Stores details of videos, including statistics and metadata.
  - `comment_info`: Stores information about video comments.
- **Data Storage**:
  - Cleaned and structured data from `pandas` DataFrames is stored in MySQL tables.
  - Data includes channel stats, video metadata, and user comments.

## 5. **Pre-defined Query Options**
Users can select queries from a dropdown menu, including:
- Names of all videos and their corresponding channels.
- Channels with the most videos.
- Top 10 most viewed videos and their channels.
- Videos with the highest number of likes or comments.
- Channels publishing videos in a specific year (e.g., 2022).
- Average video duration per channel.

## 6. **Data Transformation**
- Video durations are converted to seconds using `pandas` and regular expressions for consistent storage and analysis.
- Comments and statistics are processed to ensure structured storage.
- DataFrames allow seamless integration between raw API responses and MySQL storage.

## Workflow
1. User inputs a YouTube Channel ID or interacts with query options via the Streamlit interface.
2. The application fetches data from the YouTube Data API using modular functions.
3. Retrieved data is processed and cleaned using `pandas` DataFrames.
4. Processed data is stored in a MySQL database.
5. Users can query the database through the web interface to gain insights.

## Conclusion
This project leverages the power of **pandas** for efficient data handling, transformation, and analysis, alongside **MySQL** for persistent storage and **Streamlit** for user interaction. It provides an end-to-end system for YouTube data harvesting, storage, and analysis.
