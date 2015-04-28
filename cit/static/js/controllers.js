angular.module('CITApp.controllers', []).
controller("showNotificationsCtrl", ['$scope', '$window','$location', function($scope, $window, $location) {		
		$scope.doGreeting = function() {
			var m =  $location.$$search.mes;
			if (m) $scope.mes = $location.$$search.mes;
			alert($scope.mes);
			console.log($scope.mes);
			
		};
	  }]);

