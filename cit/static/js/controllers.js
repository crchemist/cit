function MainCtrl($location) {
 $http.get('/auth/logout/').
 		success(function(data) { 
            $location = '/#';
        }).
 		error(function(data){
            alert('error');
        });
    }
app.controller('MainCtrl', ['$scope', '$http', MainCtrl]);