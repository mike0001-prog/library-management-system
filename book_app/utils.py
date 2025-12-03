from django.contrib import messages
import csv
import pandas as pd
from django.shortcuts import redirect
from .models import Category,Book
import zipfile
from django.core.files.base import ContentFile 

def extract_file(request,file,images):
    image_file = images.name
    f = file.name
    required_fields = ["category","name","author","isbn","edition","about_book","quantity"]
    if not all(field in reader.fieldnames for field in required_fields):
        messages.error(request,"fields in excel/csv file should align with sample provided in help")
        return redirect("add_question")
    if not f.endswith("csv") and not f.endswith("xlsx") and not image_file.endswith("zip"):
        messages.error(request,"file type not supported accepts only csv and excel, accepts only zip files for images")
        return redirect("add_question")
    if f.endswith("csv"):
        d = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(d)
    elif f.endswith("xlsx"):
        df  = pd.read_excel("Book1.xlsx")
        reader = df.to_dict(orient='records')
    for line in reader:
        print(line)
        try:
            category = Category.objects.get(name=line["category"])
        except Exception:
            Category.objects.create(name=line["category"])
            category = Category.objects.get(name=line["category"])
            print("created")
        
            book=Book.objects.create(name=line["name"],
                                    author=line["author"],
                                    isbn=line["isbn"],
                                    quantity=line["quantity"],
                                    edition=line["edition"],
                                    about_book=line["about_book"],
                                    Category=category)
            if images:
                image_folder = zipfile.ZipFile(images)
                image_dict = {name: image_folder.read(name) for name in image_folder.namelist()}
                image_name = line["image"]
                image_data=image_dict.get(image_name)
                if image_data:
                    book.image.save(image_name,ContentFile(image_data),save=True)
        messages.success(request,"books added successfully")
        
            
            
