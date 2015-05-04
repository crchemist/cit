app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        template: "<div ng-transclude>></div>",
        transclude:true,
        link: function($scope, element, attrs){
        	
        	//var termKey = "msg";
        	$scope.showMessage = true;

    		$scope.closeAlert = function(){
    			$scope.showMessage = true;
    		}

        	$scope.$watch(function () { return $location.search().msg; }, function() {
			$scope.msg = $location.search().msg ;
    		});
     
		$scope.$watch('msg', function(msg) {
			if(msg){
				$scope.showMessage =false;
			     }
            })
        }
    }
}]);
