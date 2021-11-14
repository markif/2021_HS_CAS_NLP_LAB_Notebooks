
# Setup

# Software

## Python
- `sudo apt-get install python3-pip python3-testresources`
- `python3 -m pip install --upgrade pip setuptools`

## REST Server
- `python3 -m pip install Flask flask-cors fhnw-nlp-utils`

You might also need to install some specific dependencies/versions of the pickled classifier you are using:
- `python3 -m pip install scikit-learn==0.24.2`
- `python3 -c "import nltk; nltk.download('punkt')"`

### Start REST Server

#### Console
- `python3 rest-server.py`

#### At Startup
- `sudo cp sentiment-classifier-rest-server.service /etc/systemd/system/sentiment-classifier-rest-server.service`
- `sudo systemctl enable sentiment-classifier-rest-server.service`
- `sudo systemctl start sentiment-classifier-rest-server.service`

##### View Logs
- `journalctl -f -u sentiment-classifier-rest-server.service`

## Usage
- `curl -X POST http://localhost:5000/api/v1/sentiment -H 'Content-Type: application/json' -d '["Dies ist ein super Arzt. <br>", "Ein schlechter <p> Arzt."]'`
- `curl -X POST http://localhost:5000/api/v1/sentiment -H 'Content-Type: text/plain' -d 'Dies ist ein super Arzt. <br>'`
