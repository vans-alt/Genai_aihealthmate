<?php
// Database connection
$conn = new mysqli("localhost", "root", "", "profile_db");

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $age = $_POST['age'];
    $dob = $_POST['dob'];
    $gender = $_POST['gender'];
    $height = $_POST['height'];
    $weight = $_POST['weight'];
    $user_id = 3; // Assuming user ID is static for now

    // Check if user already exists
    $check_query = "SELECT * FROM users WHERE id = ?";
    $stmt = $conn->prepare($check_query);
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // Update existing profile
        $update_query = "UPDATE users SET name=?, age=?, dob=?, gender=?, height=?, weight=? WHERE id=?";
        $stmt = $conn->prepare($update_query);
        $stmt->bind_param("sissiii", $name, $age, $dob, $gender, $height, $weight, $user_id);
    } else {
        // Insert new profile
        $insert_query = "INSERT INTO users (name, age, dob, gender, height, weight, id) VALUES (?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($insert_query);
        $stmt->bind_param("sissiii", $name, $age, $dob, $gender, $height, $weight, $user_id);
    }

    if ($stmt->execute()) {
        // Redirect to profile.php after saving
        header("Location: profile.php");
        exit(); // Ensure script stops execution after redirection
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Profile</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: rgb(234, 189, 193)  }
        .container { width: 50%; margin: auto; padding: 20px; background:white; border-radius: 8px; }
        h2 { color: red; }
        .button { background: red; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Edit Profile</h2>
        <form method="post">
            <label>Name: <input type="text" name="name" value="<?= htmlspecialchars($profile_data['name'] ?? '') ?>" required></label><br><br>
            <label>Age: <input type="number" name="age" value="<?= htmlspecialchars($profile_data['age'] ?? '') ?>" required></label><br><br>
            <label>Date of Birth: <input type="date" name="dob" value="<?= htmlspecialchars($profile_data['dob'] ?? '') ?>" required></label><br><br>
            <label>Gender: 
                <select name="gender" required>
                    <option value="Male" <?= ($profile_data['gender'] ?? '') == 'Male' ? 'selected' : '' ?>>Male</option>
                    <option value="Female" <?= ($profile_data['gender'] ?? '') == 'Female' ? 'selected' : '' ?>>Female</option>
                    <option value="Other" <?= ($profile_data['gender'] ?? '') == 'Other' ? 'selected' : '' ?>>Other</option>
                </select>
            </label><br><br>
            <label>Height (cm): <input type="number" name="height" value="<?= htmlspecialchars($profile_data['height'] ?? '') ?>" required></label><br><br>
            <label>Weight (kg): <input type="number" name="weight" value="<?= htmlspecialchars($profile_data['weight'] ?? '') ?>" required></label><br><br>
            <button class="button" type="submit">Save</button>
        </form>
    </div>
</body>
</html>
