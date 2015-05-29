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
				$http.get('/auth/organizations/').
				success(function(data) {
					$scope.ogranization = data
					console.log($scope.ogranization);
       			});
		}

app.controller('IssueController',['$http', '$scope', function($http,$scope){
	this.issue = {
		'description': '',
		'address': 'POINT(49 22)'
	}
	
    var resultVarName = 'ajaxSubmitResult1';

    
	$http.post('http://localhost:8080/issues/make-issue/', this.issue, headers={'Content-Type': 'application/json'})
        .success(function (data, status, headers, config)
        {
          $scope[resultVarName] = data;
        })
        .error(function (data, status, headers, config)
        {
          $scope[resultVarName] = "SUBMIT ERROR";
        });

	function addIssue(issue, resultVarName){
        
        

        

	};

}]);
		