<?php
include("db_connect.php");

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    echo "<p>Please log in first.</p>";
    exit();
}

$user_id = $_SESSION['user_id']; // Get User ID from session

// Fetch profile details from profile_db
$query = "SELECT name, age, gender, dob, height, weight FROM users WHERE id = ?";
$stmt = $profile_conn->prepare($query);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Profile</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .container { width: 50%; margin: auto; padding: 20px; background: #f8d7da; border-radius: 8px; }
        h2 { color: red; }
        .button { background: red; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Your Profile</h2>
        <?php if ($result->num_rows > 0) { 
            $row = $result->fetch_assoc(); ?>
            <p><strong>Name:</strong> <?= htmlspecialchars($row['name']) ?></p>
            <p><strong>Age:</strong> <?= htmlspecialchars($row['age']) ?></p>
            <p><strong>Date of Birth:</strong> <?= htmlspecialchars($row['dob']) ?></p>
            <p><strong>Gender:</strong> <?= htmlspecialchars($row['gender']) ?></p>
            <p><strong>Height:</strong> <?= htmlspecialchars($row['height']) ?> cm</p>
            <p><strong>Weight:</strong> <?= htmlspecialchars($row['weight']) ?> kg</p>
        <?php } else { ?>
            <p>No profile found. Please update your details.</p>
        <?php } ?>
        <a href="profile_fill.php"><button class="button">Edit Profile</button></a>
    </div>
</body>
</html>
<?php
$stmt->close();
$profile_conn->close();
?>
