read -p "Install python 3.9? (Y/n) " INSTALL_PY
read -p "Enter the lambda function name: " LAMBDA_NAME

if [[ "$INSTALL_PY" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    bash 0-install-python3.9.sh
fi

echo $LAMBDA_NAME > stack-name.txt

echo ================
echo  CREATE BUCKET 
echo ================
bash 1-create-bucket.sh

echo ================
echo   BUILD LAYER 
echo ================
bash 2-build-layer.sh

echo ================
echo     DEPLOY
echo ================
bash 3-deploy.sh

echo ================
echo  DELETE BUCKET
echo ================

ARTIFACT_BUCKET=$(cat bucket-name.txt)
aws s3 rb --force s3://$ARTIFACT_BUCKET
rm bucket-name.txt