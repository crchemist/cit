app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        template: "<div ng-transclude>></div>",
        transclude:true,
        link: function($scope, element, attrs){
        	$scope.showMessage = true;

    		$scope.closeAlert = function(){
    			$scope.showMessage = true;
    		}

        	$scope.$watch(function () { return $location.absUrl(); }, function() {
                if($location.search().msg){
                    $scope.msg = $location.search().msg;
                    $scope.showMessage =false;
                }
               // $scope.msg = $location.search().msg ;
    		});
    /* 
		$scope.$watch('msg', function(msg) {
			if(msg){
				$scope.showMessage =false;
			     }
            })
*/
        }
    }
}]);
