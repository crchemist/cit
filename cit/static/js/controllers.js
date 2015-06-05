app.controller('LogoutCtrl', ['$scope', '$http', '$location', LogoutController]);
	function LogoutController($scope, $http, $location) {
			  $scope.logout = function(path){
				$http.get('/auth/logout/').
				success(function(data) {								
					window.location.reload();													
  				});
			};			
		}


app.controller('GalleryCtrl',['$scope','$location',function($scope, $location) {
	$scope.showContext = true;
	$scope.$watch(function() { 
					return $location.url(); 
			}, 
			function() {
				if($location.path() == '' || $location.path() == '/_=_' || $location.path() == '/auth/logout/') {
					 $scope.showContext = true;
				}
				else
					 $scope.showContext = false;
     		});	
}]);

//Get Names of organizations and from show them in profile form
app.controller('OrganizationCtrl', ['$scope', '$http', '$location', getOrganization]);
function getOrganization($scope, $http) {
				$http.get('/organizations/').
				success(function(data) {
					$scope.organizationsData = data
					$scope.selectOrganization = [];
					$scope.organization = [];
					for (var i=0; i< $scope.organizationsData.organizations.length; i++){
						$scope.organization.push($scope.organizationsData.organizations[i].name);
						console.log($scope.organization);
					}
					console.log($scope.organizationsData.organizations.length);
					console.log($scope.organizationsData.organizations);
					console.log($scope.selectOrganization);
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
		
