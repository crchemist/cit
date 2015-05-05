app.controller('UserNS', ['$scope', '$http', function($scope, $http) {

        $http.get('/auth/user-info/').success(function(data) {
            $scope.user_data = data;
            if (Object.keys($scope.user_data).length > 0) {
                $scope.user_data.fullNS = $scope.user_data.first_name + ' ' + $scope.user_data.last_name;
            } else {
                $scope.user_data.fullNS = '';
            }
        });

    }]);

app.directive('userNamesurname', function(){
        return {
            restrict: 'A',
            transclude: true,
            template: '{{ user_data.fullNS }}'
        }
    })