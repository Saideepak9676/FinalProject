# User Management System with Analytics 🚀

## 🌟 Epic Project Overview
A sophisticated user management system built with FastAPI and SQLAlchemy, featuring advanced analytics, comprehensive testing, and seamless CI/CD integration. This project represents the culmination of software engineering best practices and modern development techniques.

## 🎯 Core Features

### 1. User Analytics System 📊
- **Event Tracking**
  - Comprehensive user activity monitoring
  - Session-based analytics
  - Role transition tracking
  - Custom event metadata support

- **Conversion Analytics**
  - Anonymous to authenticated user conversion tracking
  - Detailed conversion rate calculations
  - Time-based analytics reporting
  - Session-based user journey analysis

- **User Activity Monitoring**
  - Inactive user detection
  - User engagement metrics
  - Role-based activity analysis
  - Historical activity tracking

### 2. Advanced User Management 👥
- **Role Management**
  - Automatic admin role assignment for first user
  - Role-based access control (RBAC)
  - Dynamic role transitions
  - Role hierarchy enforcement

- **Security Features**
  - Enhanced password validation
  - Bcrypt password hashing
  - Failed login attempt tracking
  - Account locking mechanism

- **User Identity**
  - Unique username enforcement
  - Email validation and verification
  - URL-safe username generation
  - Profile customization options

## 🧪 Test Suite

### Analytics Service Tests
1. `test_track_event`
   - Validates event creation
   - Verifies data persistence
   - Checks event attributes
   - Tests error handling

2. `test_get_inactive_users`
   - Identifies inactive accounts
   - Validates time thresholds
   - Tests user status updates
   - Verifies query accuracy

3. `test_conversion_rate`
   - Tracks anonymous visits
   - Monitors user conversions
   - Validates rate calculations
   - Tests date range filtering

### User Management Tests
4. `test_user_base_url_invalid`
   - URL format validation
   - Invalid URL detection
   - Error message verification
   - Edge case handling

5. `test_valid_profile_urls`
   - Social media link validation
   - URL format checking
   - Protocol verification
   - Domain validation

6. `test_invalid_profile_urls`
   - Malformed URL detection
   - Invalid protocol handling
   - Domain validation
   - Error response testing

7. `test_hash_password`
   - Password hashing verification
   - Salt generation
   - Hash uniqueness
   - Performance testing

8. `test_verify_password_correct`
   - Password verification
   - Hash comparison
   - Invalid input handling
   - Error scenarios

9. `test_verify_password_timing`
   - Timing attack prevention
   - Constant-time comparison
   - Security validation
   - Performance metrics

10. `test_account_lock_after_failed_logins`
    - Login attempt tracking
    - Account locking logic
    - Unlock mechanisms
    - Security compliance

## 🛠️ Quality Assurance and reolved issues

### 1. [Docker Compose Build Error](https://github.com/Saideepak9676/FinalProject/issues/1)
- Fixed package version constraints
- Optimized build process
- Enhanced container efficiency
- Improved build reliability

### 2. [CI/CD Integration](https://github.com/Saideepak9676/FinalProject/issues/3)
- DockerHub integration
- Multi-platform build support
- Automated testing pipeline
- Security scanning implementation

### 3. [Username Management](https://github.com/Saideepak9676/FinalProject/issues/5)
- Unique username generation
- URL-safety validation
- Privacy enhancement
- User experience improvement

### 4. [Password Validation](https://github.com/Saideepak9676/FinalProject/issues/6)
- Complex password requirements
- Secure hashing implementation
- Validation feedback
- Security enhancement

### 5. [User Uniqueness](https://github.com/Saideepak9676/FinalProject/issues/8)
- Email uniqueness validation
- Nickname uniqueness checks
- Duplicate prevention
- Data integrity assurance

## 🚀 Deployment

### Docker Integration
Build the image: docker-compose build
Run the container: docker-compose up -d
docker-compose exec fastapi pytest


### DockerHub Repository
- Repository: [saideepak9676/finalproject](https://hub.docker.com/r/saideepak9676/finalproject)
- Latest build status: [![Build Status](badge_url)](build_status_url)
- Security scan: [![Security Status](security_badge_url)](security_status_url)

## 💻 Development Process

### Version Control
- Git workflow implementation
- Feature branch strategy
- Pull request reviews
- Continuous integration

### Issue Tracking
- Detailed issue documentation
- Progress monitoring
- Priority management
- Resolution tracking

### Code Quality
- Automated testing
- Code coverage monitoring
- Style guide enforcement
- Performance optimization

## 📚 Documentation

### API Documentation
- Swagger UI integration
- Endpoint documentation
- Request/response examples
- Authentication details

## 📞 Contact
- Project Link: [https://github.com/Saideepak9676/FinalProject](https://github.com/Saideepak9676/FinalProject)
- DockerHub: [saideepak9676/finalproject](https://hub.docker.com/r/saideepak9676/finalproject)
