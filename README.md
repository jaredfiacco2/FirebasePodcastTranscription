
<!-- PROJECT SHIELDS -->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/jaredfiacco2/FirebasePodcastTranscription">
    <img src="images/transcript.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Store Podcast Transcriptions in GCP Firebase</h3>

  <p align="center">
    This code takes an XML RSS-feed of my favorite podcast, "DarkNet Diaries", translates he data into a Python Dataframe, stores itlocally as a ".pkl" file, stores it in Google Cloud Platform's "Firebase" NoSQL database. Then, python loops through the firebase stream, locally transcribing the podcasts and storing the transcription in the firebase. The ".pkl" files are used for data mining and.  
    <br />
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

- My favorite podcast is more than 100 episodes and counting, all ~1hr each. After binging it in a month, I found myself wanting to search for episodes to rewatch or solidify interesting facts. This project enables cheap storage in the cloud, transcript searchability, and statistical research and NLP projects in the future.

- I take an RSS XML feed, loop through podcasts mp3 links, transcribing them, and storing the results locally as .pkl files and in the cloud in a firebase.  

<img src="images\processmap.png" alt="Demo"/>

### Built With

* [Python](https://python.org)
* [Firebase](https://firebase.google.com/docs/firestore)
* [RSS]
* [XML]
* [JSON]
* [PKL]

### Prerequisites

1. Installing all Required Packages
  ```sh
  pip install -r requirements.txt
  ```

2. In SSMS, Create Database Called "DataDocumentation". 

3. Create Service Account & Role
    - Service Account
        - In Server Secutiry, create a Service Account
        - Take note of the Username and password, you will use this to update the credentials in runDataDocVisual.py 
    - Role
        - In the DataDocumentation database, 

4. Open the SQL folder, run each of the files
    - First, run "Table_D.sql" files
    - Next, run "vView.sql" files
    - Finally, fun "StoredProcedures_SP" files

5. Update Server Acces Credentials in runDataDocVisual.py  

6. Target a specific node of interest vs show all nodes in server
    - To Target a node of interest, run the "Filter_EdgesAndNodes_StartingNodeLikeParam_SP" stored procedure. Input the table name or partial table name as the parameter. 
    ```
    # For For A Specific Node of Interest
    python runDataDocVisual_Filtered.py
    ```

    ```
    # For All Nodes Of Interest
    python runDataDocVisual.py
    ```


<!-- CONTACT -->
## Contact

[Jared Fiacco](https://www.linkedin.com/in/jaredfiacco/) - jaredfiacco2@gmail.com

Project Link: [https://github.com/jaredfiacco2/FirebasePodcastTranscription](https://github.com/jaredfiacco2/FirebasePodcastTranscription)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jaredfiacco/
[features-oauth]: images/BugTrackerTools_Oauth.gif
[features-api]: images/BugTrackerTools_API.gif
[features-clickup]: images/BugTrackerTools_V05.gif
[features-dashboard]: images/BugTrackerTools_Dashboard_V01.gif
[features-workqueue]: images/BugTrackerTools_Workqueue.gif