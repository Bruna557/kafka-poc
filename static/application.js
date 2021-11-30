$(document).ready(function(){
    const socket = io('ws://localhost:5000');

    ROUTES = {
        '7f788538-9be8-4510-8f01-1758ac269e01': 'route_1',
        'e11d1b63-6724-45c4-b70c-1b8382bb504e': 'route_2',
        'dbaac5ca-5bd5-48dc-b665-70c77619d7f0': 'route_3'
    }

    // receive details from server
    socket.on('avg_speed', function(msg) {
        res = JSON.parse(msg.data)
        console.log('Route: ' + ROUTES[res.route_id] + ' => speed: ' + res.speed + ' count: ' + res.count);
        document.getElementById(`${ROUTES[res.route_id]}_count`).innerHTML = res.count;
        document.getElementById(`${ROUTES[res.route_id]}_speed`).innerHTML = res.speed;
    });
});