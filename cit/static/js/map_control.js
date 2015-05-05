
window.addEventListener("load", function () {
	var output = document.getElementById("map");
	var map;

	showMap(49.457, 31.765, 7);
	
	if (!navigator.geolocation){
		map.setView([49.457, 31.765], 7);
	    return;
	  }

	function success(position) {
	   	var latitude  = position.coords.latitude;
   		var longitude = position.coords.longitude;
   		var range = 9;
		map.setView([latitude, longitude], range);
	}

	function showMap(x,y,z) {
		map = L.map('map').setView([x, y], z);
		L.tileLayer('https://{s}.tiles.mapbox.com/v4/mdemitc.m0cg2hm8/{z}/{x}/{y}.png?access_token={id}', {
				id: 'pk.eyJ1IjoibWRlbWl0YyIsImEiOiJNR2thSnB3In0.IzaWDdO6nh0lGHnCO0V4Mw'
			}).addTo(map);
		
			new L.Control.GeoSearch({
				provider: new L.GeoSearch.Provider.OpenStreetMap(),
				showMarker: markerIcon
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
		map.setView([49.457, 31.765], 7);
	};


	navigator.geolocation.getCurrentPosition(success, error);
});



