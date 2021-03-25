<!DOCTYPE HTML>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>


<h1> Teichsteuerung </h1>

<p> <b> Ventil manuell schalten </b> </p>

<p>
<form action="on.php" method="post">
	<input type="submit" id="switch_on" name="switch_on" value="Einschalten">
</form>
</p><p>
 <form action="off.php" method="post">
	<input type="submit" id="switch_off" name="switch_off" value="Ausschalten">
</form>
</p>


<br>
<p><b> Action Log </b><p>
<?php

$db = new SQLite3('/home/pi/teich.db');

$results = $db->query('SELECT * FROM actions ORDER BY date DESC, time DESC');

//$results = $db->query('SELECT * FROM actions');

while ($row = $results->fetchArray()) {
    echo "{$row['date']} {$row['time']} {$row['action']}";
    echo "<br>";
}

?>

</html>
