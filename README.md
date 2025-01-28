# Walmart 2013 Sales Forecast Visualization

This project visualizes sales forecast data using the Prophet model and generates a graphical representation of sales predictions. The forecast data is plotted using `Matplotlib`, and the generated plot can be saved as an image for further analysis.

## Features

- Sales prediction using the Prophet model.
- Forecasting for the next 365 days.
- Graphical representation of the forecast using `Matplotlib`.
- Specific forecast analysis for selected dates.

## Requirements

- Docker (for containerized setup)
- Docker Compose (for managing multi-container applications)
- Python 3.10 (for building the Docker image)

## Installation

To run this project with Docker, follow the steps below:

### 1. Clone the repository

Clone this repository to your local machine.
  
```bash
git clone https://github.com/Sreehari05055/SalesVisualization.git
cd SalesVisualization

### 2. Build and Run the Docker Containers

1. **Build the Docker containers**:

   In the root directory of the project, run the following command to build the Docker images for both the app and MongoDB services:
   
   ```bash
   docker-compose build
