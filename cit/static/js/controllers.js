angular.module('CITApp.controllers', []).
controller("showNotificationsCtrl", ['$scope', '$window','$location', function($scope, $window, $location) {		
		$scope.say = function() {
			var m = $location.search();
			if (m !== "") {
				alert(m.mes);
			}
		};
	  }]);

