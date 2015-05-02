app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        template: "<div ng-transclude>></div>",
        transclude:true,
        link: function($scope, element, attrs){
        	
        	var termKey = "msg";
        	$scope.showMessage = true;

    		$scope.closeAlert = function(){
    			$scope.showMessage = true;
    		}



        	$scope.$watch(function () { return $location.search(); }, function() {
				if ($location.search()[termKey]) 
					$scope.msg = $location.search()[termKey] ;

    		});
     
		    $scope.$watch('msg', function(msg) {
		       $location.search(termKey, msg);
		       if(msg){ 
				    $scope.showMessage =false;
			     }
            })
        }
    }
}]);
