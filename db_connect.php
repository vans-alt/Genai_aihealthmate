<?php
// Connection for user authentication DB
$user_auth_conn = new mysqli("localhost", "root", "", "user_auth");

// Check if connection failed
if ($user_auth_conn->connect_error) {
    die("❌ Connection failed to user_auth: " . $user_auth_conn->connect_error);
}

// Connection for profile DB
$profile_conn = new mysqli("localhost", "root", "", "profile_db");

// Check if connection failed
if ($profile_conn->connect_error) {
    die("❌ Connection failed to profile_db: " . $profile_conn->connect_error);
}

session_start();
?>
