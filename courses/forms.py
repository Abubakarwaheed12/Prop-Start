import time
from django import forms
import boto3
from django.conf import settings
from .models import (
    Lectures, 
    premium_course,
)


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lectures
        fields = ['lesson', 'name', 'lecture_description', 'video', 'document']

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('video')

        if file:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            key = f"lectures/{int(time.time())}/{file.name}"
            response = s3_client.create_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key
            )

            part_number = 1
            parts = []
            while True:
                chunk = file.read(5 * 1024 * 1024)  # Read 5MB chunks
                print("Chunks : ", chunk)
                if not chunk:
                    break
                part = s3_client.upload_part(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key,
                    UploadId=response['UploadId'],
                    PartNumber=part_number,
                    Body=chunk
                )
                parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                part_number += 1

            s3_client.complete_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                UploadId=response['UploadId'],
                MultipartUpload={'Parts': parts}
            )

            
            if commit:
                instance.save()
        return instance
     


class PremiumForm(forms.ModelForm):
    class Meta:
        model = premium_course
        fields = ['name', 'lecture_description', 'video', 'document']

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('video')

        if file:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            key = f"lectures/{int(time.time())}/{file.name}"
            response = s3_client.create_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key
            )

            part_number = 1
            parts = []
            while True:
                chunk = file.read(5 * 1024 * 1024)  # Read 5MB chunks
                print("Chunks : ", chunk)
                if not chunk:
                    break
                part = s3_client.upload_part(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key,
                    UploadId=response['UploadId'],
                    PartNumber=part_number,
                    Body=chunk
                )
                parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                part_number += 1

            s3_client.complete_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                UploadId=response['UploadId'],
                MultipartUpload={'Parts': parts}
            )

            
            if commit:
                instance.save()
        return instance