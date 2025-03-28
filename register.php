<?php
session_start();
include 'db.php'; // Database connection

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $confirmPassword = $_POST['confirmPassword'];

    // Check if passwords match
    if ($password !== $confirmPassword) {
        die("<script>alert('Passwords do not match!'); window.location.href='signup.html';</script>");
    }

    // Hash the password for security
    $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

    try {
        // Check if the email already exists
        $stmt = $conn->prepare("SELECT email FROM users WHERE email = :email");
        $stmt->bindParam(':email', $email);
        $stmt->execute();


        if ($stmt->rowCount() > 0) {
            die("<script>alert('Email already exists! Please use another email.'); window.location.href='signup.html';</script>");
        }

        // Insert user into database
        $stmt = $conn->prepare("INSERT INTO users (email, password) VALUES (:email, :password)");
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':password', $hashedPassword);
        $stmt->execute();

        echo "<script>alert('Registration successful! You can now sign in.'); window.location.href='login.html';</script>";
    } catch (PDOException $e) {
        die("Error: " . $e->getMessage());
    }
}
?>
