# advertising_agent
A desktop application that generates advertisements based on user input using the Meta AI API.


Features

Generate advertisements based on user-provided prompts
Save generated advertisements to a file
User-friendly interface built with PyQt5
Asynchronous API calls for improved performance
Requirements

Python 3.x
PyQt5
meta-ai-api library
META_AI_TOKEN environment variable set with your Meta AI API key
Usage

Clone the repository and install the required libraries.
Set the META_AI_TOKEN environment variable with your Meta AI API key.
Run the application using python main.py.
Enter a prompt and filename in the GUI, then click "Generate Advertisement".
Code Structure

The code is organized into three main classes:

AdvertisingAssistantModel: Handles API calls and advertisement generation.
AdvertisingAssistantView: Defines the GUI and user interface.
AdvertisingAssistantController: Manages the interaction between the model and view.
Contributing

Contributions are welcome! Please submit a pull request with your changes and a brief description of what you've added.
