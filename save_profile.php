<?php
session_start();
include 'db_connect.php';

if (!isset($_SESSION['user_id'])) {
    echo "Please log in first.";
    exit();
}

$user_id = $_SESSION['user_id'];

// Get form data safely
$name = $_POST['name'] ?? '';
$age = $_POST['age'] ?? '';
$gender = $_POST['gender'] ?? '';
$dob = $_POST['dob'] ?? '';
$height = $_POST['height'] ?? '';
$weight = $_POST['weight'] ?? '';

// Validate data
if (empty($name) || empty($age) || empty($gender) || empty($dob) || empty($height) || empty($weight)) {
    echo "All fields are required!";
    exit();
}

// Prevent SQL injection
$query = "UPDATE users SET name = ?, age = ?, gender = ?, dob = ?, height = ?, weight = ? WHERE id = ?";
$stmt = $profile_conn->prepare($query);
$stmt->bind_param("sisssii", $name, $age, $gender, $dob, $height, $weight, $user_id);

if ($stmt->execute()) {
    echo "Profile updated successfully!";
    header("Location: profile_fill.php"); // Redirect back to profile
} else {
    echo "Error updating profile: " . $stmt->error;
}

$stmt->close();
$profile_conn->close();
?>
