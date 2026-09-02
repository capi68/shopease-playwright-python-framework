#  ShopEase - E2E Test Automation Framework

An end-to-end automated testing suite designed for the **ShopEase** e-commerce platform. Built with **Python 3.10+**, **Playwright**, and **Pytest**, implementing production-ready architectural patterns like **Page Object Model (POM)** and robust session state management.

---

##  Key Features

- **Page Object Model (POM):** Clean abstraction of UI pages and reusable component wrappers.
- **Isolated State Management:** Session storage reusability (`localStorage`) for Customer and VIP authentication roles without UI login overhead on every test.
- **Comprehensive E2E Coverage:** Validates authentication, product catalog filtering/sorting, stock limitations (`prod-011` out-of-stock edge cases), cart operations, multi-step checkout wizard, order history, and cross-page data persistence.
- **Parallel & Isolated Execution:** Guaranteed test independence through Pytest fixtures and clean browser contexts.
- **Rich Test Reporting:** Integrated with **Allure Framework** including step logging, test documentation, and failure evidence.

---

##  Tech Stack

- **Language:** Python 3.10+
- **Core Automation:** Playwright
- **Test Runner:** Pytest / `pytest-playwright`
- **Reporting:** Allure (`allure-pytest`)
- **Containerization:** Docker (App under test execution)

---

##  Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose

### Application Setup
```bash
docker compose up --build -d
curl http://localhost:5174/health

### Instalation
- pip install pytest playwright allure-pytest pytest-playwright
- playwright install

# Execute full test suite
pytest

# Execute tests with Allure reporting
pytest --alluredir=allure-results
allure serve allure-results
