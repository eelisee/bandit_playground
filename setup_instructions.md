# Setup Instructions

Welcome to the Bandit Playground project! Follow these instructions to set up the project locally on your machine. This guide assumes you have basic Python experience. If any issues arise, refer to the **Troubleshooting** section at the end.

## 1. System Requirements

- **Python version**: This project works with Python 3.9 and 3.11.5 (other versions may work, but they have not been tested).
- **Operating system**: Compatible with all operating systems that support Python and Dash (Windows, macOS, Linux).

## 2. Clone the Repository

First, you need to clone the repository from GitHub to your local machine. Open your terminal (or command prompt) and run the following command:

```bash
git clone https://github.com/eelisee/bandit_playground.git
cd bandit_playground
```

## 3. Set Up a Virtual Environment

It is strongly recommended to use a virtual environment to manage the project's dependencies. You can create and activate a virtual environment by running the following commands:

__For macOS/Linux:__

```bash
python3 -m venv venv
source venv/bin/activate
```

__For Windows:__
```bash
python -m venv venv
venv\Scripts\activate
```

## 4. Install Dependencies

Once the virtual environment is activated, you need to install the required Python packages. This project uses the following libraries:

```bash
dash==2.10.0
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-bootstrap-components==1.0.3
plotly==5.11.0
pandas==1.3.5
numpy==1.21.4
psutil==5.9.1
multiprocess==0.70.12.2
selenium==4.5.0
```

Install them by running the following command:

```bash
pip install -r requirements.txt
```

This command will install all the dependencies listed in the ```requirements.txt``` file. Ensure that all packages install without errors.

## 5. Running the Dashboard

Once the installation is complete, you can start the dashboard by running the following command:

```bash
python src/dashboard.py
```

After the command runs, your default web browser should automatically open with the dashboard at this URL:

```bash
http://127.0.0.1:8050
```

If it doesn't open automatically, you can manually copy and paste this URL into your browser.

## 6. Customizing Parameters in the Dashboard

The dashboard allows you to experiment with various stochastic bandit algorithms by adjusting parameters such as the number of arms, reward probabilities, and exploration-exploitation strategies. Explore different settings to observe how each algorithm performs under varying conditions. You can adjust parameters directly in the user interface provided by the dashboard.

## 7. Adapting Algorithms and saving Results

The dashboard automatically saves the results of each algorithm run beforehand and plotted in the dashboard in the data/ folder. Each file corresponds to the selected parameters and algorithm. If you want to adapt algorithms, these results are saved after running and can later be reloaded and analyzed.

## 8. Troubleshooting

Here are some common issues you might encounter and how to resolve them:

### 8.1 Port Conflicts
If you see an error indicating that the port 8050 is already in use, this means another process is using the same port. To fix this, either stop the other process or run the dashboard on a different port. You can specify a new port as follows:

```bash
python src/dashboard.py --port 8060
```

Then, open ```http://127.0.0.1:8060``` in your browser.

### 8.2 Missing Dependencies
If you encounter errors about missing dependencies, ensure that you have installed all required packages:

Run ```pip install -r requirements.txt``` again to ensure all dependencies are installed.
If the error persists, check if you are using the correct Python version (3.9 or 3.11.5).

### 8.3 Virtual Environment Not Activated
If running python src/dashboard.py opens a different Python version or doesn’t work as expected, it might mean the virtual environment is not activated. Make sure to activate it:

__For macOS/Linux:__

```bash
source venv/bin/activate
```

__For Windows:__
```bash
venv\Scripts\activate
```
### 8.4 Issues Installing Packages
Some packages may fail to install due to system-specific issues (e.g., conflicting versions or missing system libraries). Here are some general tips:

**Upgrade pip:** Make sure you have the latest version of ```pip``` by running:

```bash
pip install --upgrade pip
```

**Check the error log:** The error message during installation usually gives clues about missing dependencies or incompatible versions.

### 8.5 Other Issues
If you encounter an issue not covered here, try the following steps:

**Google the error message:** Many installation issues have been encountered and solved by others.

**Check Python and package versions:** Ensure you are using compatible versions of Python and the packages listed in ```requirements.txt```.

## 10. Contact and Support

If you encounter any issues that you cannot resolve, feel free to reach out or post your issue in the relevant GitHub repository issue tracker. Please provide details about your system, the error message, and the steps that led to the issue.