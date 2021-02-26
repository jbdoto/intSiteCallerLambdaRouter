# IntSiteCaller Event Upload Router 

https://docs.aws.amazon.com/lambda/latest/dg/images-create.html

https://docs.aws.amazon.com/lambda/latest/dg/images-test.html

https://docs.aws.amazon.com/lambda/latest/dg/python-image.html


### Testing 

    docker build . -t intsitecaller-event-handler:latest

    # default region is used by boto to configure step client
    docker run -e STATE_MACHINE_ARN=arn:aws:states:us-east-1:<account_id>:stateMachine:intsitecaller-1_0_0 \ 
        -e AWS_DEFAULT_REGION=us-east-1 -e AWS_REGION=us-east-1 -e AWS_ACCESS_KEY_ID=<key_id> \
        -e AWS_SECRET_ACCESS_KEY=<key> -p 9000:8080  intsitecaller-event-handler:latest

    # test with empty post body:
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
    
    # or post with data from json file:
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '@sample_s3_event.json'

### Pushing to ECR
    
    aws ecr get-login-password --region us-east-1 --profile=jdoto-ab3 \ 
    | docker login --username AWS --password-stdin 483158796244.dkr.ecr.us-east-1.amazonaws.com

    docker tag intsitecaller-upload-handler 483158796244.dkr.ecr.us-east-1.amazonaws.com/intsitecaller-upload-handler:1.0.0
     
    docker push 483158796244.dkr.ecr.us-east-1.amazonaws.com/intsitecaller-upload-handler:1.0.0

    