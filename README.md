# Blog Application API

This is a RESTful API for a blog application built with Django and Django REST Framework. It supports basic CRUD operations for blog posts and comments.
This Project is live on https://sdcblogproject.onrender.com/api/blogs/

## Features

- User registration and authentication using JWT tokens.
- Create, read, update, and delete blog posts.
- Add comments to blog posts.

## API Endpoints

### Authentication

- **POST /register/**
  - Register a new user.
  - **Headers:**
    ```json
    {
      "content-type" : "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password",
      "email": "your_email@example.com"
    }
    ```

- **POST /login/**
  - Obtain a Json web token by providing username and password.
  - **Headers:**
    ```json
    {
      "content-type" : "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response:**
    ```json
    {
      "access": "your_access_token",
      "refresh": "your_refresh_token",
      "author_id": "your_author_id"
    }
    ```
    
- **GET /refresh_token/<your-refresh-token>**
  - Obtain a new access token by providing the refresh token.
  
  - **Response:**
    ```json
    {
      "access": "your_access_token",
      "refresh": "your_refresh_token"
    }
    ```



### Blog Posts

- **POST /api/blogs/**
  - Create a new blog post.
  - **Headers:**
    ```json
    {
      "authorization" : "Bearer your_jwt_access_token"
    }
    ```
  - **Request Body:**
    ```json
    {
      "title": "Your Blog Title",
      "content": "Your blog content here.",
      "author": "your_author_id"
    }
    ```
  - **Files:**
    ```json
    {
      "images" : "<your-image-file>"
    }
    ```

- **GET /api/blogs/**
  - Retrieve a list of all blog posts.

- **GET /api/blogs/{blog_id}/**
  - Retrieve a specific blog post by its ID.

- **PUT /api/blogs/{blog_id}/**
  - Update an existing blog post by its ID.
  - **Request Body:**
    ```json
    {
      "title": "Updated Blog Title",
      "content": "Updated blog content.",
      "author": "your_author_id"
    }
    ```

- **DELETE /api/blogs/{blog_id}/**
  - Delete a blog post by its ID.
  - **Request Body:**
    ```json
    {
      "author": "your_author_id"
    }
    ```

### Comments

- **POST /api/blogs/{blog_id}/comments/**
  - Add a comment to a blog post.
  - **Request Body:**
    ```json
    {
      "blog" : "blog_id",
      "comment_text": "This is a comment.",
      "author" : "your_author_id"
    }
    ```

### Like

- **PUT /api/blogs/{blog_id}/like/**
  - Add a like to a blog post.
  

## Usage

1. **Set Up Environment**
   - Create a `.env` file in the project root directory with the following contents:
     ```
     DATABASE_URL=your_database_url
     SECRET_KEY=your_secret_key
     DEBUG=True
     ALLOWED_HOSTS=allowed-hosts
     SUPERUSER_SECRET_KEY = secret-key-to-create-super-user
     //Create an account on cloudinary and get this info
     CLOUDINARY_URL = your_cloudinary_url
     CLOUDINARY_CLOUD_NAME = your_cloudinary_cloud_name
     CLOUDINARY_API_KEY = your_cloudinary_api_key
     CLOUDINARY_API_SECRET = your_cloudinary_api_secret
     ```

2. **Install Dependencies**
   - Run the following command to install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Migrate Database**
   - Run the migrations to set up the database:
     ```bash
     python manage.py makemigrations
     python manage.py makemigrations blog_app
     python manage.py migrate
     ```

4. **Run the Server**
   - Start the development server:
     ```bash
     python manage.py runserver
     ```

5. **Testing the API**
   - Use a tool like [Thunder Client](https://www.thunderclient.com/) or `curl` to test the API endpoints.
