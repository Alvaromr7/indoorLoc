<!DOCTYPE html>
<html>
<head>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script type="text/javascript">
        // function ajax(){
        //     var req = new XMLHttpRequest();
        //     req.onreadystatechange = function(){
        //         if (req.readyState == 4 && req.status == 200) {
        //             document.getElementById('signallist').innerHTML = req.responseText;
        //         }
        //     }
        //     req.open('GET', '../connectedDevices.py', true);
        //     req.send();
        // }
        $.post({
        url: '../connectedDevices.py',
        data: {
                'signallist': signallist,
        },
        success: function(data) {
            console.log("post succeeded")
        }
    })
        //linea que hace que se refreseque la pagina cada segundo
        setInterval(function(){ajax();}, 1000);
    </script>
</head>
<body onload="ajax();">
    <table>
        <tr>
            <td>IP address</td>
            <td>Hostname</td>
            <td>MAC address</td>
            <td>Signal</td>
        </tr>
        %for i in range(len(maclist)):
            <tr>
                <td>{{iplist[i]}}</td>
                <td>{{hostlist[i]}}</td>
                <td>{{maclist[i]}}</td>
                <td>{{signallist[i]}}</td>
            </tr>
        %end
    </table>
</body>
</html>
