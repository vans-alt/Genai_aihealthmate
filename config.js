const poolData = {
    UserPoolId: "eu-north-1_KlqHnN9y9",  // Replace with your actual User Pool ID
    ClientId: "6a6qvqgomq0us3vc6ocq1emd4i" // Replace with your actual App Client ID
};

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
