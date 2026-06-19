# AI-Content-Moderation-API
We have officially successfully built and showcased the initial prototype of our AI Content Moderation API &amp; Gateway Portal as part of our Advanced Database Management System lab requirements!  This repository features a fully decoupled, async architecture combining a robust Python backend with a high-performance modern user interface.
System Architecture & Implementation Mechanics
1. Robust Backend (Django REST Framework)
API Version Control: Implemented explicit routing matrices under the api/v1/ core prefix to ensure modularity.

Dual-Pipeline Auditing Views: Created distinct function-based API endpoints (moderate_text and moderate_image) inside our core application to process plain text layers and image resource URL strings independently.

Cross-Origin Security Integration: Configured django-cors-headers middleware to handle secure asynchronous local data transfers from the frontend cleanly without blocking browser execution.

2. Live Attribute-Driven Frontend Dashboard (Tailwind CSS)
Persistent Session Matrix: Utilized browser localStorage to manage configuration states (Name, Age, and Role Profile) dynamically across browser refreshes, removing database authentication overhead during rapid prototype testing.

Active Security Interceptors: Designed an immediate client-side data shield. If an active session profile evaluates to a Kid role attribute with an Age under 18, the engine overrides incoming payload structures to force-flag a security policy violation and drop an alert banner.

📂 Repository Code Tree Blueprint
Plaintext
AI Content Moderation API/
├── core/                       # Root Configuration Project App
│   ├── settings.py             # Middleware stacks & Installed apps
│   ├── urls.py                 # Core routing engine mapping api/v1/
│   └── index.html              # Responsive Tailwind UI Dashboard
└── moderator/                  # Primary Core Analytics App
    ├── urls.py                 # Endpoint router matching text/ & image/ paths
    └── views.py                # Business logic views returning JSON payloads
📈 Next Steps on the Project Roadmap
[ ] Migrate localStorage session mock attributes into a permanent PostgreSQL/SQLite user table matrix.

[ ] Connect the image URL input field to a live Computer Vision model (like OpenCV or a cloud moderation API) instead of the simulated verification payload.

[ ] Containerize the entire environment setup using Docker for standardized deployment.
