# Blog Application API

This is a RESTful API for a blog application built with Django and Django REST Framework. It supports basic CRUD operations for blog posts and comments.

## Features

- User registration and authentication using JWT tokens.
- Create, read, update, and delete blog posts.
- Add comments to blog posts.

## API Endpoints

### Authentication

- **POST /register/**
  - Register a new user.
  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password",
      "email": "your_email@example.com"
    }
    ```

- **POST /api/token/**
  - Obtain a JWT token by providing username and password.
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
      "refresh": "your_refresh_token"
    }
    ```

### Blog Posts

- **POST /api/blogs/**
  - Create a new blog post.
  - **Headers:**
    ```
    {
      "content-type" : "application/json",
      "authorization" : "Bearer your_jwt_access_token"
    }
    ```
  - **Request Body:**
    ```json
    {
      "title": "Your Blog Title",
      "content": "Your blog content here.",
      "author": your_author_id
    }
    ```

- **GET /api/blogs/**
  - Retrieve a list of all blog posts.

- **GET /api/blogs/{id}/**
  - Retrieve a specific blog post by its ID.

- **PUT /api/blogs/{id}/**
  - Update an existing blog post by its ID.
  - **Request Body:**
    ```json
    {
      "title": "Updated Blog Title",
      "content": "Updated blog content.",
      "author": your_author_id
    }
    ```

- **DELETE /api/blogs/{id}/**
  - Delete a blog post by its ID.

### Comments

- **POST /api/blogs/{id}/comments/**
  - Add a comment to a blog post.
  - **Request Body:**
    ```json
    {
      "blog" : blog_id,
      "comment_text": "This is a comment.",
      "author" : your_author_id
    }
    ```

### Like

- **POST /api/blogs/{id}/like/**
  - Add a like to a blog post.
  

## Usage

1. **Set Up Environment**
   - Create a `.env` file in the project root directory with the following contents:
     ```
     DATABASE_URL=your_database_url
     SECRET_KEY=your_secret_key
     DEBUG=True
     ALLOWED_HOSTS=*
     CSRF_COOKIE_SECURE=True
     ```

2. **Install Dependencies**
   - Run the following command to install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Migrate Database**
   - Run the migrations to set up the database:
     ```bash
     python manage.py migrate
     ```

4. **Run the Server**
   - Start the development server:
     ```bash
     python manage.py runserver
     ```

5. **Testing the API**
   - Use a tool like [Thunder Client](https://www.thunderclient.com/) or `curl` to test the API endpoints.
