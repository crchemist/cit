
document.addEventListener("DOMContentLoaded", function () {
	var output = document.getElementById("map");

	if (!navigator.geolocation){
	    output.innerHTML = "<p>Geolocation is not supported by your browser</p>";
	    return;
	  }

	   function success(position) {
	   		var latitude  = position.coords.latitude;
   			var longitude = position.coords.longitude;
		   	var map = L.map('map').setView([latitude, longitude], 9);

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
		}

		function error() {
		    output.innerHTML = "Unable to retrieve your location";
		};

		navigator.geolocation.getCurrentPosition(success, error);
});



