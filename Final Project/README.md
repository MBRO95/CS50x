# **Flomentum: Personalized Daily Schedule and Insights**

Flomentum is a Flask-based web application that generates personalized daily schedules and provides insights to optimize productivity, rest, and well-being. The app leverages user inputs to align activities with circadian rhythms and includes customizable features like a light/dark mode toggle and dynamic schedule visualization.

[Video Demo](https://youtu.be/COR9QSgyuuE?si=mIWGuvT6b3WZt8Yx)

---

## **Features**
- **Personalized Schedules**: Create tailored schedules based on user inputs (e.g., wake time, bedtime, and sleep duration).
- **Dynamic Insights**: Showcase unique user insights to optimize their day.
- **Responsive Design**: Designed with Bootstrap for seamless usability across devices.
- **Interactive Visuals**: Smooth scrolling, hover effects, and clickable timeline features.

---

## **Project Structure**

### **1. Application Files**
#### `app.py`
- **Purpose**: Core Flask application file that manages routing, user input validation, and dynamic content generation.
- **Key Features**:
  - Routes for `home`, `dashboard`, `schedule`, and `insights`.
  - User session management to personalize content.
  - Data-driven insights using mock user data (`users.json`).

#### `scheduler.py`
- **Purpose**: Contains the logic for generating personalized schedules based on user inputs.
- **Key Features**:
  - Sequential schedule calculation to avoid overlaps.
  - Dynamic adjustment of windows like **Non-Sleep Deep Rest** and **Evening Wind-Down**.
  - Research-backed default durations for each activity.

---

### **2. Templates**
#### `layout.html`
- **Purpose**: Master template for consistent design across pages.
- **Features**:
  - Responsive navbar with dynamic active page highlighting.
  - Light/dark mode toggle for user accessibility.

#### `home.html`
- **Purpose**: Welcoming page showcasing the app’s features and purpose.
- **Features**:
  - Call-to-action buttons for navigating to other parts of the app.
  - Highlighted app features using Bootstrap cards.

#### `dashboard.html`
- **Purpose**: Collects user inputs to create personalized schedules.
- **Features**:
  - Form fields for wake time, bedtime, sleep duration, and optional intimacy inclusion.
  - Real-time and server-side validation for user inputs.

#### `schedule.html`
- **Purpose**: Displays the generated schedule.
- **Features**:
  - Timeline visualization of schedule windows.
  - Detailed descriptions for each window with suggested activities.

#### `insights.html`
- **Purpose**: Placeholder page for personalized insights based on user data.
- **Features**:
  - Card-based layout showcasing unique user insights.
  - Smooth scrolling to detailed sections for enhanced interactivity.

---

### **3. Data Files**
#### `users.json`
- **Purpose**: Mock user database storing sample data like sleep consistency and productivity windows.
- **Design Choice**:
  - Using a JSON file instead of a database for simplicity and portability.

---

### **4. Static Files**
#### `validation.js`
- **Purpose**: Implements client-side validation for forms.
- **Features**:
  - Dynamic field validation for wake and bedtime logic.
  - Smooth feedback for user inputs.

#### `style.css`
- **Purpose**: Custom styles to enhance the Bootstrap theme.
- **Features**:
  - Hover effects for buttons.
  - Card shadowing and transitions for visual polish.

---

## **Design Choices**
1. **Dynamic Scheduling Logic**:
   - Ensured sequential window calculation to avoid overlaps.
   - Allowed for flexible adjustments to windows like **NSDR** and **Evening Wind-Down**.

2. **User-Centric Design**:
   - Prioritized ease of use with a Bootstrap-based responsive layout.
   - Added interactive features like smooth scrolling and active page highlights.

3. **Maintainability**:
   - Modularized functionality into separate files (`scheduler.py`, `validation.js`).
   - Used `users.json` for easy prototyping without setting up a database.

4. **Future-Proofing**:
   - Placeholder for advanced insights to demonstrate potential functionality.
   - Designed with scalability in mind, e.g., integrating real user data.

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/flomentum.git
   cd flomentum
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python app.py
    ```
4. Open the app in your browser:
    ```
    http://127.0.0.1:5000/
    ```

---

### **Future Enhancements**
- **Database Integration**: Replace `users.json` with a database for robust user management.
- **AI-Driven Insights**: Incorporate machine learning for predictive recommendations.
- **Native Mobile App**: Transition to a Swift-based iOS application to improve accessibility and user experience.

---

### **Acknowledgments**
This project was inspired by:
- Andrew Huberman’s research on circadian rhythms and behavioral design principles. [Huberman Lab](https://www.hubermanlab.com/)
- The broader principles of behavioral design and habit formation, applied to optimize daily schedules.

This project utilizes and builds upon work from:
- CS50x by way of some foundational code, best practices, and utilities to get a Flask-based web app up and running. [CS50x](https://cs50.harvard.edu/x/2025/)
- The Bootstrap Team by way of the 5.3.3 CDN-hosted JavaScript and CSS files. [Bootstrap](https://getbootstrap.com/)
- The Bootswatch Team by way of the 5.3.3 CDN-hosted Bootsrap theme - Morph. [Bootswatch | Morph](https://bootswatch.com/morph/)
