# Vendor-Management-System

This is a Vendor Management System developed using Django and Django REST Framework. This system handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/navansh03/Vendor-Management-System.git
   ```
   Locating to the Project Directory:
   ```bash
   cd Vendor-Management-System
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:

   - On Windows, run:
     ```bash
     .\env\Scripts\activate
     ```
   - On Unix or MacOS, run:
     ```bash
     source env/bin/activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Build the Docker image:

   ```bash
   docker build -t vendor-management-system-django-1 .
   ```

6. Run the Docker container:
   ```bash
   docker run -p 8000:8000 vendor-management-system-django-1:latest
   ```

The application should now be running at `http://localhost:8000`.

## Creating a User

To create a user, you can use the Django admin interface. First, run the following command to create a superuser:

```bash
cd ManagementSystem
python manage.py createsuperuser
```

## API Documentation

### Token Generation

To generate a token, send a POST request to `http://localhost:8000/api/token/` with your username and password in the body. Here's an example using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"yourusername","password":"yourpassword"}' http://localhost:8000/api/token/
```
##### Please replace yourusername and yourpassword with your actual username and password which you have created.

You can then use this token in your API requests by including it in the `Authorization` header, prefixed with `Token `:

```bash
curl -X GET -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" http://localhost:8000/api/vendors/
```

### API Endpoints
All API endpoints are documented in Swagger. After running the application, you can access the Swagger UI at `http://localhost:8000/swagger`.

The Swagger UI provides a comprehensive list of all API endpoints, along with descriptions and examples for each one. You can also try out the API directly from the Swagger UI.

## Running Tests

Then, to run the test suite, execute the following command:

```bash

python manage.py test
```
This will run all the tests in your Django project and display the results in the terminal

## Contact

If you have any questions or issues, feel free to contact the developer. You can reach me at:

- Email: navanshgoswami4@gmail.com
- GitHub: [@navansh03](https://github.com/navansh03)
