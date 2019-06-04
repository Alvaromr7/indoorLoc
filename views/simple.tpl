<!DOCTYPE>
<html>
<head>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script type="text/javascript">
        function ajax(){
            var req = new XMLHttpRequest();

            req.onreadystatechange = function(){
                if (req.readyState == 4 && req.status == 200) {
                    document.getElementById('myTable').innerHTML = req.responseText;
                }
            }

            req.open('GET', 'http://localhost:8080/data', true);
            req.send();
        }

        setInterval(function(){ajax();}, 1000);
    </script>
</head>
<body>
    <table id="myTable">
        <tr>
            <td>MAC address</td>
            <td>RSSI</td>
        </tr>
        %for row in rows1:
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
        %end
        <tr>
            <td>MAC address</td>
            <td>RSSI</td>
        </tr>
        %for row in rows2:
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
        %end
    </table>
</body>
</html>
