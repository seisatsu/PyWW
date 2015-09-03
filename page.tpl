<!doctype html>
<html>
<head>
    <title>{title} &raquo; {page}</title>
    <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">
    <link rel="stylesheet" type="text/css" href="{baseurl}{stylesheet}" />
</head>
<body>

<p class="breadcrumbs"><a href="{baseurl}">{title}</a> &raquo; <a href="{baseurl}?page={page}">{page}</a></p>

<!--Begin ReStructured Text-->
{rstparsed}<!--End ReStructured Text-->

<form action="{baseurl}?page={page}&edit=1" method="post">
    {editbutton}
</form>
</body>
</html>
