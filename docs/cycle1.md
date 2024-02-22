## Backend architecture


- **Overview**

    The backend architecture of the pharmacy website is designed to provide a robust and scalable platform for managing pharmaceutical data and serving endpoints to support the frontend application and mobile application. Built on Django Rest Framework (DRF), the architecture follows best practices to ensure security, performance, and maintainability.


- **Components**

	- **1. Django Framework**


        Django provides the foundation for the backend application, offering a high-level Python web framework for rapid development and clean, pragmatic design. It handles routing, request handling, authentication, and database interactions.

    - **2. Django Rest Framework (DRF)**

        DRF extends Django's capabilities to support building Web APIs. It provides serializers, views, and generic API views to streamline the creation of RESTful endpoints. DRF also offers authentication, permissions, and throttling mechanisms out of the box.

    - **3. Database Layer**

        The backend relies on a relational database management system (RDBMS) to store and retrieve pharmaceutical data. Common choices include PostgreSQL, MySQL, or SQLite
        we use SQLite for development and PostgreSQL for production.

    - **4. Models**

        Django's ORM (Object-Relational Mapping) is used to define models representing pharmaceutical entities such as drugs, prescriptions, users, and orders. These models map to database tables, allowing for easy manipulation and querying of data.

    - **5. Views**

        DRF views handle incoming HTTP requests and generate appropriate responses. Views are responsible for processing data, validating inputs, and interacting with the database through Django models. Views may be class-based or function-based, depending on the complexity of the logic.

    - **6. Serializers**

        Serializers in DRF convert complex data types such as Django models into native Python data types suitable for rendering into JSON or other content types. They facilitate data validation, parsing incoming request data, and formatting outgoing response data.

    - **7. Middleware**

        Middleware components in Django intercept HTTP requests and responses, allowing for cross-cutting concerns such as logging, security, or custom preprocessing logic. Middleware can be used to enforce CORS policies, handle exceptions, or modify request/response headers.

    - **8. Testing**

        Unit tests, integration tests, and end-to-end tests ensure the reliability and correctness of the backend application. Django provides robust testing frameworks, and tools like pytest can be used for comprehensive test coverage.

    - **9. Deployment and Scalability**

        The backend application can be deployed on cloud platforms like AWS, Azure, or Google Cloud Platform for scalability and high availability. Containerization with Docker and orchestration with Kubernetes simplify deployment and management of the application across different environments.
        we used PythonAnywhere because it free




## Authentication

- backend

    DRF provides built-in support for various authentication mechanisms, including token-based authentication, session authentication, OAuth, etc. Authentication ensures that only authorized users can access protected endpoints. Authorization mechanisms control what actions users can perform based on their roles and permissions.

    list of used library.
 - 1- **Django Allauth**

	- **Purpose**: Django Allauth is a flexible authentication solution for Django applications, offering support for social account authentication like Goggle and Facebook, email verification, and account management.

- 2. **Dj-Rest-Auth**

	- **Purpose**: Dj-Rest-Auth extends Django Allauth's functionality to provide RESTful endpoints for user authentication and registration.

- 3. **Simple JWT (JSON Web Tokens)**

	- **Purpose**: Simple JWT is a lightweight library for creating and validating JSON Web Tokens (JWT) to implement token-based authentication in DRF and provide access and refresh tokens and can set period for them





## Profile page and settings


- **backend**
    - **Overview**

        User profiles play a crucial role in providing a personalized experience for users within our application. They allow users to manage their information, preferences, and settings. Here's how you can document user profile management in our application Profile includes personal details, contact information, preferences, and any other relevant data that enhances the user experience.

    - **Components**
        - **1. Profile Model**

            The profile model stores additional user information. This model typically extends Django's built-in **`User`** model or links to it using a one-to-one relationship.

            Example:

            ```python

            from django.contrib.auth.models import User
            class Profile(models.Model):
                user = models.OneToOneField(User, on_delete=models.CASCADE)
                image= models.ImageField(upload_to='avatars/', blank=True)
                # more fields

            ```

            ### **2. Profile Serializers**

            Forms or serializers are used to validate and process profile data when users update their profiles through forms or API endpoints.

            ### **3. Profile Views or Endpoints**

            Views or endpoints handle profile-related requests, such as displaying profile information, updating profiles, or deleting profiles.

    - **Functionality**

        ### **1. Profile Creation**

        Profiles automatically created upon user registration

        ### **2. Profile Update**

        Users should have the ability to update their profile information

        ### **3. Profile Retrieval**

        Users should be able to view their own profiles

        ### **4. Profile Picture Management**

        Users should be able to upload, update, or remove profile pictures

        ### **5. Profile Privacy Settings**

        Users should have control over the visibility of their profile information. They may choose to make their profiles public, private, or visible to specific users or groups.

        ### **6. Profile Deletion**

        Users is able to delete their profiles.

        ## **Security Considerations**

        ### **Access Control**

        Access to profile information is restricted based on user permissions.
