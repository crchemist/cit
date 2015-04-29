angular.module('CITApp.controllers', []).
controller("showNotificationsCtrl", ['$scope','$location', function($scope, $location) 
{
		$scope.say = function() {
			var m = $location.search();
			if (m !== "") {
				alert(m.mes);
			}
		};
	  }]);

