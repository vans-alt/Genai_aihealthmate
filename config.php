$conn = new mysqli("localhost", "system", "viyass", "users");

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
