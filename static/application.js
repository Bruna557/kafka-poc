$(document).ready(function(){
    const socket = io('ws://localhost:5000');
    var data_received = [];

    // receive details from server
    socket.on('car_detected', function(msg) {
        console.log('Received event' + msg.data);
        //maintain a list of ten data points
        if (data_received.length >= 10){
            data_received.shift()
        }
        data_received.push(msg.data);
        data_string = '';
        for (var i = 0; i < data_received.length; i++){
            data_string = data_string + '<p>' + data_received[i].toString() + '</p>';
        }
        $('#log').html(data_string);
    });
});