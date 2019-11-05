
var stackApp = angular.module("stackApp", []);

stackApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{/');
  $interpolateProvider.endSymbol('/}');
}]);

function processResponse(response, $scope) {
	var data = response['data']
	$scope.answers = data['answers']
	if (data['has_previous']==true) {
		$scope.previousTrue = 'previous'
		$scope.previous = data['previous_page_number']
		console.log('previous page ' + $scope.previous)
	} else {
		$scope.previousTrue = ''
	} 
	if(data['has_next']==true) {
		$scope.next = data['next_page_number']
		$scope.nextTrue = 'next'
	} else {
		$scope.nextTrue = ''
	}
}

stackApp.controller("stackCtrl", ['$scope', '$http',function($scope, $http){

	$scope.getAnswers = function() {
		$http.get('answers/?question='+$scope.question+'&page='+1,{}).then( 
			function (response){
				angular.element('table').css('display', 'block')
				angular.element('.pages').css('display', 'block')
				processResponse(response, $scope)
			}, function (failure) {
				console.log(failure)
			});
	}






	$scope.clicked = function($event) {
		console.log('This is '+$event.currentTarget.getAttribute('data-num'))
		var page = $event.currentTarget.getAttribute('data-num');
		//console.log($($event.target).data('num'));
		var question = $scope.questions;
		$http.get('answers/?question='+question+'&page='+page,{}).then( 
			function (response){
				console.log(response['data'])
				processResponse(response, $scope)
			}, function (failure) {
				console.log(failure)
			});
	}

}]);


/*function submit() {
	question = document.getElementById('question').value;
	$.get("/answers", {
		question: question,
		page: 1
	}, function(data) {
		console.log(data)
	});
}*/