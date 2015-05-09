app.controller('LogoutCtrl', ['$scope', '$http', '$location', LogoutController]);
	function LogoutController($scope, $http, $location) {
			  $scope.logout = function(path){
				$http.get('/auth/logout/').
				success(function(data) { 
					$location.path('');
					console.log(data);					
					window.location.reload();													
  				});
			};			
		}