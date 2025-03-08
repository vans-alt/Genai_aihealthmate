# GenAI-Healthcare
# AIHealthMate - GenAI Healthcare Application

## Overview
AIHealthMate is a Generative AI-powered healthcare application designed to process and analyze medical prescriptions using AWS and Informatica services. This application enables users to upload doctor prescriptions and interact with an AI chatbot to simplify medical jargon, clarify doubts, and gain deeper insights into their health conditions.

## Features
- **Upload and Analyze Doctor Prescriptions**: Extracts and processes medical data from uploaded prescriptions.
- **Conversational AI Chatbot**: Provides simplified explanations, medication details, and health recommendations.
- **AWS Services Used**:
  - **Amazon S3**: Secure storage for prescription uploads.
  - **Amazon Bedrock**: GenAI model processing.
  - **Amazon Textract**: Extracts text and structure from prescriptions.
  - **Amazon Comprehend Medical**: Processes and understands medical terminology.
  - **AWS IAM & Cognito**: Manages user authentication and security.
  - **AWS Amplify**: Frontend hosting and deployment.
  - **Amazon SNS**: Sends alerts and notifications.
- **Integration with Informatica Services**: Enables advanced data processing, analysis, and automation.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Hosted on AWS Amplify)
- **Backend**: AWS Lambda, API Gateway
- **AI Processing**: Amazon Bedrock, Textract, Comprehend Medical
- **Database**: AWS S3, DynamoDB
- **Security**: AWS Cognito, IAM
- **Messaging & Alerts**: Amazon SNS
- **Data Analytics**: Informatica Services

## Installation & Setup
### Prerequisites
- AWS account with required services enabled.
- Informatica services access.

### Clone Repository
```sh
 git clone https://github.com/yourusername/AIHealthMate.git
 cd AIHealthMate
```

### Frontend Setup
Simply open the `index.html` file in a browser or deploy it using AWS Amplify.

### Backend Deployment
1. Configure AWS services (S3, Textract, Bedrock, Comprehend Medical, Cognito, IAM).
2. Deploy Lambda functions and API Gateway.
3. Integrate with Informatica services.

## Usage
1. **Upload Prescription**: Users upload a scanned prescription.
2. **AI Processing**: Textract extracts data, Comprehend Medical processes terms, and Bedrock enables AI chat.
3. **Conversational AI**: Users can chat with AI for explanations, medication reminders, and insights.
4. **Notifications**: SNS sends alerts for reminders and updates.

## Contributing
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push changes: `git push origin feature-branch`
5. Open a Pull Request.



