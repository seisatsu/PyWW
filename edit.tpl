<!doctype html>
<html>
<head>
    <title>{title} &raquo; {page} &raquo; [edit]</title>
    <link rel="stylesheet" href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css">
    <link rel="stylesheet" type="text/css" href="{baseurl}{stylesheet}" />
</head>
<body>

<p class="breadcrumbs"><a href="{baseurl}">{title}</a> &raquo; <a href="{baseurl}?page={page}">{page}</a> &raquo; <a href="{baseurl}?page={page}&edit=1">[edit]</a></p>

    <form action="{baseurl}?page={page}" method="post">
        <textarea name="newcontent" cols=64 rows=40>{content}</textarea>
        <br />
        <input class="button-commit pure-button" type="submit" value="Commit" />
    </form>
</body>
</html>
