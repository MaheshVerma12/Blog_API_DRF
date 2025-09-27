A Django REST Framework project in which full CRUD functionalities of DRF is implemented in the form of a Blog app's API. It has given functionalities ->
(1) New user can register an account 
(2) Existing users can login 
(3) Secure user registration and login using JSON web tokens
(4) Logged in users can create a blog post in their account space, can view their posts, can update their own posts and can delete their own posts
(5) Not logged in users can only view random blog posts stored in the database.

## API Endpoints

Here are some of the primary API endpoints:

*   **Authentication:**
    *   `POST /api/account/register/`: Register a new user.
    *   `POST /api/account/login/`: Log in and receive a JWT token.
    *   `POST /api/account/token/refresh/`: Refresh an expired access token.

*   **Blog Posts:**
    *   `GET /api/home/blogs/`: Get a list of all blog posts.
    *   `POST /api/home/blogs/`: Create a new blog post.
    *   `GET /api/home/blogs/<id>/`: Retrieve a specific blog post.
    *   `PUT /api/home/blogs/<id>/`: Update a specific blog post.
    *   `DELETE /api/home/blogs/<id>/`: Delete a specific blog post.
