# Project Name

This is our submission of Uber Hackathon 2023.

## Table of Contents
1. [Screenshots](#screenshots)
2. [Tryout API Calls](#tryout-api-calls)
3. [Demo](#demo)
4. [Explanation](#explanation)
5. [Features & How to Use](#features)
6. [API Reference](#api-reference)
    - [Get Travel Routes](#get-all-items)
    - [Real Time Location](#get-item)
    - [](#add-function)
7. [Error Handling](#error-handling)
8. [Tech Stack](#tech-stack)
    - [Client](#client)
    - [Server](#server)
9. [Future Scope](#future-scope)
10. [Authors](#authors)


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## Tryout API Calls

Click on the links to see what our API calls look like. Some of these API calls are integrated into our front end. Some of them are API only calls that can be utilized by clients.

## Demo

Insert gif or link to demo

## Explanation

## Features

## How to Use

## API Reference

### Generate Realtime Optimal Route

```http
  GET /api/generate_route
```

| Parameter | Type    | Description                                                                                        |
|:----------|:--------|:---------------------------------------------------------------------------------------------------|
| `start`   | `tuple` | **Required**. A tuple representing the starting point in the format (x, y). Must be a valid tuple. |
| `end`     | `tuple` | **Required**. A tuple representing the ending point in the format (x, y). Must be a valid tuple.   |
| `hour`    | `float` | **Required**. The hour at which the travel is happening. Must be a valid float.                    |

#### Example URL
```
http://localhost:5000/generate_route?hour=12&start=[0,0]&end=[99,99]
```

#### Outputs
- `route`: List of tuples representing the path from start to end.
- `error`: Error message in case of invalid inputs.

#### Error Handling
Returns an error message in JSON format if any of the inputs are invalid.

---

### List Travel Options

```http
  GET /api/main
```

| Parameter | Type    | Description                                                                                                 |
|:----------|:--------|:------------------------------------------------------------------------------------------------------------|
| `start`   | `tuple` | **Required**. A tuple representing the starting point in the format (x, y). Must be a valid tuple.          |
| `end`     | `tuple` | **Required**. A tuple representing the ending point in the format (x, y). Must be a valid tuple.            |
| `time`    | `tuple` | **Required**. A tuple representing the time of the day in the format (hour, minute). Must be a valid tuple. |

#### Example URL
```
http://localhost:5000/main?start=[0,0]&end=[99,99]&time=[12,30]
```

#### Outputs
- JSON object containing time, cost, environmental tax, and route for each travel option.

#### Error Handling for `/main`

The `/main` API endpoint includes the following error handling mechanisms:

- **ValueError**: If any of the inputs are in an invalid format, the API will return a JSON object with an error message.
```json
{"error": "Invalid input format. Please check your inputs."}
```

- **Other Exceptions**: For any other unexpected errors, the API will return a JSON object with a detailed error message.
```json
{"error": "An unexpected error occurred: [Error Details]"}
```


## Error Handling


## Tech Stack
<div>
    <img src="https://raw.githubusercontent.com/vigneshsaravanakumar404/skill-icons/main/icons/CS.svg" width="64" height="64" alt="Computer Science">
    <img src="https://raw.githubusercontent.com/vigneshsaravanakumar404/skill-icons/main/icons/Flask-Dark.svg" width="64" height="64" alt="Flask">
    <img src="https://raw.githubusercontent.com/vigneshsaravanakumar404/skill-icons/main/icons/Github-Dark.svg" width="64" height="64" alt="GitHub">
    <img src="https://raw.githubusercontent.com/vigneshsaravanakumar404/skill-icons/main/icons/Python-Dark.svg" width="64" height="64" alt="Python">
    <img src="https://raw.githubusercontent.com/vigneshsaravanakumar404/skill-icons/main/icons/VSCode-Dark.svg" width="64" height="64" alt="VS Code">
    <img src="https://pbs.twimg.com/profile_images/1702781641389920256/n_YDwQgP_400x400.jpg" width="64" height="64" alt="Custom">
</div>


## Future Scope
In the future, the API could be significantly enhanced by integrating real-time car location data and employing graph-based traffic modeling. By mapping each car's location onto a mathematical graph representing the city's road network, the system could dynamically update route suggestions based on current traffic conditions. This would pave the way for a centralized traffic management system capable of optimizing traffic flow across the entire city. Such a system would use machine learning algorithms to continuously analyze the graph and make real-time adjustments to signals, routes, and even coordinate autonomous vehicles. The result would be a near-elimination of traffic congestion, as all roads would be used as efficiently as possible. This centralized approach would not only reduce individual travel times but also offer broader societal benefits like reduced air pollution. As the system collects more data, its predictive algorithms would become increasingly accurate, making it even more effective over time.

## Authors
<table>
  <tr>
    <td align="center" width="50%"><a href="https://github.com/vigneshsaravanakumar404"><img src="https://github.com/vigneshsaravanakumar404.png?size=100" width="100px;" alt=""/><br /><sub><b>Vignesh Saravanakumar</b></sub></a><br /><a href="https://github.com/vigneshsaravanakumar404"><img src="https://img.shields.io/badge/GitHub-vigneshsaravanakumar404-blue?style=flat-square&logo=github" /></a></td>
    <td align="center" width="50%"><a href="https://github.com/TejasRaghuram"><img src="https://github.com/TejasRaghuram.png?size=100" width="100px;" alt=""/><br /><sub><b>Tejas Raghuram</b></sub></a><br /><a href="https://github.com/TejasRaghuram"><img src="https://img.shields.io/badge/GitHub-TejasRaghuram-blue?style=flat-square&logo=github" /></a></td>
  </tr>
</table>