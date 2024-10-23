<!-- PHP code to establish connection with the localserver -->
 '''php
<?php
$user = 'root';
$password = 'Afham.my0799';
$database = 'car_recommendation';
$servername = 'localhost:3306';

$mysqli = new mysqli($servername, $user, $password, $database);

if ($mysqli->connect_error) {
    die('Connect Error (' . $mysqli->connect_errno . ') ' . $mysqli->connect_error);
}

$sql = "SELECT * FROM userdata ORDER BY score DESC";
$result = $mysqli->query($sql);

$mysqli->close();
?>

<!-- HTML code to display data in tabular format -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cars Display</title>
    <!-- CSS FOR STYLING THE PAGE -->
    <style>
        table {
            margin: 0 auto;
            font-size: large;
            border: 1px solid black;
        }
        h1 {
            text-align: center;
            color: #006600;
            font-size: xx-large;
            font-family: 'Gill Sans', 'Gill Sans MT', 'Calibri', 'Trebuchet MS', 'sans-serif';
        }
        td {
            background-color: #E4F5D4;
            border: 1px solid black;
        }
        th, td {
            font-weight: bold;
            border: 1px solid black;
            padding: 10px;
            text-align: center;
        }
        td {
            font-weight: lighter;
        }
    </style>
</head>
<body>
    <section>
        <h1>Cars Display</h1>
        <!-- TABLE CONSTRUCTION -->
        <table>
            <tr>
                <th>Brand</th>
                <th>Image</th>
                <th>Link</th>
                <th>Price</th>
                <th>Condition</th>
                <th>Mileage</th>
                <th>Engine</th>
                <th>Transmission</th>
                <th>Body Type</th>
                <th>Location</th>
            </tr>
            <!-- PHP CODE TO FETCH DATA FROM ROWS -->
            <?php
                while ($rows = $result->fetch_assoc()) {
            ?>
            <tr>
                <!-- FETCHING DATA FROM EACH ROW OF EVERY COLUMN -->
                <td><?php echo $rows['Brand']; ?></td>
                <td><?php echo $rows['Image']; ?></td>
                <td><?php echo $rows['Link']; ?></td>
                <td><?php echo $rows['Price']; ?></td>
                <td><?php echo $rows['Condition']; ?></td>
                <td><?php echo $rows['Mileage']; ?></td>
                <td><?php echo $rows['Engine']; ?></td>
                <td><?php echo $rows['Transmission']; ?></td>
                <td><?php echo $rows['Body Type']; ?></td>
                <td><?php echo $rows['Location']; ?></td>
            </tr>
            <?php
                }
            ?>
        </table>
    </section>
</body>
</html>