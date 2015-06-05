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
					$scope.ogranization = data
					console.log($scope.ogranization);
       			});
		}

app.controller('IssueController',['$http', '$scope', '$rootScope','$route', function($http,$scope,$rootScope, $route){
	$rootScope.coord = '';
	this.issue = {
		'description': '',
		'address': ''
	}
            
    $rootScope.markers = new Array();

    $scope.$on('leafletDirectiveMap.click', function (event, wrap) {
      $rootScope.coord = "POINT(" + wrap.leafletEvent.latlng.lat + " " + wrap.leafletEvent.latlng.lng + ")";
      
      $rootScope.markers.length = 0;
      $rootScope.markers.push({
        lat: wrap.leafletEvent.latlng.lat,
        lng: wrap.leafletEvent.latlng.lng,
        });
    });

    
  this.addIssue = function(issue){
      if ($rootScope.coord !== ''){
    	this.issue.address = $rootScope.coord
      
      $http.post('/issues/make-issue/', issue,
        headers={'Content-Type': 'application/json'})
        .success(function (data)
        {
          $rootScope.success = true;
          $rootScope.faile = false;
          $rootScope.noCoord = false;
          $rootScope.coord = '';
          $route.reload();  
        })
        .error(function ()
        {
          $rootScope.faile = true;
          $rootScope.success = false;
        });       
       
       }
      else{
        $rootScope.noCoord = true;
        $rootScope.success = false;
      } 
	
	};

}]);
		
