# Museum Ticket Booking System - Running Instructions

## Features Added

### 1. Cancel Booking Feature
- **Dashboard**: Added a "Cancel Booking" button to each booking entry on the admin dashboard
- **Confirmation**: Shows a confirmation prompt before cancelling
- **Backend**: Added cancellation logic with timestamp tracking
- **Database**: Added `cancelled` and `cancelled_at` fields to track cancellations
- **UI Updates**: Real-time UI updates when booking is cancelled

### 2. Upload Aadhar Card Feature
- **File Upload**: Added file upload field for Aadhar card (PDF/Image)
- **File Display**: Shows selected filename after upload
- **Backend**: Handles file storage in `media/aadhar_uploads/` directory
- **Validation**: Accepts only PDF and image files
- **Form Enhancement**: Updated all booking forms across different cities

### 3. Responsive UI
- **Mobile-friendly**: Clean and responsive design for all screen sizes
- **Table Responsive**: Dashboard table scrolls horizontally on mobile
- **Button Optimization**: Properly sized buttons for touch interfaces
- **Form Improvements**: Enhanced form layout for better user experience

## Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- Node.js 14+ (for React frontend)
- pip (Python package manager)

## Installation & Setup

### 1. Backend Setup (Django)

```bash
# Navigate to the project directory
cd "Ticketless-Entry-System-to-Museums-main"

# Install required Python packages
pip install django djangorestframework django-crispy-forms django-cors-headers
pip install qrcode[pil] pillow pandas razorpay xhtml2pdf django-filter pyzbar

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser
```

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd Frontend

# Install Node.js dependencies
npm install

# Build the React app
npm run build
```

## Running the Application

### 1. Start the Django Backend Server

```bash
# From the main project directory
python manage.py runserver

# Server will start at: http://127.0.0.1:8000/
```

### 2. Access the Application

- **Main Application**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/admin/
- **Booking Dashboard**: http://127.0.0.1:8000/Ticket/
- **React Frontend**: http://127.0.0.1:8000/react

## Using the New Features

### Cancel Booking Feature

1. **Access Dashboard**: Go to http://127.0.0.1:8000/Ticket/
2. **Login**: Use admin credentials (if login required)
3. **View Bookings**: See all current bookings in the table
4. **Cancel Booking**: Click "Cancel Booking" button next to any booking
5. **Confirm**: Confirm the cancellation in the popup
6. **Result**: Booking status will update to "Cancelled" immediately

### Upload Aadhar Card

1. **Book Ticket**: Go to any monument booking page
2. **Fill Details**: Enter all required booking information
3. **Upload Aadhar**: In the "Upload Aadhar Card" section:
   - Click "Choose File" or drag & drop
   - Select PDF or image file
   - See filename display after selection
4. **Submit**: Complete the booking process
5. **File Storage**: File is saved in `media/aadhar_uploads/` directory

## File Structure

```
project/
├── Backend/
│   ├── settings.py          # Django settings
│   └── urls.py              # URL configuration
├── Frontend/
│   ├── src/
│   │   ├── Agra/            # Agra monuments booking forms
│   │   ├── Hyderabad/       # Hyderabad monuments booking forms
│   │   ├── Jaipur/          # Jaipur monuments booking forms
│   │   ├── Kolkata/         # Kolkata monuments booking forms
│   │   ├── NewDelhi/        # Delhi monuments booking forms
│   │   ├── Pune/            # Pune monuments booking forms
│   │   └── responsive.css   # Responsive styles
│   └── build/
│       └── ticket.html      # Admin dashboard template
├── qrscan/
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   └── payment.py           # Payment handling
├── media/
│   └── aadhar_uploads/      # Uploaded files directory
└── manage.py                # Django management script
```

## API Endpoints

### Cancel Booking
- **URL**: `/cancel-booking/`
- **Method**: POST
- **Parameters**: `booking_id`
- **Response**: JSON with success/error status

### File Upload
- **URL**: `/book/`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **File Field**: `aadharCard`

## Database Changes

### MonumentTickets Model Updates
- Added `aadhar_card_file` field for file uploads
- Added `cancelled` boolean field
- Added `cancelled_at` timestamp field
- Updated `phone` field to CharField for better validation

## Troubleshooting

### Common Issues

1. **File Upload Not Working**
   - Ensure `media/aadhar_uploads/` directory exists
   - Check form has `encType="multipart/form-data"`

2. **Cancel Button Not Responding**
   - Check JavaScript console for errors
   - Verify CSRF token is properly configured

3. **Mobile View Issues**
   - Clear browser cache
   - Check responsive CSS is loaded

4. **Migration Errors**
   - Delete migration files in `qrscan/migrations/` (except `__init__.py`)
   - Run `python manage.py makemigrations` again

### Performance Tips

1. **File Storage**: Consider using cloud storage for production
2. **Database**: Use PostgreSQL for better performance in production
3. **Caching**: Enable Django caching for better response times
4. **Media Serving**: Use a CDN for serving uploaded files

## Security Considerations

1. **File Upload Security**: Only PDF and image files are accepted
2. **CSRF Protection**: Enabled for all forms
3. **File Size Limits**: Set in Django settings (5MB default)
4. **User Authentication**: Required for admin dashboard access

## Future Enhancements

1. **Email Notifications**: Send emails on booking cancellation
2. **Audit Trail**: Log all cancellation activities
3. **Bulk Operations**: Cancel multiple bookings at once
4. **File Preview**: Show thumbnail of uploaded Aadhar cards
5. **Advanced Search**: Filter by upload status, cancellation date, etc.

## Support

For issues or questions, check:
1. Django logs in the console
2. Browser developer tools console
3. Network tab for API request/response details
4. Database entries in Django admin panel

Happy booking! 🎫🏛️
