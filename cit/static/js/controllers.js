app.controller('LogoutCtrl', ['$scope', '$http', '$location', changeLocation]);
	function changeLocation($scope, $http, $location) {
			$scope.redirect = function(path){
				$http.get('/auth/logout/').
				success(function(data) { 
					$location.path('/');
  				});
			}
	}