import json
import lambda_function  # Replace with your actual filename (without .py)

# Load the test event
with open("event.json", "r") as f:
    event = json.load(f)

# Call the Lambda function and capture the response
response =lambda_function.lambda_handler(event, None)

# Print the response in a readable format
print(json.dumps(response, indent=2))
