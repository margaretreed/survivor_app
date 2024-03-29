# Survivor Stats

![alt text](/static/images/readme/homepage.png)

Survivor Stats is your go to resource for analysis on voting patterns and alliances in the game of Survivor! Explore seasons and episodes with the aid of data visualization features for identifying who voted *for* whom and who voted *with* whom. For every episode across all 41 seasons of survivor, users can view an interactive arc diagram to highlight the connection between a castaway and who they voted for. Users can also visualize strongest alliances throughout a season with the heat map feature to track how often two castaways vote together. 

## Table of Contents
 - [Tech Stack](#techstack)
 - [Features](#features)
 - [Version 2.0](#version2)
 - [About the Developer](#about)

## Tech Stack <a name="techstack"></a>
**Backend:** Python3, Pandas, Flask, SQLAlchemy, Jinja<br>
**Database:** PostgreSQL<br>
**Frontend:** HTML5, CSS3, Javascript, D3.js, jQuery<br>

## Features <a name="features"></a>

### Season Overview
Users can see the basic info on each season of Survivor, along with cast photos, and an option to reveal the winner.

<img src="/static/images/readme/season-overview1.gif" width="350" />

### Watch Guide
Users can view a season and see if any castaways in that season appear in previous seasons. Torch icons indicate the total number of seasons a castaway has appeared in across all 41 seasons.

<img src="/static/images/readme/watch-rec1.gif" width="350" />

### Episode Analysis
Users can analyze each episode of survivor with the aid of an arc diagram to reveal how each castaway voted that episode. Users can also analyze strongest alliances up to the selected episode by viewing the heat map that indicates how often two survivors voted together.

<p float="left">
  <img src="/static/images/readme/arc-diagram1.gif" width="350" />
  <img src="/static/images/readme/heat-map1.gif" width="350" /> 
</p>

In addition, greyed out cast images reveal the eliminated castaways for the selected episode.

<img src="/static/images/readme/eliminated-cast1.png" width="350" />

## Version 2.0 <a name="version2"></a>
- Build out watch recommendation feature with user inputs to recommend which seasons to watch and in what order
- Visualize data for castaways that appear in multiple seasons, and which seasons have the most returning castaways
- Add map feature for each season, and to display all season locations
- Add weather feature to highlight seasons and episodes with extreme weather conditions

## About the Developer <a name="about"></a>
Meg Reed is a software engineer in Berkeley, CA.
