<!doctype html>
<html>
<head>
<title>Protected - {TITLE}</title>
</head>
<body>
This page is password protected.<br />
<form action="{PYWW}?page={FILE}" method="post">
<input type="password" name="pass" id="pass"></input>
<br />
<input type="submit" value="Proceed" />
</form>
<script>
	document.getElementById("pass").focus()
</script>
</body>
</html>

