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

//make possible for user select several organizations  
app.controller('OrganizationCtrl', ['$scope', '$http', getOrganization]);
function getOrganization($scope, $http) {
	//get names of organizations from database and show them in profile form
	$http.get('/organizations/').
	success(function(data) {
		$scope.organizationsData = data
		$scope.selectedOrganization = [];
		$scope.organization = [];
		
		for (var i=0; i< $scope.organizationsData.organizations.length; i++){
			//take all names of organizations from  database
			$scope.organization.push($scope.organizationsData.organizations[i]); 
		}
	});

	$scope.pushOrganization = function(){
		// go through each selectedOrganization
		//p.s. selectedOrganization gets data from ng-model in profile.html on submit button
	    for (var j=0; j< $scope.selectedOrganization.length; j++){
	    	//post each organization's id from selectOrganization into url and 
	    	//add user - organization dependency into database
			$http.post('/organizations/organizations/' + $scope.selectedOrganization[j].id + '/add-user/').
				success(function(data, status){
					console.log('Organization added successfully');
				}).
				error(function(data, status){
					console.log('Adding organization faild');
				});
        };
    };
}

app.controller('IssueController',['$http', '$scope', '$rootScope','$route', 
	function($http,$scope,$rootScope, $route){
	$rootScope.coord = '';
	this.issue = {
		'description': '',
		'address': ''
	}
            

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
		
