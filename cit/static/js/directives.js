app.directive('errorDirective',['$location',function($location) {
	return {
        restrict: 'AEC',
        template: "<div ng-transclude>></div>",
        transclude:true,
        link: function($scope, element, attrs){
        	$scope.hideMessage = true;

    		$scope.closeAlert = function(){
    			$scope.hideMessage = true;
    		}

        	$scope.$watch(function() { 
				return $location.absUrl(); }, 
			function() {
				if($location.search().msg) {
				    $scope.msg = $location.search().msg;
				    $scope.hideMessage =false;
				}              
     		});
            }
         }
 }]);
