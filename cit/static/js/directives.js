app.
directive('errorDirective',['$rootScope', '$location',function($rootScope, $location){
	return {
        restrict: 'AEC',
        controller:['$scope','$location', function($scope,$location){
        	
        	var termKey = "msg";
        	
        	$scope.$watch(function () { return $location.search(); }, function() {
				if ($location.search()[termKey]) 
					$scope.msg = $location.search()[termKey] ;
      			     			
      			//alert ("hello")
      		
    		});
     
		    $scope.$watch('msg', function(msg) {
		       $location.search(termKey, msg);
		       if(msg) alert(msg); //scope.$apply("fun.addAlert(msg)");//alert(msg);
		    });
        }] 
       
	
}}]);
