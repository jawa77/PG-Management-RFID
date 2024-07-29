# RFID-Based Authentication System for PG Management

This project is an RFID-based authentication system designed for managing a PG (paying guest) facility. It includes a dashboard for monitoring and controlling access, as well as Raspberry Pi code for RFID reader interaction.

## Features

- **Dashboard**
  - View logs of all activities.
  - Monitor the number of people inside and outside the facility.
  - Activate and deactivate RFID cards at any time.
  - Change restricted access times.
  - Export data to Excel sheets.
  - All data is connected and stored in MongoDB.
  - Additional features will be added in future updates.

- **RFID Reader (Hardware)**
  - Easily activate a card by holding it near the RFID reader.
  - Deactivate or reactivate cards as needed.

## Project Structure

The project consists of two main parts:

1. **Dashboard**
   - A web-based interface for managing the PG facility.
   - Includes all logs, user management, and configuration options.

2. **Hardware**
   - Code for the Raspberry Pi to interact with the RFID reader.

## Dashboard

The dashboard provides a comprehensive interface to manage all aspects of the RFID-based authentication system. Key functionalities include:

- Viewing real-time logs and history of access events.
- Monitoring the current number of people inside the facility.
- Activating and deactivating RFID cards.
- Changing restricted access times.
- Exporting logs and user data to Excel for analysis.

### Dependencies

- MongoDB for data storage.
- Web server (e.g., Node.js, Python Flask/Django) to host the dashboard.

## Hardware

The hardware component consists of a Raspberry Pi connected to an RFID reader. The code for the Raspberry Pi handles:

- Reading RFID cards.
- Communicating with the dashboard via API to validate and log access events.

### Configuration

The `config.json` file contains configuration settings for the Raspberry Pi code. You need to update the `secretKey` value in this file.

```json
{
  "apiUrl": "http://your-dashboard-api-url",
  "secretKey": "your-secret-key"
}
