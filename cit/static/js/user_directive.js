app.controller('UserNS', ['$scope', '$http', '$window', function($scope, $http, $window) {

        $http.get('/auth/user-info/').success(function(data) {
            $scope.user_data = data;
            if (Object.keys($scope.user_data).length > 0) {
                $scope.user_data.fullUserName = $scope.user_data.first_name + ' ' + $scope.user_data.last_name;
            } else {
                $scope.user_data.fullUserName = null;
            }
        });

		$scope.hideSuccessMessage = true;
		$scope.hideErrorMessage = true;

		$scope.pushData = function() {
			var dataObj = {
				'name' : $scope.user_data.first_name,
				'surname' : $scope.user_data.last_name
			};
				
			$http.post('/auth/user/profile/',dataObj).
				success(function(data, status) {
					$scope.hideSuccessMessage = false;
					$scope.hideErrorMessage = true;
				}).
				error(function(data, status) {
					$scope.hideErrorMessage = false;
					$scope.hideSuccessMessage = true;
				});
		};

    }]);

app.directive('userNamesurname', function(){
        return {
            restrict: 'A',
            transclude: true,
            template: '{{ user_data.fullUserName }}'
        }
    })
