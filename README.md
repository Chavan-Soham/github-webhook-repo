# GitHub Event Webhook Dashboard

This project provides a webhook receiver and dashboard for GitHub repository events. It’s designed to capture and store push, pull request, and merge events (such as when a pull request is merged into the master branch), then display them in a user-friendly interface.

## Features

- **Webhook Endpoint**: Receives GitHub event payloads for `push` and `pull_request` (including merges).
- **Event Storage**: Stores event details in a MongoDB database.
- **Dashboard UI**: Shows recent events with author, branch info, and UTC timestamp.
- **ngrok Integration**: Easily expose your local server to GitHub using ngrok.

## How It Works

1. **Setup webhook in your GitHub repo**: Point it to your ngrok URL (e.g., `https://<subdomain>.ngrok.io/github-webhook`).
2. **Push and PR events**: When you push or merge pull requests to the master branch, GitHub sends event data to your webhook endpoint.
3. **Event Handling**:
    - `push` events: Author, branch, and timestamp are extracted and saved.
    - `pull_request` events: Details for both opened and merged PRs are processed.
4. **Dashboard**: Visit `/events` to view the latest activity.

## Quick Start

### Prerequisites

- Python 3.x
- MongoDB
- ngrok (for public URL)

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Chavan-Soham/github-event-webhook-dashboard.git
    cd github-event-webhook-dashboard
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Start MongoDB:**
    ```bash
    mongod
    ```

4. **Run the Flask app:**
    ```bash
    python app.py
    ```

5. **Expose your local server using ngrok:**
    ```bash
    ngrok http 5000
    ```
    Use the generated public URL as the webhook URL in your GitHub repo settings.

## Event Data Example

Events are displayed with:
- Author
- Source & target branches
- UTC timestamp

## Folder Structure

- `app.py`: Main Flask application and webhook handler.
- `templates/events.html`: Dashboard UI.
- `testing.py`: Sample payloads and test logic.
- `output text file/`: Example files for testing.

## Screenshots

![Dashboard Example](https://github.com/user-attachments/assets/ed4d13c7-2f8d-4d1d-9455-ff0094ad3acd)

## License

MIT

---

**Thank you for using GitHub Event Webhook Dashboard!**
