<!doctype html>
<html>
<head>
    <title>Editing {page}</title>
    <link rel="stylesheet" type="text/css" href="{baseurl}{stylesheet}" />
</head>
<body>
    <form action="{baseurl}?page={page}" method="post">
        <textarea name="newcontent" cols=64 rows=40>{content}</textarea>
        <br />
        <input type="submit" value="Commit" />
    </form>
</body>
</html>
