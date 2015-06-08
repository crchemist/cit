app.directive('userNamesurname', function(){
        return {
            restrict: 'A',
            transclude: true,
            template: '{{ user_data.fullUserName }}'
        }
    })
