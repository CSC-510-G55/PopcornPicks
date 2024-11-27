# <i> PopcornPicks🍿: Your Destination for Movie Recommendations </i>

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/CSC-510-G55/PopcornPicks/graphs/commit-activity) [![Contributors Activity](https://img.shields.io/github/commit-activity/m/se24ncsu/PopcornPicks)](https://github.com/CSC-510-G55/PopcornPicks/pulse) [![GitHub issues](https://img.shields.io/github/issues/se24ncsu/PopcornPicks.svg)](https://github.com/CSC-510-G55/PopcornPicks/issues?q=is%3Aopen+is%3Aissue) [![GitHub issues-closed](https://img.shields.io/github/issues-closed/se24ncsu/PopcornPicks.svg)](https://github.com/CSC-510-G55/PopcornPicks/issues?q=is%3Aissue+is%3Aclosed) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/CSC-510-G55/PopcornPicks) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT) [![Unittest](https://github.com/CSC-510-G55/PopcornPicks/actions/workflows/unittest.yml/badge.svg)](https://github.com/se24ncsu/PopcornPicks/actions/workflows/unittest.yml) [![codecov](https://codecov.io/gh/CSC-510-G55/PopcornPicks/graph/badge.svg?token=7HIC094S2R)](https://codecov.io/gh/CSC-510-G55/PopcornPicks) [![GitHub release](https://img.shields.io/github/release/CSC-510-G55/PopcornPicks.svg)](https://github.com/CSC-510-G55/PopcornPicksreleases/) [![StyleCheck: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![HitCount](https://hits.dwyl.com/se24ncsu/PopcornPicks.svg)](https://hits.dwyl.com/CSC-510-G55/PopcornPicks) ![GitHub contributors](https://img.shields.io/github/contributors/CSC-510-G55/PopcornPicks) ![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/se24ncsu/PopcornPicks) ![GitHub repo size](https://img.shields.io/github/repo-size/se24ncsu/PopcornPicks) [![Black](https://github.com/CSC-510-G55/PopcornPicks/actions/workflows/black.yml/badge.svg)](https://github.com/CSC-510-G55/PopcornPicks/actions/workflows/black.yml) [![Prettier](https://github.com/CSC-510-G55/PopcornPicks/actions/workflows/prettier.yml/badge.svg)](https://github.com/CSC-510-G55/PopcornPicks/actions/workflows/prettier.yml) [![GitHub closed issues by-label](https://img.shields.io/github/issues-closed-raw/se24ncsu/PopcornPicks/bug?color=green&label=Squished%20bugs)](https://github.com/CSC-510-G55/PopcornPicks/issues?q=is%3Aissue+label%3Abug+is%3Aclosed) ![Discord](https://img.shields.io/discord/1143966088695124110) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14220693.svg)](https://doi.org/10.5281/zenodo.14220693)

<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/header_display.png" alt="drawing"/>
<b>Popcorn Picks is your ultimate movie buddy, delivering handpicked film recommendations tailored to your taste! Powered by a lightning-fast algorithm, it makes discovering new favorites and hidden gems a breeze. Dive into a world of movie magic, where you can explore personalized insights, keep track of what you love, and even share recommendations with friends via email. Whether you're a casual viewer or a true cinephile, Popcorn Picks takes your movie-watching experience to the next level—effortlessly and enjoyably!</b>

# Contents

- [Why use PopcornPicks?](#why-use-popcornpicks)
- [Project Documentation](#documentation)
- [Project Presentation Videos](#project-presentation-video)
- [Brief Overview of Project](#project-description)
- [What Docs](#what-docs)
- [How Docs](#how-docs)<br/>

  - [MongoDB](#mongodb-integration)
  - [Docker](#docker-container)
  - [Collaborative Filtering](#collaborative-filtering)
  - [Streaming Links](#streaming-links)
  - [Dashboard](#dashboard)
  - [Create an Acccount](#create-an-account)
  - [Login to Account](#login-to-account)
  - [Profile and Friends](#profile-and-friends)
  - [Wall](#wall)
  - [Recommendation Mechanism](#movie-recommendation-mechanism)<br/>
  - [Email Notifier](#email-notifier)

- [Improvements Made in the Project](#project-2-delta)
- [TechStack Used for the Development of Project](#tech-stack-used)
- [Steps for Execution](#getting-started)
- [Future Scope](#future-scope)
- [Contribute](#contribute-to-the-project)
- [Team Members](#contributors)
- [Contact](#contact)
- [License](#license)

## Why use PopcornPicks?

<img
  src="https://www.wlns.com/wp-content/uploads/sites/50/2020/01/popcorn-1085072_1920_29563194_ver1.0.jpg?strip=1"
  alt="Movie Time"
  width="30%"
  align="right"
/>

PopcornPicks: Your movie recommender! Input movies, get tailored suggestions, and share via email. Elevate your movie choices effortlessly!

- **Efficient:** Lightning-fast recommendations for movie buffs! 🚀
- **Adaptable:** Tailor the recommendations to your taste.
- **Accessible:** Works across all platforms and shells.
- **Insightful:** Get movie insights at a glance.
- **Comprehensive:** Supports a wide array of user-preferred movies.
- **Simple:** Easy installation and setup – start discovering great movies in no time!"

## Documentation

Checkout for project documentation [here](https://github.com/CSC-510-G55/PopcornPicks/tree/project3/docs)

## Project Presentation Videos

### Project Overview

[https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/animated_video.mp4
](https://github.com/user-attachments/assets/ed0c3f79-b31f-4876-ba03-b2e640cf8333)

### New Features 2 minute demo

[Demo Video](https://drive.google.com/file/d/1_Ucj2hUpYx73PhojnefEAXbMKWmEwo63/view?usp=sharing)

## Project Description

PopcornPicks is a user-friendly movie recommender that curates a tailored list of 10 movie predictions based on user-provided movie preferences. Users can input their favorite movies, and our algorithm refines recommendations based on feedback—Liked, Disliked, or Yet To Watch. Additionally, PopcornPicks offers the convenience of emailing the recommended movies, enhancing the movie-watching experience. For the system architecture and other details, please refer to our documentation [here](https://github.com/CSC-510-G55/PopcornPicks/tree/project3/docs)

## What docs

View our documentation outlining each class and function of PopcornPicks here

- [Backend](https://github.com/CSC-510-G55/PopcornPicks/blob/project3/docs/backend.md)
- [Frontend](https://github.com/CSC-510-G55/PopcornPicks/blob/project3/docs/frontend.md)
- [Testing](https://github.com/CSC-510-G55/PopcornPicks/blob/project3/docs/testing.md)

View our autogenerated doco here [Doco](https://github.com/CSC-510-G55/PopcornPicks/blob/project3/docs/generated_docs/)

## How docs

### Rating Filter

#### NEW in project 3

**The project now has a rating (PG13, R, etc) filter in the recommendation page (/search_page).**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/rating_filter.png" width="600" height="375">

### Docker Container

#### NEW in project 3

**The application is containerized using Docker, ensuring consistent deployment across all environments.**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/docker.gif" width="600" height="375">

### Sharing List of Movies

#### NEW in project 3

**Implemented /lists page where you can add multiple movies to a list, and you get a sharable permanent link for that list.**

### React Components

**Utilizes modern React components with hooks for efficient state management and reusable UI elements.**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/react.gif" width="600" height="375">

### Streaming Links

**We provide streaming links directly to the appropriate website for easier access.**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/links.gif" width="600" height="375">

### Dashboard

**Features an analytics dashboard that displays user-related data like genres.**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/dashboard.gif" width="600" height="375">

### Create an Account

**Users can now create accounts, persisting data including their movie reviews and recommendations**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/create_account.gif" width="600" height="375">

### Login to account

**The user can log in to their account securly with encrypted passwords stored in our database**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/login.gif" width="600" height="375">

### Profile and Friends

**The user can add friends, view the movies reviewed by the friends, and see their reviewed movies in their profile**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/profile.gif" width="600" height="375">

### Wall

**The user can interact with other users, by viewing a community sourced wall of recent moview reviews**
<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/wall.gif" width="600" height="375">

### Movie Recommendation Mechanism

**The user selects upto 5 movies to get a tailored watchlist and provide feedback for the same**

<img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/recommend_mechanism.gif" width="600" height="375">

### Email Notifier

**The user sends his/her movies feedback via an email (Notify Me button)**

<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/email_notifier.gif" alt="Email Notifier" width="600" height="375">
    <img src="https://github.com/CSC-510-G55/PopcornPicks/blob/project3/asset/email.png" alt="Email" width="400" height="400">
</div>


## Tech stack Used👨‍💻:

<p>
<img src="https://i.giphy.com/media/LMt9638dO8dftAjtco/200.webp" width="150">
<img src="https://i.giphy.com/media/KzJkzjggfGN5Py6nkT/200.webp" width="150">
<img src="https://i.giphy.com/media/IdyAQJVN2kVPNUrojM/200.webp" width="150">
<img src="https://media.giphy.com/media/UWt0rhp21JgLwoeFQP/giphy.gif" width ="150"/>
<img src="https://media.giphy.com/media/kH6CqYiquZawmU1HI6/giphy.gif" width ="150"/>
<img src="https://media.giphy.com/media/tAjb5pyCEBhEb8jWxC/giphy.gif" width="150"/> <!-- MongoDB -->
<img src="https://media.giphy.com/media/eNAsjO55tPbgaor7ma/giphy.gif" width="150"/> <!-- React -->
<img src="https://images.ctfassets.net/o7xu9whrs0u9/4sYuVlC3grWV9xqiALyYr2/a52875856c016db3eb86c1d8adced886/Docker.logo2_.png" width="150"/> <!-- Docker -->
<img src="https://images.javatpoint.com/tutorial/flask/images/flask-tutorial.png" width="150"/> <!-- Flask -->
<img src="https://media.giphy.com/media/Sr8xDpMwVKOHUWDVRD/giphy.gif" width="150"/> <!-- Bootstrap -->
<img src="https://media.giphy.com/media/ln7z2eWriiQAllfVcn/giphy.gif" width="150"/> <!-- JavaScript -->
<img src="https://media.giphy.com/media/fsEaZldNC8A1PJ3mwp/giphy.gif" width="150"/> <!-- CSS3 -->
<img src="https://media.giphy.com/media/XAxylRMCdpbEWUAvr8/giphy.gif" width="150"/> <!-- HTML5 -->
</p>

## Getting Started

Step 1:
Git Clone the Repository

    git clone https://github.com/CSC-510-G55/PopcornPicks.git

(OR) Download the .zip file on your local machine from the following link

    https://github.com/CSC-510-G55/PopcornPicks

Step 2:
Follow the setup instructions in the installation documentation

    https://github.com/CSC-510-G55/PopcornPicks/blob/project3/docs/install.md

OR

Step 1:
Use docker image present at [Docker Image](https://drive.google.com/file/d/14ofAh84cE1sCS8k8yHVbWzRlIa1KDRhb/view?usp=share_link) and use

docker save -o popcorn.tar popcorn

docker load -i popcorn.tar

docker run -d -p 3000:3000 -p 5001:5001 popcorn

<b>Finally, start enjoying personalized movie recommendations!</b>

## Future Scope

PopcornPicks is a dynamic project with endless possibilities for expansion and enhancement. Here are some exciting avenues for future development:

1. **Create and Manage Watchlists**: Allow users to create and manage their personal watchlist of movies they want to watch later.

2. **Shared Watchlists**: Let users create shared watchlists with friends or public lists, where multiple users can add movies to the same list.

3. **Watch History**: Keep track of movies users have watched and suggest movies based on watch history.

4. **Movie Discussions and Forums**: Create a space where users can discuss movies they’ve watched, ask for recommendations, or debate opinions.
The future of PopcornPicks is full of potential, and we invite developers, movie lovers, and anyone passionate about cinema to join us in making this platform the ultimate movie companion.

## Contribute to the Project!

Please refer to the [CONTRIBUTING.md](https://github.com/CSC-510-G55/PopcornPicks/blob/project3/CONTRIBUTING.md) if you want to contribute to the PopcornPicks source code. Follow all the guidelines mentioned in the same and raise a pull request, we would love to look at it ❤️❤️!

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/balaji305"><img src="https://avatars.githubusercontent.com/u/98479241?v=4" width="75px;" alt=""/><br /><sub><b>Balaji Sankar</b></sub></a></td>
    <td align="center"><a href="https://github.com/Bhushan0504"><img src="https://avatars.githubusercontent.com/u/79035033?v=4" width="75px;" alt=""/><br /><sub><b>Bhushan Patil</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/siriscmv"><img src="https://avatars.githubusercontent.com/u/40269790?v=4" width="75px;" alt=""/><br /><sub><b>Cyril Melvin Vincent</b></sub></a><br /></td>
  </tr>
</table>

## Contact

In case of any issues, please e-mail your queries to popcornpicksse24@gmail.com or raise an issue on this repository.<br>
Our team of developers monitors this e-mail address and would be happy to answer any and all questions you have about setup or use of this project!

## Join the PopcornPicks Community:

Contribute to the project and help us improve recommendations.
Share your experience and film discoveries with us.
Together, let's make PopcornPicks the ultimate movie companion!
PopcornPicks is more than just code; it's a passion for cinema, and we invite you to be a part of this exciting journey. Start exploring, sharing, and discovering movies like never before with PopcornPicks!
Let's make movie nights extraordinary together!

## License

This project is under the MIT License.
