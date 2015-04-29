 app.controller('AppCtrl', ['$scope', 'EzAlert', function($scope, EzAlert) {
        $scope.addAlert = function(type) {
	        console.log(type);
	        var text = "Warning"
	          EzAlert[type](type + text);
        };
      }])
      ;