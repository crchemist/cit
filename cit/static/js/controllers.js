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
				$scope.organization.push($scope.organizationsData.organizations[i]);
				
				console.log($scope.organization);
				
			}
			
		});

			$scope.pushOrganization = function(){
   			    for (var j=0; j< $scope.selectOrganization.length; j++){
					$http.post('/organizations/organizations/' + $scope.selectOrganization[j].id + '/add-user/').
						success(function(data, status){
							console.log('organization ADDED');
						}).
						error(function(data, status){
							console.log('adding organization FAILD');
						});
			};
	};

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
		
