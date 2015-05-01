app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        link: function($scope, element, attrs){
        	
        	var termKey = "msg";
        	$scope.myVar = true;
        	$scope.$watch(function () { return $location.search(); }, function() {
				if ($location.search()[termKey]) 
					$scope.msg = $location.search()[termKey] ;
      			     			
      			//alert ("hello")
      		
    		});
     
		    $scope.$watch('msg', function(msg) {
		       $location.search(termKey, msg);
		       if(msg) alert(msg); //scope.$apply("fun.addAlert(msg)");//alert(msg);
		    });
}

       
	
}}]);
