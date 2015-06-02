app.controller("MarkerController", [ '$scope', '$http', function($scope, $http) {

    angular.extend($scope, {
        center: {
            autoDiscover: true
        }
    });

    $http.get("/issues/").success(function(data, status) {
        var leafIcon = {
            iconUrl: 'static/images/marker-icon.png',
            shadowUrl: 'static/images/marker-shadow.png'
        };

        angular.extend($scope, {
            geojson: {
                data: data,
                pointToLayer: function(feature, latlng) {
                    marker = new L.marker(latlng, {icon: L.icon(leafIcon)});
                    return marker;
                }
            }
            
        });
    });
}]);
