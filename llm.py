import boto3
import json

# Initialize AWS Bedrock Client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def query_bedrock_llm(patient_data, user_query):
    """Send patient data & query to AWS Bedrock LLM (Claude 3 Sonnet) and get a response."""

    # Construct prescription details
    prescription_details = "\n".join([
        f"- Medicine: {med['medicine_name']}, Dosage: {med['dosage']}, Duration: {med['duration']}"
        for med in patient_data
    ])

    # Construct the prompt for Claude 3 Sonnet
    prompt = f"""
    You are a helpful AI assistant specializing in healthcare. Answer user queries based on the following prescription details.

    *Patient Prescription Details*:
    - *Name*: {patient_data[0]['patient_name']}
    - *Doctor*: {patient_data[0]['doctor_name']}
    - *Prescription Date*: {patient_data[0]['prescription_date']}
    - *Medications*: 
    {prescription_details}

    *User Query*: {user_query}
    *AI Response*:
    """

    payload = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",  # ✅ REQUIRED FIELD
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9
    })

    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # ✅ Correct Model ID
            contentType="application/json",
            accept="application/json",
            body=payload
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        return response_body["content"][0]["text"]  # Extract response text
    except Exception as e:
        return f"Error querying AI: {str(e)}"