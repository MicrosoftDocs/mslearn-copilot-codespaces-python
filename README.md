[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/MicrosoftDocs/mslearn-copilot-codespaces-python)

# Use GitHub Copilot to write Python

Explore how you can modify a Python repository using code suggestions from GitHub Copilot to create an interactive HTML form and an Application Programming Interface (API) endpoint. By working with this repository, you'll quickly get hands-on with a Python web app that serves an HTTP API that generates a pseudo-random token, commonly used in for identification.

## Requirements

1. Enable your [GitHub Copilot service](https://github.com/github-copilot/signup)
1. Open [this repository with Codespaces](https://codespaces.new/MicrosoftDocs/mslearn-copilot-codespaces-python)

## 💪🏽 Exercise

The API already has a single endpoint to generate a token. Let's update the API by adding a new endpoint that accepts text and returns a list of tokens.

### 🛠 Step 1: Add a Pydantic model

Go to the `main.py` file, and add a comment so that GitHub Copilot can generate a `Pydantic` model for you. The generated model should look like this:

```python
class Text(BaseModel): 

text: str
```

### 🔎 Step 2: Generate a new endpoint

Next, generate a new endpoint with GitHub Copilot by adding the comment: 

```python
# Create a FastAPI endpoint that accepts a POST request with a JSON body containing a single field called "text" and returns a checksum of the text 
```

### 🐍 Step 3: Add necessary imports

The generated code causes the application to crash. The crash happens because the `base64` and `os` modules aren't imported. Add the following lines to the top of the file:

```python
import base64 
import os
```

Finally, verify the new endpoint is working by trying it out by going to the `/docs` endpoint and confirming that the endpoint shows up.


🚀 Congratulations, through the exercise, you haven't only used copilot to generate code but also done it in an interactive and fun way! You can use GitHub Copilot to not only generate code, but write documentation, test your applications and more.


## Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.
