app.controller("MarkerController", [ '$scope', '$http','$rootScope', function($scope, $http, $rootScope) {

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
            markers: $rootScope.markers,
            geojson: {
                data: data,
                pointToLayer: function(feature, latlng) {
                    var customPopup = feature.properties.description + 
                                       '<br/><img src=' + feature.properties.photos + ' alt="photo of issue" width="200px"/>';
                    marker = new L.marker(latlng, {icon: L.icon(leafIcon)}).bindPopup(customPopup );
                    return marker;
                }
            }
            
        });
    });
}]);
