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

cd package
zip -9 -r ../my-deployment-package.zip .
cd ..
zip -g my-deployment-package.zip *.py
filesize=$(wc -c my-deployment-package.zip | awk '{print $1}')

if [ "$filesize" -gt 50000000 ]; then
    BUCKET_ID=$(dd if=/dev/random bs=8 count=1 2>/dev/null | od -An -tx1 | tr -d ' \t\n')
    BUCKET_NAME=temp-lambda-function-$BUCKET_ID
    aws s3 mb s3://$BUCKET_NAME
    aws s3 cp my-deployment-package.zip s3://$BUCKET_NAME
    size=$(expr $filesize / 256000)
    aws lambda create-function --function-name $lambdaname\
    --runtime python3.9\
    --role $role\
    --handler $handler\
    --memory-size $size\
    --publish --code S3Bucket=$BUCKET_NAME,S3Key=my-deployment-package.zip
    
    aws s3 rm s3://$BUCKET_NAME --recursive
    aws s3api delete-bucket --bucket $BUCKET_NAME
else
    aws lambda create-function --function-name $lambdaname\
        --runtime python3.9\
        --role $role\
        --handler $handler\
        --publish --zip-file fileb://my-deployment-package.zip
fi
