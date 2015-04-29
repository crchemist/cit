angular.module('CITApp.controllers', []).
directive('errorDirective',['$location',function(location){
	return {
        restrict: 'AEC',
      //  transclude: true,//20
       
	//replace:true,
        link: function ($scope, $element, $attrs) {
			var elementPath = $attrs.href.substring(1);
			    $scope.$location = location;
var t = '$location.path()';
			    $scope.$watch('$location.path()', function(locationPath) {
				if (elementPath === locationPath)  
					//console.log('hello');
					alert(location);
				else {
					alert(t);
					// console.log(t)
//console.log(locationPath);
			   		 }
				});
		}

	}
}]);
