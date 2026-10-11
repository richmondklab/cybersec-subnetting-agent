# CyberSec Subnetting Agent

A practical cybersecurity and networking learning project that helps students calculate subnets, solve lab exercises, and get guided hints for subnetting tasks.

## Features

- Calculate IPv4 subnet information from IP + CIDR
- Convert subnet mask to CIDR and vice versa
- Generate network lab exercises
- Grade student answers
- Provide built-in AI-style hints (OpenAI optional)
- Simple web interface for student interaction

## Project structure

- `app.py` – Flask web app and API
- `subnetting_engine.py` – subnetting logic and exercise generation
- `templates/index.html` – main UI
- `static/style.css` – styling
- `static/app.js` – front-end behavior
- `requirements.txt` – Python dependencies
- `README.md` – usage instructions

## Quick start

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. Open the app in a browser:

   ```text
   http://localhost:5000
   ```

## Optional AI hints

Set an OpenAI API key to enable AI-generated guidance:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

If no key is set, the app uses built-in subnetting hints and explanations.

## Example usage

The UI lets a student do the following:

- Enter an IP and CIDR, like `192.168.10.0` and `26`
- Calculate the network, broadcast, subnet mask, first host, last host, and usable hosts
- Generate a lab exercise automatically
- Submit answers and receive a score
- Request a hint without revealing the complete answer

## Example API endpoints

- `GET /` – main interface
- `POST /api/calculate` – calculate subnet details
- `POST /api/generate-exercise` – create a new exercise
- `POST /api/check-answer` – grade a student answer
- `POST /api/hint` – return a guided hint
- `POST /api/explain` – return a concept explanation

## Learning goals

This project is designed for training labs around:

- IPv4 subnetting
- CIDR notation
- Network segmentation
- Host calculations
- Cybersecurity practical labs

## License

MIT
