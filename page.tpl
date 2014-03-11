<!doctype html>
<html>
<head>
    <title>{page}</title>
    <link rel="stylesheet" type="text/css" href="{baseurl}{stylesheet}" />
</head>
<body>
    {rstparsed}<form action="{baseurl}?page={page}&action=edit" method="post">
        <input type="submit" value="Edit" />
    </form>
</body>
</html>
