## Introduction
This repository serves as a template for developing your own Streamlit application for internal use within Sage Bionetworks.
The template is designed to source data from the databases in Snowflake and compose a dashboard using the various tools provided by [Streamlit](https://docs.streamlit.io/)
and plotly.

Below is the directory structure for all the components within `streamlit_template`. In the following section we will break down the purpose for
each component within `streamlit_template`, and how to use these components to design your own application and deploy via an AWS EC2 instance.

```
streamlit-snowflake-template/
├── .streamlit/
│   ├── config.toml
│   └── example_secrets.toml
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── toolkit/
│   ├── __init__.py
│   ├── queries.py
│   ├── utils.py
|   └── widgets.py
├── Dockerfile
├── app.py
├── requirements.txt
└── style.css
```

## Requirements & Installation

* Python 3.9 - 3.11*
* [Snowflake account]

<sub>\*[Snowpark Python] currently only supports these Python versions</sub>

For best practice, use [miniconda], [Anaconda], or [virtualenv] to create a Python 3.9, 3.10, or 3.11 environment, then install the app dependencies.  Here is an example using miniconda:

```
# Create a new env and activate it
conda create -n streamlit-app python=3.11 -y
conda activate streamlit-app

# Install dependencies with pip
pip install -r requirements.txt
```

[Snowflake account]: https://signup.snowflake.com/
[Snowpark Python]: https://docs.snowflake.com/en/developer-guide/snowpark/python/index
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[Anaconda]: https://www.anaconda.com/
[virtualenv]: https://docs.python.org/3/tutorial/venv.html

## Create your own Streamlit application

### 1. Setup and Enable Access to Snowflake 

- Create a new repository from this template under the `Sage-Bionetworks` organization on GitHub.
- Within the `.streamlit` folder, you will need a file called `secrets.toml` which will be read by Streamlit before making communications with Snowflake.
Use the contents in `example_secrets.toml` as a syntax guide for how `secrets.toml` should be set up. See the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/admin-account-identifier#using-an-account-name-as-an-identifier) for how to find your
account name. **Note:** If you use the `Copy account identifier` button it will copy data in the format of `orgname.account_name`, update it to be `orgname-account_name`.
- Test your connection to Snowflake by running the example Streamlit app at the base of this directory. This will launch the application on port 8501, the default port for Streamlit applications.
   
  ```
  streamlit run app.py
  ```

  If you receive the following error during local deployment:

  ```
  No active warehouse selected in the current session - Select an active warehouse with the 'use warehouse' command
  ```

  you may need to designate a default warehouse for your Snowflake account. The simplest way is to log into Snowflake via your web browser, open a new SQL Worksheet, and select a warehouse. You'll then be asked if you want to set this as your default warehouse.  You can also configure your default warehouse by going to your **Profile** > **Default role & warehouse**.

  If the error continues after setting a default warehouse, check with an admin to confirm your user permissions.

> [!CAUTION]
> Do not commit your `secrets.toml` file to your forked repository. Keep your credentials secure and do not expose them to the public.


### 2. Build your Queries

Once you've completed the setup above, you can begin working on your SQL queries.
- Navigate to `queries.py` under the `toolkit/` folder.
- Your queries can either be string objects, or functions that return string objects. Assign each of them an easy-to-remember variable/function name, as they will be imported into `app.py` later on. See below for two examples on how you can write your queries depending on your needs.
- It is encouraged that you test these queries in a SQL Worksheet on Snowflake's Snowsight before running them on your application.

**Example of a string object query**: <br>
You may assign your string objects to global variables if you do not intend for the queries to be modified in any way. Below is a simple example for
a use-case where only the number of files for Project `syn53214489` is calculated.
```
QUERY_NUMBER_OF_FILES = """

select
    count(*) as number_of_files
from
    synapse_data_warehouse.synapse.node_latest
where 
    project_id = '53214489'
and
    node_type = 'file';
"""
```

**Example of a function query**:<br>
We encourage the use of function queries if you plan to make your application, and therefore your queries, interactive. For example, let's say you want to give users the option to input the `project_id` they want to query the number of files for. Your query in this case would look like the following...
```
def query_number_of_files(pid):
  """Returns the total number of files for a given project (pid)."""

  return f"""
  select
    count(*) as number_of_files
  from
      synapse_data_warehouse.synapse.node_latest
  where 
      project_id = {pid}
  and
      node_type = 'file';
  """
```

### 3. Build your Widgets

Your widgets will be the main visual component of your Streamlit application.

- Navigate to `widgets.py` under the `toolkit/` folder.
- Modify the imports as necessary. By default we are using `plotly` to design our widgets.
- Create a function for each widget. For guidance, follow one of the examples in `widgets.py`.

### 4. Build your Application

Here is where all your work on `queries.py` and `widgets.py` come together.
- Navigate to `app.py` to begin developing.
- Import the queries you developed in Step 2.
- Import the widgets you developed in Step 3.
- Begin developing! Use the pre-existing `app.py` in the template as a guide for structuring your application.

> [!TIP]
> The `utils.py` houses the functions used to connect to Snowflake and run your SQL queries. Make sure to reserve an area
> in the script for using `get_data_from_snowflake` with your queries from Step 2.
>
> Example:
>
> ```
> from toolkit.queries import (
>    query_entity_distribution,
>    query_project_downloads,
>    query_project_sizes,
>    query_unique_users,
> )
>  
>  entity_distribution_df = get_data_from_snowflake(query_entity_distribution())
>  project_sizes_df = get_data_from_snowflake(query_project_sizes())
>  project_downloads_df = get_data_from_snowflake(query_project_downloads())
>  unique_users_df = get_data_from_snowflake(query_unique_users(my_param))
> ```

### 5. Test your Application

We encourage implementing unit and regression tests in your application, particularly if there are components that involve interacting with the application
to display and/or transform data (e.g. buttons, dropdown menus, sliders, so on).

- Navigate to `tests/test_app.py` to modify the existing script.
- The default tests use [Streamlit's AppTest tool](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest#run-an-apptest-script) to launch the application and retrieve its components. Please modify these existing tests or create brand new ones
as you see fit.

> [!TIP]
> Make sure to launch the test suite from the base directory of the `streamlit_app/` (i.e `pytest tests/test_app.py`)
> to avoid import issues.

### 6. Dockerize your Application
  
- **Update the requirements file** <br>
  Ensure that the `requirements.txt` file is up to date with all the necessary Python packages that are used in your scripts.
- **Push all relevant changes** <br>
  Ensure you have pushed all your changes to your branch of the forked repository that you are working in (remember not to commit your `secrets.toml` file).

You can choose to build and push a Docker image to the GitHub Container Registry and pull it directly from the registry when ready to deploy in Step 7. Keep in mind the size of your Docker image will be right around 800Mb at _least_, due to the python libraries
required for a basic application to run, so be conscious of this when choosing to upload your image.

If you do not wish to publish a Docker image to the container registry, you can skip the to the next section. Otherwise, follow the instructions below.

- **Build the Docker image** <br>
  Run the following command in your terminal from the root of your project directory where the `Dockerfile` is located:
  ```
  docker build -t ghcr.io/<your-username>/<your-docker-image-name>:<tag> .
  ```
  Replace `<your-username>` with the user that owns the forked repository, `<your-docker-image-name>` with a name for your Docker image, and `<tag>` with a version tag (e.g., v1.0.0).

- **Login to GitHub Container Registry** <br>
  Before pushing your image, you need to authenticate with the GitHub Container Registry. Use the following command:
  ```
  echo "<your-token>" | docker login ghcr.io -u <your-github-username> --password-stdin
  ```
  Replace `<your-token>` with a GitHub token that has appropriate permissions, and `<your-github-username>` with your GitHub username.

- **Push the Docker Image** <br>
  Once authenticated, push your Docker image to the GitHub Container Registry with the following command:
  ```
  docker push ghcr.io/<your-github-username>/<your-docker-image-name>:<tag>
  ```
  Replace the placeholders with your relevant details.

For further instructions on how to deploy your Docker image to the GitHub Container Registry, [see here](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

### 7. Launch your Application on AWS EC2

- Create an EC2: Linux Docker product from the Sage Service Catalog.
- Go to _Provisioned Products_ in the menu on the left-hand-side.
- Once your EC2 product's `status` is set to `Available`, click it and navigate to the _Events_ tab.
- Click the URL next to `ConnectionURI` to launch a shell session in your instance.
- Navigate to your home directory (`cd ~`).
- Clone your repository in your desired working directory. Example:
  ```
  git clone https://github.com/<your-username>/snowflake.git
  ```
  Replace `<your-username>` with the user that the forked repository is under.
- Create your `secrets.toml` file again. By default, the instance should already have `vi` available to use as an editor.
- Build your Docker image, either from the `Dockerfile` in the repository, or by pulling down your image from the GitHub Container Registry.
- Run your Docker container from the image, and make sure to have your `secrets.toml` (in the current working directory) mounted and the 8501 port specified, like so:
  ```
  docker run \
    -p 8501:8501 \
    -v $PWD/secrets.toml:/.streamlit/secrets.toml \
    <image name>
  ```
  Before sharing the app with others, initiate the authentication process manually (since Docker containers can't automatically open a browser for the `externalbrowser` authenticator). This step will only need to happen once (unless the cache gets cleared).
  
  First, access your Streamlit app via the private IP address in order to trigger a login request. Return to your EC2 instance's shell session; you should see a message similar to this:

  ```
  Initiating login request with your identity provider. [truncated]
  Going to open: https://some-link.com to authenticate...
  We were unable to open a browser window for you, please open the url above manually then paste the URL you are redirected to into the terminal.
  ```

  Copy the provided URL into a new browser and follow the prompt.  After logging in, you may get a page that says "This site can't be reached" which is expected.  Copy the new URL from the browser (which now contains a token) and paste it into your shell session.  Return to your Streamlit app; you should now be connected to Snowflake.

## Additional Tips: Leveraging VSCode for Development
If you would like to leverage VSCode to debug and test your application, rather than working with `streamlit` and `pytest` on the command line, follow the instructions below:

There is a `.vscode/launch.json` file located at the root of the `snowflake` repository. This file is used to define configurations for debugging and testing within VSCode. The `launch.json` file in this repository contains two key configurations: one for debugging the Streamlit app and another for running tests with the pytest library. Here’s how you can set it up and use it:

### 1. Set Up VSCode on Your Machine

Make sure you have Visual Studio Code (VSCode) installed on your machine. You can download it [here](https://code.visualstudio.com/).

### 2. Create An Active Workspace on VSCode

* Open up VSCode.
* Click up _File_ > _Open Folder..._ and navigate to the root directory of the `snowflake` repository.
* Select the folder and click _Open_.

### 3. Review The `launch.json` Configurations

* Open the `launch.json` file in the VSCode editor.
* The launch.json file in this project contains two configurations: <br>

    **Debugging the Streamlit App:**<br>
        This configuration is named "debug streamlit". When you run this, it will start the Streamlit app in a debug session. This allows you to place breakpoints in your code, step through the execution, and inspect variables as the app runs. <br>
    <br>
    **Running Pytest for the Streamlit App:**<br>
        The second configuration is named "pytest for Streamlit app". This is used to run the tests in the project using the pytest framework. It’s designed to execute the test file associated with the Streamlit app and allows you to debug your tests if they fail.

### 4. Running the Configurations

* **Open the Run and Debug Sidebar**<br>
        Click on the "Run and Debug" icon in the Activity Bar on the left side of the VSCode window. It looks like a play button with a bug on it. Alternatively, you can open it by pressing `Ctrl+Shift+D` (Windows/Linux) or `Cmd+Shift+D` (Mac).
* **Select a Configuration**<br>
        At the top of the "Run and Debug" sidebar, you’ll see a dropdown menu where you can select one of the configurations defined in the launch.json file.
        Select "debug streamlit" to start debugging the Streamlit app, or "pytest for Streamlit app" to run and debug your tests.
* **Start Debugging or Testing**<br>
        Once you’ve selected the desired configuration, click the green play button (Start Debugging) at the top of the sidebar, or simply press F5.
        The debugger will start, and you can place breakpoints in your code by clicking in the left margin next to the line numbers.
        If you’re running the tests, the pytest module will execute the specified test file, and you can debug any test failures using the same tools.
