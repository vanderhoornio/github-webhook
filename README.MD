# Github API project
This API project is meant to receive a webhook POST request from Github for each new release in a repository. After receiving the POST request the API will send a notification to trigger a workflow. This workflow is meant to test and deploy applications/services.
https://docs.github.com/en/webhooks


#### Dependencies
- pip install flask
- pip install requests
- pip install python-dotenv
- pip install PyGithub