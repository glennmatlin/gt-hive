---
created: 2026-02-26T19:44:44 (UTC -08:00)
tags: []
author:
---

# PACE - External - Open OnDemand Guide

---
## Open OnDemand Instances for PACE's Clusters

| Cluster | Link |
| --- | --- |
| Phoenix | [Phoenix OnDemand](https://ondemand-phoenix.pace.gatech.edu/) |
| ICE | [ICE OnDemand](https://ondemand-ice.pace.gatech.edu/) |

> **Warning:** OnDemand does not have IE11 support and does not work well with Safari. Use Chrome, Firefox, or Edge for best performance.

## Introduction

Open OnDemand was created by the Ohio Supercomputer Center and their documentation can be accessed at [OnDemand OSC](https://www.osc.edu/resources/online_portals/ondemand).

The Open OnDemand interface allows you to access PACE clusters through a web browser. You can manage files in a GUI and have access to all your directories. The interface also allows for you to submit and monitor jobs, see their output, and check the status of the job queue. In addition, you are able to run interactive applications such as Jupyter Notebook, Matlab, etc., all in the web browser instead of having to SSH into the cluster.

## Getting Started

In order to access OnDemand you must be connected to the GT VPN. If you do not already have the VPN set up, visit [Configure the GT VPN](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042139).

Once connected to the VPN you can access the interface for each cluster via the link in the chart above.

To access the cluster via a shell simply click on **Clusters -> Shell Access** in the top menu bar.

A new window will appear with a terminal. You will be prompted with a question and by answering "yes" you will be connected to the cluster. On this terminal you will be able to do all the same things as you could have done by regularly using SSH to connect to the cluster.
## Managing Files

You can access your data in your home directory on the cluster by clicking on the **Files** tab in the navigation bar and selecting `home`. `project` and `scratch` storage on Phoenix is also accessible through this dropdown in the OnDemand interface. This will open the file explorer, which allows you to create, edit, and delete files. You can also navigate to other directories on the system.
Here are a list of the available buttons and their functions:

| Button | Function |
| --- | --- |
| **Open In Terminal** | Opens the current directory in a new terminal |
| **New File** | Creates an empty file in the current directory |
| **New Directory** | Creates an empty directory |
| **Upload** | Allows for you to upload files from your local machine to the current directory |
| **Download** | Downloads the selected file to your local machine |
| **Copy/Move** | Opens a prompt allowing you to either copy or move the selected file to a new location |
| **Delete** | Deletes the selected file (with confirmation) |
| **Change Directory** | Opens a prompt to specify a new path to open |
| **Copy Path** | Copies the path of the current directory to the clipboard |
| **Show Owner/Mode** | Displays the user-owner and mode for all files/directories in the current directory |
| **Show Dotfiles** | Displays all files/directories in the current directory that begin with '.' |
| **Filter** | Displays files/directories that contain the specified string (case insensitive) |

Additionally, each object has an adjacent dropdown to rename/download/delete directories and view/edit/rename/download/delete files.

## Creating and Submitting Jobs

You can submit jobs to run interactively, including a browser-based GUI interface, or as a batch submission using a PBS script as you would from the command line.

## Interactive Apps

Interactive applications allow the users to run tasks directly on compute nodes rather than through a batch script.

### Starting an Interactive App

To start an interactive job, select the **Interactive Apps** tab from the navigation bar and select the appropriate application.

Interactive jobs will not end when you close the browser window! Please be sure to kill any active jobs when you are done working to ensure you will not be charged for extra time. This can be done by hitting the red **Delete** button for the job under the **Active Jobs** menu described in the [Monitoring Jobs](#monitoring-jobs) section.

The available interactive applications are:

#### Jupyter Notebook

The Jupyter Notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text. Uses include: data cleaning and transformation, numerical simulation, statistical modeling, data visualization, machine learning, and much more. For more details, visit [https://jupyter.org/](https://jupyter.org/).

To start an active Jupyter Notebook session, do the following:

1.  Click on **Interactive Apps -> Jupyter Notebooks** in the top menu.
2.  This will open a new screen with options that can be specified for your session. Fill in the options as needed and click the blue **Launch** button to start the session. It may take some time for the session to start as resources will have to be made available.
3.  When the session starts there will be a window with a button that says **Connect to Jupyter**. Click on this button and your Jupyter Notebook will be opened. The window will also contain information regarding your session such as when it started and how much time is remaining.
4.  There will be 3 tabs in your Jupyter Notebook: Files, Running, and Clusters.
    -   The **Files** tab will display the contents of your `home` directory.
    -   The **Running** tab contains the terminal sessions and notebooks that are running
    -   The **Clusters** tab is used for running parallel code via [ipyparallel](https://ipyparallel.readthedocs.io/en/latest/) - **CURRENTLY THIS FEATURE IS NOT SUPPORTED**
5.  To create a new notebook or terminal, click on the **New** button and choose the appropriate option. You can create your own conda environment and [have it appear in this menu](https://gatech.service-now.com/home?id=kb_article_view&sysparm_article=KB0042670#using-jupyter-with-your-own-conda-environment).
6.  To stop the Jupyter Notebook session go back to the home page on the OnDemand interface and click on **My Interactive Sessions** in the top menu. This will take you to a page with a list of all your interactive sessions. To stop any specific session click on the **Delete** button.

#### Matlab

To start an active MatLab session do the following:

1.  Click on **Interactive Apps -> MatLab** in the top menu.
2.  This will open a new screen with options that can be specified for your session. Fill in the options as needed and click the blue **Launch** button to start the session. It may take some time for the session to start as resources will have to be made available.
3.  Click on the **Launch MatLab** button and new window will appear with Matlab.
#### RStudio

To start an active RStudio session do the following:

1.  Click on **Interactive Apps -> RStudio** in the top menu.
2.  This will open a new screen with options that can be specified for your session. Fill in the options as needed and click the blue **Launch** button to start the session. It may take some time for the session to start as resources will have to be made available.
3.  Click on the **Connect to RStudio Server** button and new window will appear with RStudio.
#### Interactive Desktop

The interactive desktop spawns a virtual desktop session on a compute node, which can be helpful for running other GUI applications, such as ANSYS, COMSOL, and ParaView, which are not currently supported as stand-alone interactive applications.

When starting an interactive desktop session, you may need to wait up to 5 minutes after the Launch button appears before the desktop will load successfully. If the desktop session returns a "failed to connect to server" message, please wait a few minutes and click Connect again.

#### Interactive Shell

The interactive shell application opens a terminal within your browser, from which you can run shell commands as you would on the command line.

-   If you are asked to input a username and password when opening the interactive shell, close the tab and click Connect again. This can occur if you click Connect too quickly after the session is initiated.

### Managing Interactive Applications

You can see a list of current and recent interactive sessions by clicking the **My Interactive Sessions** tab from the navigation bar. From here, you can connect to existing applications, view their execution details, and delete them.

## Batch Job Submissions

You can submit batch job submissions using the **Job Composer** tab in the navigation bar.

## Creating a New Job

These are the steps that need to be taken to create a new job.

### Selecting a Template

Once you have navigated to the Job Composer page, click on the **New Job** button. There are three options that can be used as templates for a new job. The **From Default Template** option will create a new job with the necessary information already complete and an example script named `main_job.sh`. On the right of the screen, you will be able to see this information in the **Job Details** section.
### Editing the Job Script

Underneath **Job Details** there is a **Submit Script** section. This is where you will see the name of the script and its contents. The script can be edited by clicking on the **Open Editor** button which will open up a new window with a text editor. Once you have edited the script to your liking in the editor, click the **Save** button and the changes will be reflected in the script contents.
### Editing the Job Options

In the **Job Composer** there is a **Job Options** button. By clicking on this you will be taken to page with the job information. Fill in the necessary information. Make sure to enter your account name in the appropriate section as the job will not run unless this is filled in correctly.
## Submitting a Job

Once you have finalized the job options and script, you are ready to submit the job. Click on the job you want to submit in the table and press the green **Submit** button. A message will appear at the top of the screen letting you know that the job was submitted successfully. If there was an error, the cause will be specified in the message. The job options or script can be edited appropriately to fix the error. After the job is submitted the status will change to _Queued_ or _Running_. When the job is done, the status will be displayed as _Completed_.
## Monitoring Jobs

From the Home menu, choose **Jobs -> Active Jobs** from the top menu. This will take you to new window with all your completed and active jobs. The red **Delete** button next to a running job will end it.
