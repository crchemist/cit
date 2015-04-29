var map = L.map('map').setView([49.457, 30.465], 7);

L.tileLayer('https://{s}.tiles.mapbox.com/v4/mdemitc.m0cg2hm8/{z}/{x}/{y}.png?access_token={id}', {
			id: 'pk.eyJ1IjoibWRlbWl0YyIsImEiOiJNR2thSnB3In0.IzaWDdO6nh0lGHnCO0V4Mw'
		}).addTo(map);

//Markers
var markerIcon = L.icon({
    iconUrl: '/static/images/marker_img.png',
    iconSize: [57, 57]
});
var markerIcon_2 = L.icon({
    iconUrl: '/static/images/marker_icon.png',
    iconSize: [25, 41]
});

var marker = L.marker([49.457, 31.465], {icon: markerIcon}).addTo(map),
    marker_2 = L.marker([49.957, 35.465], {icon: markerIcon_2}).addTo(map),
    marker_3 = L.marker([49.957, 28.465], {icon: markerIcon_2}).addTo(map);

marker.bindPopup("Map control");
marker_2.bindPopup("Map");
marker_3.bindPopup("Map_3");
