# Attendance Management System

A comprehensive Django-based attendance management system for educational institutions with role-based access control and real-time monitoring capabilities.

## 🎯 Features

### Core Functionality
- **Role-Based Access Control**: Separate dashboards for Students, Faculty, and Deans
- **Real-Time Attendance Tracking**: Manual and automated attendance marking
- **Attendance Analytics**: Detailed reports and statistics
- **Alert System**: Automatic notifications for low attendance
- **Bulk Import**: CSV-based user and attendance data import

### User Roles
- **Students**: View attendance percentages, receive alerts
- **Faculty**: Mark attendance, generate reports, upload CSV data
- **Deans**: Monitor institution-wide statistics, analytics
- **Admin**: Full system management via Django Admin

## 🛠️ Tech Stack

- **Backend**: Django 5.2.7
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite3 (development), PostgreSQL/MySQL (production)
- **Authentication**: Django Auth with Custom User Model
- **API**: Django REST Framework (for future mobile integration)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Attendance_System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings:
   SECRET_KEY=your-secret-key
   DEBUG=True
   MIN_ATTENDANCE_PERCENTAGE=75
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Main Site: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📊 System Architecture

### Data Models
- **User**: Custom user model with role-based authentication
- **Student/Faculty/Dean**: Role-specific profiles
- **Class**: Academic classes/sections
- **Subject**: Subjects taught in classes
- **StudentEnrollment**: Links students to classes
- **AttendanceRecord**: Daily attendance tracking
- **WhatsAppMessage**: Notification system

### Key Features Implementation
- **Attendance Validation**: Prevents editing past records
- **Unique Constraints**: Ensures data integrity
- **Model Methods**: Business logic encapsulated in models
- **Query Optimization**: Uses `select_related` and `prefetch_related`

## 🔧 Usage

### For Students
1. Login with student credentials
2. View attendance percentage on dashboard
3. Receive alerts for low attendance (<75%)

### For Faculty
1. Login with faculty credentials
2. Access faculty dashboard
3. Mark attendance manually or upload CSV
4. Generate attendance reports

### For Deans
1. Login with dean credentials
2. Access comprehensive analytics
3. Monitor class-wise attendance statistics
4. View institution-wide reports

### For Admins
1. Access Django Admin panel
2. Manage users, classes, subjects
3. Bulk import data via CSV
4. Configure system settings

## 📈 Future Enhancements

### Planned Features
- **Face Recognition**: Prevent proxy attendance using OpenCV
- **Mobile App**: Native mobile applications
- **Email/SMS Alerts**: Automated notification system
- **Advanced Analytics**: Predictive attendance modeling
- **API Layer**: RESTful API for third-party integrations
- **Multi-tenancy**: Support for multiple institutions

### Technical Improvements
- **Caching**: Implement Redis for performance
- **Background Tasks**: Celery for async operations
- **Testing**: Comprehensive unit and integration tests
- **Documentation**: API documentation with Swagger
- **CI/CD**: Automated deployment pipelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please open an issue on the GitHub repository or contact the development team.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap for the responsive UI components
- All contributors and users of this project