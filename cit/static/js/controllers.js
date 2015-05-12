app.controller('LogoutCtrl', ['$scope', '$http', '$location', LogoutController]);
	function LogoutController($scope, $http, $location) {
			  $scope.logout = function(path){
                $http.get('/'+settings.url.auth_bp+settings.url.logout).
				success(function(data) { 
					$location.path('');						
					window.location.reload();													
  				});
			};			
		}