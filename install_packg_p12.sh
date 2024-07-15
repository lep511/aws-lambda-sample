docker pull public.ecr.aws/sam/build-python3.12:latest
docker run -it --security-opt seccomp=unconfined public.ecr.aws/sam/build-python3.12:latest /bin/bash

cd
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
mkdir -p python

cat <<EOF > requirements.txt
pandas
requests
EOF

python -m pip install -r requirements.txt -t python/
cd python
rm -rf *dist-info
cd ..
zip -r lambda-layer.zip python

curl -F "file=@/root/lambda-layer.zip" https://tmpfiles.org/api/v1/upload
# Download the file follow the link
