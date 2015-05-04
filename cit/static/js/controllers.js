app.config(["$routeProvider", function($routeProvider) {
    $routeProvider
        .when('logout', {
                  templateUrl: 'index.html',
                  controller: 'LogoutCtrl'
             })
    }])
app.controller('LogoutCtrl', ['$scope', '$http', '$location', LogoutController]);
	function LogoutController($scope, $http, $location) {
			$scope.logout = function(path){
				$http.get('/auth/logout/').
				success(function(data) { 
					$location.path('/');
  				});
			};
	}