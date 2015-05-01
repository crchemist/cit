app.controller('UserNS', ['$scope', '$http', function($scope, $http) {

        $http.get('/auth/user-info/').success(function(data) {
            $scope.products = data;
            if (Object.keys($scope.products).length > 0) {
                $scope.products.fullNS = $scope.products.name + ' ' + $scope.products.surname;
            } else {
                $scope.products.fullNS = '';
            }
        });

    }]);

app.directive('userNamesurname', function(){
        return {
            restrict: 'A',
            transclude: true,
            template: '{{ products.fullNS }}'
        }
    })