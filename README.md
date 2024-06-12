# Restaurant App - Django

## Overview

This Django-based project is designed as a comprehensive solution for managing a single-vendor e-commerce platform, specifically tailored for restaurants. It encompasses a wide range of functionalities like user authentication, menu management, cart management, order placement, email verification, and payment processing. The application aims to provide a seamless experience for both the restaurant in managing their offerings and for customers in browsing, ordering, and enjoying food items.

## Key Features

### User Authentication

- **User Registration:** Allows new users to create an account.
- **User Login:** Enables existing users to log in.
- **User Logout:** Permits users to securely log out.
- **Email Verification:** Ensures user email authenticity for account security.
- **JWT & Cookies:** Utilizes JWT for authentication and cookies to store JWT tokens securely.

### Menu Management

- **View Menus:** Users can browse through the list of all available menu items.
- **Add Menu Items:** Admins can add new items to the menu.
- **Update Menu Items:** Existing menu items can be modified.
- **Delete Menu Items:** Allows for the removal of menu items from the list.

### E-commerce Functionalities

- **Cart Management:** Users can add items to their cart, view cart contents, and remove items.
- **Order Placement:** Facilitates the process of placing orders for items in the cart.
- **Payment Processing:** Integrated with Stripe for secure and efficient payment processing.
- **Order History:** Users can view their past orders and their statuses.

### Additional Features

- **Email Notifications:** Automated emails for account creation, password resets.

## Technologies Used

- **Django:** The core framework used for building the application.
- **MySQL:** Database for storing user and application data.
- **Stripe:** For handling secure payment transactions.
- **SMTP Server:** For handling email sending functionalities.

## API Documentation

For a detailed overview of available APIs and schema, visit the [API Documentation](https://sohanyf.pythonanywhere.com/api/schema/swagger-ui/).

## Getting Started

To get a local copy up and running follow these simple steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your database, Stripe, and email backend configurations in `settings.py`.
4. Run migrations using `python manage.py migrate` to create the database schema.
5. Start the development server using `python manage.py runserver`.
6. Visit `http://127.0.0.1:8000/` in your web browser to start using the application.

## Contribution

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

For any questions or suggestions, feel free to contact me:

Sohanur Rahman - [sohan6@duck.com](mailto:sohan6@duck.com)

Project Link: [https://github.com/tangent24-hash/restaurant-app-django](https://github.com/tangent24-hash/restaurant-app-django)
