read -p "Enter package to install or [req.txt]: " packg
read -p "Enter region: [us-east-1]" region

if [[ -z "$region" ]]; then
    export region=us-east-1
fi

if [[ -z "$description" ]]; then
    export description="-"
fi

rm python/ -rf
mkdir -p python

if [[ -z "$packg" ]]; then
    python3 -m pip install -r req.txt -t python/
else
    python3 -m pip install $packg -t python/
fi

zip -r layer.zip python

read -p "Create lambda layer? (y/N) " lambdalay

if [[ "$lambdalay" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    read -p "Enter name layer: " namelayer
    read -p "Enter description: " description
    if [[ -z "$description" ]]; then
        export description="-"
    fi
    aws lambda publish-layer-version --layer-name $namelayer --description $description --zip-file fileb://layer.zip --compatible-runtimes python3.9 --region $region
fi

read -p "Copy lambda layer to S3? (y/N) " lambdlaycopy

if [[ "$lambdlaycopy" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    read -r -p  "Enter the name of the bucket: " bucketname
    aws s3api  create-bucket --bucket $bucketname --region $region
    aws s3api  put-bucket-tagging --bucket $bucketname --tagging 'TagSet=[{Key=Name,Value="'$bucketname'"}]'
    aws s3 cp layer.zip s3://$bucketname/lambda_layer.zip
fi
