var myApp = angular.module("myApp", [])

	.controller('UserNS', ['$scope', '$http', function($scope, $http) {

        $http.get('/auth/user-info/').success(function(data) {
            $scope.products = data;
            if (Object.keys($scope.products).length > 0) {
                $scope.products.fullNS = $scope.products.name + ' ' + $scope.products.surname;
            } else {
                $scope.products.fullNS = 'Sign in with Facebook';
            }
        });

    }])
    .directive('myCustomer', function(){
        return {
            restrict: 'E',
            transclude: true,
            template: '<a href="/auth/login/fb/" class="btn btn-lg  btn-block btn-social btn-facebook">'
                     + '<i class="fa fa-facebook"></i>' + '{{ products.fullNS }}' + '</a>'
        }
    })

