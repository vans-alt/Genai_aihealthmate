import json
import boto3
import pymysql
import os
import re
import traceback
from datetime import datetime

# AWS Clients
s3 = boto3.client("s3")
textract = boto3.client("textract")

# RDS Credentials (Use environment variables)
RDS_HOST = os.getenv("RDS_HOST", "prescription-db.cv8sgw4ow1xg.us-east-1.rds.amazonaws.com")
RDS_USER = os.getenv("RDS_USER", "admin")
RDS_PASS = os.getenv("RDS_PASS", "humaraproject")
RDS_DBNAME = os.getenv("RDS_DBNAME", "prescription_db")

def extract_text_from_s3(bucket, key):
    """Extract text from an image in S3 using Textract."""
    try:
        print(f"Extracting text from S3: Bucket={bucket}, Key={key}")
        response = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucket, "Name": key}},
            FeatureTypes=["FORMS"]
        )
        text = " ".join([item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"])
        print("Extracted Text:", text)
        return text
    except Exception as e:
        print("Error in Textract:", str(e))
        traceback.print_exc()
        return ""

def extract_patient_details(text):
    """Extract patient details from the prescription text using regex."""
    try:
        patient_match = re.search(r'ID:\s*\d+\s*-\s*(.+?)\s*\(', text)
        doctor_match = re.search(r'Dr\.\s*([\w\s]+)', text)
        date_match = re.search(r'Date:\s*(\d{1,2}-[A-Za-z]{3}-\d{4})', text)

        patient_name = patient_match.group(1).strip() if patient_match else "Unknown"
        doctor_name = doctor_match.group(1).strip() if doctor_match else "Unknown"
        date_str = date_match.group(1) if date_match else "01-Jan-1970"
        
        try:
            formatted_date = datetime.strptime(date_str, "%d-%b-%Y").strftime("%Y-%m-%d")
        except ValueError:
            formatted_date = "1970-01-01"

        patient_data = {
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "prescription_date": formatted_date
        }
        
        print("Extracted Patient Data:", patient_data)
        return patient_data

    except Exception as e:
        print("Error extracting patient details:", str(e))
        return {"patient_name": "Unknown", "doctor_name": "Unknown", "prescription_date": "1970-01-01"}

def extract_medicines(text):
    """Extract medicines, dosage, and duration using regex."""
    medicine_pattern = re.compile(r"(TAB\.|CAP\.)?\s*([\w\s]+)\s+([\d/]+[\s\w,]*)\s+(\d+\s+Days)")
    medicines = []
    
    for match in medicine_pattern.finditer(text):
        medicine_name = match.group(2).strip()
        dosage = match.group(3).strip()
        duration = match.group(4).strip()
        medicines.append({"Text": medicine_name, "Dosage": dosage, "Duration": duration})
    
    print("Extracted Medicines:", medicines)
    return medicines

def store_in_rds(patient_data, medicines):
    """Store extracted patient details and medications in MySQL RDS."""
    conn = None
    try:
        print("Connecting to RDS...")
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASS,
            database=RDS_DBNAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cur:
            # Insert into patient_prescriptions table
            sql_patient = """
                INSERT INTO patient_prescriptions (patient_name, doctor_name, prescription_date)
                VALUES (%s, %s, %s)
            """
            cur.execute(sql_patient, (
                patient_data["patient_name"],
                patient_data["doctor_name"],
                patient_data["prescription_date"]
            ))
            
            prescription_id = cur.lastrowid  # Get the last inserted prescription ID
            conn.commit()  # Ensure patient data is stored before medications

            # Ensure prescription_id is valid before inserting medicines
            if not prescription_id:
                raise ValueError("Failed to retrieve prescription_id from patient_prescriptions")

            # Insert into medications table
            sql_medicine = """
                INSERT INTO medications (medicine_name, dosage, duration,prescription_id )
                VALUES (%s, %s, %s, %s)
            """
            for med in medicines:
                cur.execute(sql_medicine, (med["Text"], med["Dosage"], med["Duration"],prescription_id ))

        conn.commit()  # Commit medications insertion
        print("Patient prescription and medications stored successfully.")

    except pymysql.err.IntegrityError as e:
        print(f"Foreign Key Constraint Error: {e}")
        conn.rollback()  # Rollback if foreign key constraint fails

    except Exception as e:
        print(f"Database Error: {e}")
        traceback.print_exc()
        raise RuntimeError("Database Connection Failed")

    finally:
        if conn:
            conn.close()

def lambda_handler(event, context):
    """Lambda function triggered by S3 to process prescriptions."""
    try:
        print("Lambda function invoked.")
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        text = extract_text_from_s3(bucket, key)
        
        if not text:
            raise ValueError("No text extracted from the image.")

        patient_data = extract_patient_details(text)
        medicines = extract_medicines(text)

        # Store only patient prescriptions and medications
        store_in_rds(patient_data, medicines)

        return {"statusCode": 200, "body": json.dumps("Patient Prescriptions & Medications Stored Successfully")}
    
    except Exception as e:
        print("Lambda Execution Failed:", str(e))
        traceback.print_exc()
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}

def get_prescription_details(patient_name):
    """Fetch prescription details from RDS."""
    try:
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASS,
            database=RDS_DBNAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cur:
            sql_query = """
            SELECT pp.patient_name, pp.doctor_name, pp.prescription_date, 
                   m.medicine_name, m.dosage, m.duration
            FROM patient_prescriptions pp
            JOIN medications m ON pp.id = m.prescription_id
            WHERE pp.patient_name = %s
            """
            cur.execute(sql_query, (patient_name,))
            results = cur.fetchall()
        conn.close()
        return results
    except Exception as e:
        print("Error fetching data from RDS:", str(e))
        return []

if __name__ == "__main__":
    import json

    # Simulate an S3 event with multiple files
    test_event = {
        "Records": [
            
            {
                "s3": {
                    "bucket": {
                        "name": "prescription-uploads1"
                    },
                    "object": {
                        "key": "data3.png"
                    }
                }
            }
        ]
    }

    # Call the Lambda handler function manually
    response = lambda_handler(test_event, None)
    print(json.dumps(response, indent=4))
