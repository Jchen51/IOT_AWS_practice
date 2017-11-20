#camera_project.py
import time
import boto3

s3 = boto3.resource('s3')

def main():
    #while(1):
        #get data
        distance = 1 #sensor distance

        if distance < 5: #or whatever distance
            #take photo

            #get address of photo
            fileName = 'menu1.jpg'

            #upload photo
            # for bucket in s3.buckets.all():
                # print(bucket.name)
            bucketName = 'tchen44-test'

            photo = open(fileName, 'rb')
            #you can change the key to change the upload name
            #makes it easier to sort?
            s3.Bucket(bucketName).put_object(Key=fileName,Body=photo )

        #time.sleep(5) # sleep for 5 seconds


if __name__ == '__main__':
    main()
