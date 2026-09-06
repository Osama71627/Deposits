# Deposits Platform - Architecture Documentation

> **Scope:** This document describes the intended architecture and roadmap, not a verification of completed functionality. Flutter, payment providers, ZATCA compliance, automatic allocation, comprehensive RBAC, encryption, and automated reporting are not established production capabilities. See [README](../README.md) for the current implementation and setup limitations. SQLite is the current default database; PostgreSQL is optional. Docker configuration requires environment and Redis adjustments before use.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Web App  │  │  Flutter │  │  Admin   │  │   API    │   │
│  │ (HTML/JS) │  │  (Mobile)│  │ (Django) │  │ Clients  │   │
│  └─────┬─────┘  └─────┬────┘  └────┬─────┘  └────┬─────┘   │
└────────┼──────────────┼────────────┼──────────────┼─────────┘
         │              │            │              │
         │              │            │              │
┌────────┼──────────────┼────────────┼──────────────┼─────────┐
│        │         Load Balancer / Nginx               │       │
│        └──────────────┬────────────┘                 │       │
│                       │                              │       │
│              ┌────────┴────────┐                     │       │
│              │  Web (Gunicorn) │  Daphne (Channels) │       │
│              │     :8000       │     :8001           │       │
│              └────────┬────────┘                     │       │
│                       │                              │       │
│              ┌────────┴──────────────────────────────┘       │
│              │              Application Layer                │
│              │  ┌──────────────────────────────────────┐    │
│              │  │  Django REST Framework - API          │    │
│              │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ │    │
│              │  │  │Accounts│Customers│Couriers│WMS│  │ │    │
│              │  │  └────┘ └────┘ └────┘ └────┘ └────┘ │    │
│              │  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ │    │
│              │  │  │Fleet│Assets│Acct.│ CRM │ HR  │ │    │
│              │  │  └────┘ └────┘ └────┘ └────┘ └────┘ │    │
│              │  │  ┌────┐ ┌────┐ ┌────┐                 │    │
│              │  │  │Pay. │Notif.│Analytics│             │    │
│              │  │  └────┘ └────┘ └────┘                 │    │
│              │  └──────────────────────────────────────┘    │
│              └──────────────────────────────────────────────┘
│                                │
│              ┌─────────────────┴──────────────────┐
│              │            Data Layer               │
│              │  ┌─────────┐  ┌─────────┐          │
│              │  │PostgreSQL│  │  Redis  │          │
│              │  └─────────┘  └─────────┘          │
│              └─────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend   | Python 3.12, Django 5.1, DRF 3.15 |
| Database  | PostgreSQL 16 |
| Cache     | Redis 7 |
| Real-time | Django Channels, Daphne |
| Frontend  | HTML5, CSS3, JavaScript ES6 |
| Mobile    | Flutter |
| Auth      | JWT (SimpleJWT), RBAC |
| Payments  | Stripe, PayPal, Moyasar, POS |
| Maps      | Google Maps API |
| Notifications | Firebase Cloud Messaging |
| Compliance | ZATCA E-Invoicing |
| DevOps    | Docker, Nginx, Gunicorn |

## Application Modules

### 1. Accounts (apps/accounts)
- User model with roles (ADMIN, CUSTOMER, COURIER, WAREHOUSE, MANAGER)
- JWT authentication with SimpleJWT
- Role-Based Access Control (RBAC)
- Device management and session tracking
- Complete audit logging

### 2. Customers (apps/customers)
- Customer profiles with loyalty points
- Storage request management with full lifecycle
- QR code generation for item retrieval
- Item tracking and status history

### 3. Couriers (apps/couriers)
- Courier profiles with availability management
- Attendance check-in/check-out
- Earnings tracking
- Performance metrics

### 4. Warehouse / WMS (apps/warehouse)
- Multi-warehouse management
- Zone, shelf, and box hierarchy
- Automatic space assignment
- Barcode/QR code support
- Inventory auditing

### 5. Fleet (apps/fleet)
- Vehicle management
- Geofence zone definitions
- Route planning and tracking
- Real-time location tracking via WebSockets

### 6. Assets (apps/assets)
- Asset categorization
- Assignment tracking
- Maintenance records and lifecycle

### 7. Accounting (apps/accounting)
- Chart of Accounts
- Journal entries and general ledger
- Invoicing with ZATCA compliance
- Accounts receivable/payable
- Financial reporting

### 8. CRM (apps/crm)
- Customer segmentation
- Support ticket system
- Customer feedback and complaints

### 9. HR (apps/hr)
- Employee records
- Attendance tracking
- Leave management
- Payroll processing

### 10. Payments (apps/payments)
- Multi-gateway support
- POS device integration
- Payment processing and refunds

### 11. Notifications (apps/notifications)
- In-app notifications
- Push notifications via FCM
- Real-time WebSocket updates

### 12. Analytics (apps/analytics)
- Dashboard metrics
- KPI tracking
- Automated report generation

## Security Architecture

- JWT with refresh token rotation
- RBAC with granular permissions
- Rate limiting (100/hour anonymous, 1000/hour authenticated)
- Audit logging for all operations
- Data encryption at rest and in transit
- CSRF protection
- XSS prevention
- SQL injection prevention via ORM

## Scalability Strategy

1. **Database**: PostgreSQL with connection pooling (PgBouncer)
2. **Caching**: Redis for session storage, API caching, and real-time messaging
3. **Application**: Horizontal scaling with Gunicorn workers
4. **Media**: CDN integration via AWS S3 / DigitalOcean Spaces
5. **Asynchronous**: Celery for background tasks
6. **Real-time**: Daphne for WebSocket connections
7. **Load Balancing**: Nginx reverse proxy

## API Documentation

The platform provides a complete REST API documented via Swagger UI:

- **URL**: `/api/docs/`
- **Schema**: `/api/schema/`

All API endpoints follow RESTful conventions and return JSON responses.

## Deployment Architecture

```bash
# Development
python manage.py runserver

# Production (Docker)
cd docker
docker-compose up -d

# Environment Variables
SECRET_KEY=your-secret-key
DEBUG=0
DB_NAME=deposits_db
DB_USER=deposits_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Future Expansion

- Flutter mobile applications (Customer & Courier)
- AI-powered demand forecasting
- Dynamic pricing engine
- Multi-language support (AR/EN)
- Multi-region deployment
- Third-party integrations API
