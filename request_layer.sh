python3 -m venv test_venv
source test_venv/bin/activate
mkdir python  
pip install requests -t python  
aws lambda publish-layer-version --layer-name requests --zip-file fileb://requests.zip --compatible-runtimes python3.9 --region us-east-1
