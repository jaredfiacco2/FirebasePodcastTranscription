
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
    <li><a href="#prerequisites">Prerequisites/Instructions</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

- My favorite podcast is more than 100 episodes and counting, all ~1hr each. After binging it in a month, I found myself wanting to search for episodes to rewatch or solidify interesting facts. This project enables cheap storage in the cloud, transcript searchability, and statistical research and NLP projects in the future.

- I take an RSS XML feed, loop through podcasts mp3 links, transcribing them, and storing the results locally as .pkl files and in the cloud in a firebase.  

<img src="images\ProcessMap.png" alt="Process Map"/>

### Built With

* [Python](https://python.org)
* [Pandas](https://pandas.pydata.org/)
* [Firebase](https://firebase.google.com/docs/firestore)
* [RSS and XML](https://en.wikipedia.org/wiki/RSS)
* [JSON](https://en.wikipedia.org/wiki/JSON)
* [Pkl Files](https://docs.python.org/3/library/pickle.html)

### Prerequisites

1. Installing all Required Packages
  ```sh
  pip install -r requirements.txt
  ```

2. Open a Google Cloud Platform Account and a firebase account. 

3. Download a [admin sdk json file](https://firebase.google.com/docs/admin/setup#python) to access firebase. Download the file and replace the firebase-adminsdk.json file in your repo. Adjust "cred" variable in loadToFirebase_gitVersion.py file to match the name of your credentials file.
<img src="images\firebase_key.gif" alt="getFirebaseKey" />

4. Check access to [RSS Feed](https://darknetdiaries.com/feedfree.xml).
<img src="images\xml.gif" alt="xml" />

5. Run loadToFirebase.py in python. This step took my computer well over 24 hours for the 100+ hours in the DarkNet Diaries Podcast.
  ```sh
  python loadToFirebase_gitVersion.py
  ```
6. Check Firebase to make sure the data went through.
<img src="images\firebase.gif" alt="firebase" />

7. Use Jupyter Notebook and pandas to play wit the pickle data!
<img src="images\pandas.gif" alt="pandas" />

<!-- CONTACT -->
## Contact

[Jared Fiacco](https://www.linkedin.com/in/jaredfiacco/) - jaredfiacco2@gmail.com

Another GCP Project of Mine: [Publish Computer Statistics to Pub/Sub, Use Cloud Functions to Store in BigQuery](https://github.com/jaredfiacco2/ComputerMonitoring_IOT)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jaredfiacco/