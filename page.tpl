<!doctype html>
<html>
<head>
    <title>{page}</title>
    <link rel="stylesheet" type="text/css" href="{baseurl}{stylesheet}" />
</head>
<body>

<!--Begin ReStructured Text-->
{rstparsed}<!--End ReStructured Text-->
    <form action="{baseurl}?page={page}&edit=1" method="post">
        {editbutton}
    </form>
</body>
</html>
