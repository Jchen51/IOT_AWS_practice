#camera_project.py

#loop to get camera data
#if camera data is within a certain range:
#   1. take photo
#   2. upload photo
#sleep to wait for door to close/so we don't spam photos


import time
import datetime
import boto3
import json

s3 = boto3.resource('s3')

def main():
    #while(1):
        #get data
        distance = 1 #sensor distance

        if distance < 5: #or whatever distance
            #take photo

            #get address of photo
            # fileName = '2.jpg'

            #upload photo
            # for bucket in s3.buckets.all():
                # print(bucket.name)
            bucketName = 'tchen44-test'

            # photo = open(fileName, 'rb')
            #you can change the key to change the upload name
            #makes it easier to sort?
            # keyName = fileName #+'-'+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            # s3.Bucket(bucketName).put_object(Key=keyName,Body=photo )
            # print "uploaded"

            #simple recognition
            '''

            fileName='4.jpg'
            bucket='bucket'
            client=boto3.client('rekognition','us-west-2')

            response = client.detect_faces(Image={'S3Object':{'Bucket':bucketName,'Name':fileName}},Attributes=['ALL'])

            print('Detected faces for ' + fileName)
            for faceDetail in response['FaceDetails']:
                print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                    + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
                print('Here are the other attributes:')
                print(json.dumps(faceDetail, indent=4, sort_keys=True))
            '''

            #comparison
            '''
            sourceFile='2.jpg'
            targetFile='4.jpg'

            client=boto3.client('rekognition','us-west-2')

            response=client.compare_faces(SimilarityThreshold=70,
                SourceImage={'S3Object':{'Bucket':bucketName,'Name':sourceFile}},
                TargetImage={'S3Object':{'Bucket':bucketName,'Name':targetFile}})

            for faceMatch in response['FaceMatches']:
                position = faceMatch['Face']['BoundingBox']
                confidence = str(faceMatch['Face']['Confidence'])
                print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + confidence + '% confidence')
            '''

            #messaging
            '''
            
            # Create an SNS client
            client = boto3.client('sns')

            # Send your sms message.
            client.publish(PhoneNumber="+16508238825", Message="Hello World!")
            '''
        #time.sleep(5) # sleep for 5 seconds


if __name__ == '__main__':
    main()
