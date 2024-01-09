## OpenAI Chatbot

This project utilizes OpenAI APIs to create a chatbot, stores conversation history in a database, and implements authentication using Django.

### Prerequisites

- Python 3.6 or higher
- Git installed
- OpenAI API key (you can obtain it from [OpenAI](https://beta.openai.com/signup/))

### Installation

1. Clone the project from GitHub:

    ```bash
    git clone https://github.com/abhishek-rajput119/openai_chatbot.git
2. Go to the project directory:

    ```bash
    cd openai_chatbot
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv_name
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv_name\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv_name/bin/activate
        ```

5. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

6. Set up Django environment variables:

    - Open the `.env` file and add your OpenAI API key:

        ```env
        OPENAI_API_KEY=your_openai_api_key_here
        ```

7. Migrate the database:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Run the development server:

    ```bash
    python manage.py runserver
    ```

### Accessing the Application

To interact with the OpenAI Chatbot API, follow these steps:

1. Open your web browser.

2. Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).
