app.controller('LogoutCtrl', ['$scope', '$http', '$location', LogoutController]);
	function LogoutController($scope, $http, $location) {
			  $scope.logout = function(path){
				$http.get('/auth/logout/').
				success(function(data) {								
					window.location.reload();													
  				});
			};			
		}


app.controller('ContextCtrl',['$scope','$location',function($scope, $location) {
	$scope.showGallery = true;
	$scope.showMap = true;

	$scope.$watch(function() { 
					return $location.path(); 
			}, 
			function() {
				if($location.path() == '' || $location.path() == '/_=_' || $location.path() == '/auth/logout/') {
					$scope.showMap = true;
					$scope.showGallery = true;
				}
				else {
					$scope.showMap = true;
					$scope.showGallery = false;
				}

				if($location.path() == '/profile') {
					$scope.showMap = false;
					$scope.showGallery = false;
				}
				
     		});	
}]);

//Get Names of organizations and from show them in profile form
app.controller('OrganizationCtrl', ['$scope', '$http', '$location', getOrganization]);
function getOrganization($scope, $http) {
				$http.get('/organizations/').
				success(function(data) {
					$scope.ogranization = data
					console.log($scope.ogranization);
       			});
		}

app.controller('IssueController',['$http', '$scope', '$rootScope', '$location', function($http,$scope,$rootScope){
	this.issue = {
		'description': '',
		'address': ''
	}
    
    $scope.$on('leafletDirectiveMap.click', function (e, wrap) {
      $rootScope.coord = "POINT(" + wrap.leafletEvent.latlng.lat + " " + wrap.leafletEvent.latlng.lng + ")";
    });

    
  this.addIssue = function(issue){
      if ($rootScope.coord !== ''){
    	this.issue.address = $rootScope.coord
      };

      $http.post('/issues/make-issue/', issue,
        headers={'Content-Type': 'application/json'})
        .success(function (data)
        {
          return data
        })
        .error(function ()
        {
          alert("SUBMIT ERROR");
        });       

	};

}]);
		
