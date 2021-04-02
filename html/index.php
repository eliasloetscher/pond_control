<!doctype html>
<html lang="de">
    <head>
        <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

	<style>
	    .buttons form, .buttons form div {
		display: inline;
	    }
	    
	    .buttons button {
		display: inline;
		vertical-align: middle;
	    }
	</style>
        <title>Teichsteuerung</title>
    </head>
    <body>
	<center>
	    <br>
	    <h1> Teichsteuerung </h1>
	    <br>

	    <section>
		<h4>Systemstatus</h4>
	    		
		<?php
		    $system_state_file = "/home/pi/Documents/dev/pond_control/system_state.txt";

		    $file = fopen($system_state_file, "r") or die("Unable to open system state file!");
		    $system_state = fgets($file);
		    fclose($file);
		    if ($system_state == "OK") {
			
		    echo '<div id="system_ok" style="background-color:green"><p style="color:white">System: OK<p></p></div><br>';
		    }
		    else {
		    echo '<div id="system_error" style="background-color:red"><p>System: ERROR</p></div>';
		    echo '<form action="reset_error.php" method="post">
		    <button type="submit" class="btn btn-warning">Fehler zurücksetzen</button><br><br>
		    </form>';
		    }    
		?>
	    </section>

	    <section>
		<h4> Manuelle Steuerung </h4>
		<div class="buttons">
		    <form action="on.php" method="post">
			<div>
			    <button type="submit" class="btn btn-success">Einschalten</button>
			</div>
		    </form>
		    <form action="off.php" method="post">
			<div> 
			    <button type="button" class="btn btn-danger">Ausschalten</button>
			</div>
		    </form>
		</div>
	    </section>

	    <section>
		<br><br>
		<h4> Wasserverbrauch </h4>
		<?php
		    $db = new SQLite3('/home/pi/Documents/dev/pond_control/teich.db');
		    $results = $db->query('SELECT * FROM refill_time');

		    echo "<table><tr><td>Monat &nbsp; &nbsp;</td><td>Wasser in l</td></tr>";
		    while ($row = $results->fetchArray()) {
			echo "<tr><td>{$row['month']}</td><td>{$row['time_in_s']}</td></tr>";
		    }
		    echo "</table>";
		?>
	    </section>

	    <section>
		<br><br>
		<h4> Action Log </h4>
		<?php
		    $db = new SQLite3('/home/pi/Documents/dev/pond_control/teich.db');
		    $results = $db->query('SELECT * FROM actions ORDER BY date DESC, time DESC');

		    while ($row = $results->fetchArray()) {
			echo "{$row['date']} {$row['time']} {$row['action']}";
			echo "<br>";
		    }
		?>
	    </section>
	</center>
    </body>
</html>
