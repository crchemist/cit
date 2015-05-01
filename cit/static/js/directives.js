app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        template: "<div ng-transclude><h3>Heading</h3></div>",
        transclude:true,
        link: function($scope, element, attrs){
        	
        	var termKey = "msg";
        	$scope.myVar = true;

    		$scope.closeAlert = function(){
    			$scope.myVar = true;
    		}

            $scope.change = function() {
                element.text();
            };

        	$scope.$watch(function () { return $location.search(); }, function() {
				if ($location.search()[termKey]) 
					$scope.msg = $location.search()[termKey] ;

    		});
     
		    $scope.$watch('msg', function(msg) {
		       $location.search(termKey, msg);
		       if(msg){ 
				    $scope.myVar =false;
			     }
            })
        }
    }
}]);
