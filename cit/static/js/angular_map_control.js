app.controller("MarkerController", [ '$scope', '$http','$rootScope', function($scope, $http, $rootScope) {
    $rootScope.markers = new Array();
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

        $scope.issueDescriptionShow = false;
        $scope.custom = true;

        markerClick = function(feature) {
            $scope.issueDescription = feature.target.feature.properties.description;
            $scope.issueDes = feature.target.feature.properties.photos;
           
            $scope.issueDescriptionShow = true;
            $scope.custom = false
        };

        angular.extend($scope, {
            markers: $rootScope.markers,
            geojson: {
                data: data,
                pointToLayer: function(feature, latlng) {
                    if (feature.properties.description == false) {
                        feature.properties.description = 'No description'
                    }
                    var customPopup = feature.properties.description;
                    marker = new L.marker(latlng, {icon: L.icon(leafIcon)}).bindPopup(customPopup).on('click', markerClick);
                    return marker;
                }
            }           
        });
    });
}]);

